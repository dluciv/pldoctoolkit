#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
import argparse
import os
import sys
import shutil
import tempfile
import TextDuplicateSearch as tds

logging.basicConfig(filename='fuzzyclones2html.log', level=logging.INFO)
logger = logging

def initargs():
    global args
    argpar = argparse.ArgumentParser()
    argpar.add_argument("-fx", "--fuzzy-xml", help="XML with fuzzy clones", type=str, default=None)
    argpar.add_argument("-ndgj", "--neardup-json", help="JSON with near dups", type=str, default=None)
    argpar.add_argument("-jfrm", "--json-format", help="Input JSON type", type=str, default="autofound")
    argpar.add_argument("-sx", "--source-xml", help="Source XML")
    argpar.add_argument("-od", "--output-directory", help="Report output directory")
    argpar.add_argument("-ob", "--open-browser", help="Open web browser", type=bool, default=False)
    argpar.add_argument("-num", "--number", help="Fragment size", type=int, default=20)
    argpar.add_argument("-hd", "--hash_dist", help="Max hash distance>", type=int, default=2)
    argpar.add_argument("-ed", "--edit_dist", help="Max edit distance", type=int, default=2)

    argpar.add_argument("-uf", "--unfuzzy",
                        help="Calculate archetype and make variative elements instead of fuzzy groups",
                        default="no")
    argpar.add_argument("-evr", "--editable-variative-report",
                        default="no", help="Add controls to delete group or duplicate")
    argpar.add_argument("-oui", "--only-ui",
                        help="Only generate data needed by standalone [Qt] UI", default="yes")
    args = argpar.parse_args()

    if not args.output_directory:
        args.output_directory = tempfile.mkdtemp(suffix='-dups-report')

    if args.open_browser:
        args.only_ui = "no"

only_generate_for_ui = None


def load_near_duplicates_json(logger):
    global args
    import clones
    import util
    import json

    """
    JSON example:
    {
        "groups": [
        {
          "group_id": 1,
          "duplicates": [
            {
              "start_index": 404,
              "end_index": 604,
              "text": "ZEXTERN int ZEXPORT deflateInit OF((z_streamp strm, int level)); Initializes the internal stream state for compression. The fields zalloc, zfree and opaque must be initialized before by the caller."
            },
            {
              "start_index": 8148,
              "end_index": 8358,
              "text": "ZEXTERN int ZEXPORT inflateInit OF((z_streamp strm)); Initializes the internal stream state for decompression. The fields next_in, avail_in, zalloc, zfree and opaque must be initialized before by the caller."
            }
          ]
        },
        {
          "group_id": 2,
          "duplicates": [
            {
              "start_index": 605,
              "end_index": 705,
              "text": "If zalloc and zfree are set to Z_NULL, deflateInit updates them to use default allocation functions."
            },
            {
              "start_index": 8579,
              "end_index": 8679,
              "text": "If zalloc and zfree are set to Z_NULL, inflateInit updates them to use default allocation functions."
            }
          ]
        },
        ...
      ]
    }
    """

    # default required settings for fuzzy groups
    clones.write_reformatted_sources = False
    clones.checkmarkup = False
    clones.only_generate_for_ui = args.only_ui == "yes"

    inputfile = clones.create_input_file_by_suffix(args.source_xml)
    clones.initdata([inputfile], [])

    with open(args.neardup_json, encoding='utf-8') as ndj:
        fuzzyclonedata = json.load(ndj)

    fgrps = []
    for fgrp in fuzzyclonedata['groups']:
        # here is group
        group_id = fgrp['group_id']
        fclns = []
        fclntexts = []
        fclnwords = []
        for fcln in fgrp['duplicates']:
            si = fcln['start_index']
            ei = fcln['end_index']
            tx = fcln['text']
            fclns.append((0, int(si), int(ei)))
            fclntexts.append(tx)
            fclnwords.append(util.ctokens(tx))

        fgrps.append(clones.FuzzyCloneGroup(
            group_id, fclns #, fclntexts, fclnwords
        ))

    clones.initdata([inputfile], fgrps)


def load_near_duplicates(logger):
    global args
    import clones
    import util

    # default required settings for fuzzy groups
    clones.write_reformatted_sources = False
    clones.checkmarkup = False
    clones.only_generate_for_ui = args.only_ui == "yes"

    inputfile = clones.create_input_file_by_suffix(args.source_xml)
    clones.initdata([inputfile], [])

    config = tds.create_config()
    config.input_file = args.source_xml
    if args.fuzzy_xml:
        config.searcher_type = 0  # fuzzy
    else:
        config.searcher_type = 1  # ngram
    config.fragment_size = args.number
    config.max_hashing_diff = args.hash_dist
    config.max_edit_distance = args.edit_dist

    duplicates = tds.fuzzy_search(config)

    fgrps = []
    for idx, case in enumerate(duplicates.cases):
        # here is group
        group_id = idx
        fclns = []
        fclntexts = []
        fclnwords = []
        for dup in case.text_fragments:
            si = dup.start.offset
            ei = dup.end.offset + len(dup.end.text)
            tx = str(dup)
            fclns.append((0, int(si), int(ei)))
            fclntexts.append(tx)
            fclnwords.append(util.ctokens(tx))

        fgrps.append(clones.FuzzyCloneGroup(
            group_id, fclns, fclntexts, fclnwords
        ))

    clones.initdata([inputfile], fgrps)


def load_dups_benchmark_json(logger):
    global args
    import clones
    import util
    import json

    clones.write_reformatted_sources = False
    clones.checkmarkup = False
    clones.only_generate_for_ui = args.only_ui == "yes"

    inputfile = clones.create_input_file_by_suffix(args.source_xml)

    with open(args.neardup_json, encoding='utf-8') as ndj:
        fuzzyclonedata = json.load(ndj)

    # Then the data... OMG...
    # It is all wrong now...
    fgrps = []
    for fgrp in fuzzyclonedata['Benchmarks']:
        # here is group
        group_id = fgrp['name']
        fclns = []
        fclntexts = []
        fclnwords = []
        for fcln in fgrp['group_ids']:
            [si, ei] = fcln['position']
            # tx = fcln['name2'] # not everywhere filled
            tx = inputfile.text[si:ei]
            fclns.append((0, int(si), int(ei)))
            fclntexts.append(tx)
            fclnwords.append(util.ctokens(tx))

        fgrps.append(clones.FuzzyCloneGroup(group_id, fclns, fclntexts, fclnwords))

    clones.initdata([inputfile], fgrps)


def report(logger):
    global args
    import webbrowser
    import clones
    import pathlib

    if args.unfuzzy in ["yes", "True", "1"]:
        import archetype_extraction
        clones.cm_inclusiveend = True
        ves = [archetype_extraction.get_variative_element(clones, g) for g in clones.clonegroups]
        ves = filter(None, ves)
        if args.editable_variative_report == 'yes':
            for ve in ves:
                ve.edit_controls = True
        cohtml = clones.VariativeElement.summaryhtml(ves, clones.ReportMode.variative)
    else:
        fuzzygroups = [clones.VariativeElement([cg]) for cg in clones.clonegroups]
        if args.editable_variative_report == 'yes':
            for ve in fuzzygroups:
                ve.edit_controls = True
        cohtml = clones.VariativeElement.summaryhtml(fuzzygroups, clones.ReportMode.fuzzyclones)

    outdir = args.output_directory
    with open(os.path.join(outdir, "pyvarelements.html"), 'w', encoding='utf-8') as htmlfile:
        htmlfile.write(cohtml)

    shutil.copyfile(
        os.path.join(os.path.dirname(os.path.abspath(__file__)), 'js', 'interactivity.js'),
        os.path.join(outdir, "interactivity.js")
    )
    shutil.copyfile(
        os.path.join(os.path.dirname(os.path.abspath(__file__)), 'js', 'jquery-2.0.3.min.js'),
        os.path.join(outdir, "jquery-2.0.3.min.js")
    )

    if args.open_browser:
        report_url = pathlib.Path(os.path.join(os.path.abspath(outdir), "pyvarelements.html")).as_uri()
        webbrowser.open(report_url)

if __name__ == '__main__':
    logger.info(f"fuzzyclones2html: {' '.join(sys.argv)}")
    initargs()

    if args.json_format == "autofound":
        if args.neardup_json:
            load_near_duplicates_json(logger)
        else:
            load_near_duplicates(logger)
    else:
        load_dups_benchmark_json(logger)

    report(logger)
