#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Heatmap browser complex
"""
import sys
import traceback

import subprocess
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import pyqtSignal, pyqtSlot
from PyQt5.QtWebChannel import QWebChannel
from PyQt5.QtWidgets import QAction
import util
import pyqt_common

from pyqt_common import *

_scriptdir = os.path.dirname(os.path.realpath(__file__))
_scriptname = os.path.basename(os.path.realpath(__file__))
_accepted_dups_html = "acceptedduplicates.html"

class HMBrowserComplex(QtWidgets.QMainWindow, ui_class('hm_browser_window.ui')):
    """
    Control objects:
      - wvHeatMap --- heat map webview
      - wvFuzzyRepetitions --- repetitions webview
    """
    def __init__(self, parent=None, app: pyqt_common.EMUIApp=None):
        super(HMBrowserComplex, self).__init__(parent=parent)
        self.setupUi(self)  # method of ui_class

        self.app = app
        self.hm_page: QtWebEngineWidgets.QWebEnginePage = self.wvHeatMap.page()
        self.rp_page: QtWebEngineWidgets.QWebEnginePage = self.wvFuzzyRepetitions.page()

        self.splitter.setSizes([400,250])

        # ---- RP menu ----
        try:
            self.rp_page.view().setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
            self.rp_page.view().customContextMenuRequested.connect(self.web_context_menu)

            self.rp_menu = QtWidgets.QMenu()
            self.rp_menu_del_grp = self.rp_menu.addAction("Delete group")
            self.rp_menu_del_grp.triggered.connect(lambda: self.rp_page.runJavaScript("window.group_delete();"))
            self.rp_menu_del_dup = self.rp_menu.addAction("Delete duplicate")
            self.rp_menu_del_dup.triggered.connect(lambda: self.rp_page.runJavaScript("window.variation_delete();"))
        except Exception as e:
            print(e, file=sys.stderr)
        # ---- RP menu ----

        self.bindEvents()

    @QtCore.pyqtSlot(QtCore.QPoint)
    def web_context_menu(self, point):
        self.rp_menu.popup(self.rp_page.view().mapToGlobal(point))
        self.rp_page.runJavaScript(f"window.switch_to_tr({point.x()}, {point.y()});")

    @QtCore.pyqtSlot(str)
    def clog(self, txt):
        print("JAVASCRIPT:", txt)

    @QtCore.pyqtSlot(int, int, str)
    def src_select(self, start0, finish0, candidate_idx=None):
        print("SRC selection <-", start0, finish0, candidate_idx)
        self.hm_page.runJavaScript("select_source(%d, %d);" % (start0, finish0))

    @QtCore.pyqtSlot()
    def exportReport(self):
        dlg = QtWidgets.QFileDialog(self)
        sfn = dlg.getSaveFileName(self, 'Save Report to File', os.path.dirname(self.inputfile), 'HTML files (*.html)')
        if sfn and isinstance(sfn, tuple) and len(sfn[0]):
            fn = sfn[0]
            htmlpath = os.path.join(self.workfolder, _accepted_dups_html)
            util.save_standalone_html(htmlpath, fn)

    def loadRepetitions(self, url: str):
        """
        Failed to make it work with asyncio, lets try to do it by any means...
        :param url: URL
        :param app: EMUIApp
        :return: Nothing
        """
        # TODO: make use of pyqt_common.load_p_url_then_run_js_co !!!
        def loaded(ok: bool):
            try:
                if self.rp_page.url() != QtCore.QUrl(url):
                    print("Blank")
                elif not ok:
                    print("Something went wrong")
                else:  # loaded url, everything ok
                    self.rp_page.loadFinished.disconnect()
                    self.hmbc.registerObject('qtab', self)
                    # right now -- fire and forget
                    self.rp_page.runJavaScript(
                        pyqt_common.qwcjs("""
                        try {
                            window.qwc = new QWebChannel(qt.webChannelTransport, function (channel) {
                                try {
                                    window.qtab = channel.objects.qtab;
                                    window.adaptToQWebView();
                                } catch (ie) {
                                    alert(window.qtab);
                                    alert(ie);
                                }
                            });
                        } catch (e) {
                            alert(e);
                        }
                        """)
                    )
            except Exception as e:
                print(repr(e))
                traceback.print_stack()

        self.hmbc = QWebChannel(self.rp_page)
        self.rp_page.setWebChannel(self.hmbc)

        self.rp_page.loadFinished.connect(loaded)
        self.rp_page.load(QtCore.QUrl(url))

    def loadHeatMap(self, url: str):
        self.hm_url = url
        try:
            self.hm_page.loadFinished.connect(lambda ok: self.unsetCursor())
            self.hm_page.load(QtCore.QUrl(url))  # fire and forget
        except Exception as e:
            print(repr(e))
            traceback.print_stack()

    def nd2html(self, inputfile, workfolder, unfuzzy):
        self.app.processEvents()

        popen_args = [
                         sys.executable, '-OO', os.path.join(_scriptdir, "nearduplicates2html.py"),
                         "-sx", inputfile,
                         "-od", workfolder,
                         "-uf", 'yes' if unfuzzy else 'no',
                         "-evr", 'yes'
                     ]
        print("Reporting with: " + ' '.join(popen_args))
        reppr = subprocess.Popen(popen_args, stdout=subprocess.PIPE)

        oe = reppr.communicate()
        ffrc = reppr.returncode

        self.app.processEvents()

    @util.excprint
    def buildAndLoadND(self, inputfile, workfolder, unfuzzy):
        self.unfuzzy = unfuzzy
        self.inputfile = inputfile
        self.workfolder = workfolder

        with util.QHourGlass():
            self.nd2html(inputfile, workfolder, unfuzzy)
            pve = os.path.join(workfolder, _accepted_dups_html)
            self.loadRepetitions(pyqt_common.path2url(pve))

    @util.excprint
    def refreshND(self):
        with util.QHourGlass():
            self.buildAndLoadND(self.inputfile, self.workfolder, self.unfuzzy)

    def refreshHM(self):
        with util.QHourGlass():
            self.loadHeatMap(self.hm_url)

    def bindEvents(self):
        # self.shouldLoadHeatMap.connect(self.loadHeatMap)
        # self.shouldLoadRepetitions.connect(self.loadRepetitions)
        self.actionE_xport.triggered.connect(self.exportReport)
        pass
