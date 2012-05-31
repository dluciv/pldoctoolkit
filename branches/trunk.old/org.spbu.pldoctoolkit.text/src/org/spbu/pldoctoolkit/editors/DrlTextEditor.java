package org.spbu.pldoctoolkit.editors;

import org.eclipse.jface.action.IMenuManager;
import org.eclipse.jface.action.MenuManager;
import org.eclipse.jface.text.source.ISourceViewer;
import org.eclipse.ui.editors.text.TextEditor;
import org.spbu.pldoctoolkit.DrlPublisherPlugin;
import org.spbu.pldoctoolkit.actions.BasicExportAction;
import org.spbu.pldoctoolkit.actions.InsertTemplateAction;
import org.spbu.pldoctoolkit.actions.PdfExportAction;
import org.spbu.pldoctoolkit.actions.ValidateDrlAction;
import org.spbu.pldoctoolkit.actions.ValidateDrlOnSaveAction;
import org.spbu.pldoctoolkit.templates.TemplatesDocument;

public class DrlTextEditor extends TextEditor {
	public static final String XML_PARTITIONING = "__drl_partitioning";
	
	public static final String VALIDATE_DRL_ON_SAVE = "validate_drl_on_save";
	public static final String VALIDATE_DRL = "validate_drl";
	public static final String EXPORT_TO_HTML = "export_to_html";
	public static final String EXPORT_TO_PDF = "export_to_pdf";
	//public static final String EXPORT_TO_HH = "export_to_html_help";
	//public static final String EXPORT_TO_DB = "export_to_docbook";
	public static final String [] INSERT_TEMPLATES = new String[1000];
	
	private ColorManager colorManager;

	public DrlTextEditor() {
		super();
		colorManager = new ColorManager();
		setSourceViewerConfiguration(new XMLConfiguration(colorManager, this));
		setDocumentProvider(new XMLDocumentProvider());
	}
	
	@Override
	protected void initializeEditor() {
		super.initializeEditor();
	}

	public void dispose() {
		colorManager.dispose();
		super.dispose();
	}
	
	@Override
	protected void editorSaved() {
		super.editorSaved();
		this.getAction(VALIDATE_DRL_ON_SAVE).run();
	}

	@Override
	protected void createActions() {
		super.createActions();
		try {
			setAction(VALIDATE_DRL_ON_SAVE, new ValidateDrlOnSaveAction(this));
		} catch (Exception e) {
			e.printStackTrace();
		}
		
		try {
			setAction(VALIDATE_DRL, new ValidateDrlAction(this));
		} catch (Exception e) {
			e.printStackTrace();
		}
		
		try {
			setAction(EXPORT_TO_HTML, new BasicExportAction(this, DrlPublisherPlugin.getURL("xsl/docbook/html/docbook.xsl"), "Export to HTML", "HTML", "html", false));
		} catch (Exception e) {
			e.printStackTrace();
		}
		
		try {
			setAction(EXPORT_TO_PDF, new PdfExportAction(this));
		} catch (Exception e) {
			e.printStackTrace();
		}
/*
		try {
			setAction(EXPORT_TO_HH, new BasicExportAction(this, DrlPublisherPlugin.getURL("xsl/docbook/htmlhelp/htmlhelp.xsl"), "Export to HTML Help", "HTML help", "hh", false));
		} catch (Exception e) {
			e.printStackTrace();
		}

		try {
			setAction(EXPORT_TO_DB, new BasicExportAction(this, null, "Export to DocBook", "DocBook", "db", true));
		} catch (Exception e) {
			e.printStackTrace();
		}
*/		
		try {
			TemplatesDocument templatesDocument = new TemplatesDocument();
			for (int i = 0; i < templatesDocument.numOfTemplates;i++){
					INSERT_TEMPLATES[i] = templatesDocument.templates[i].name;
			    	setAction(INSERT_TEMPLATES[i],	new InsertTemplateAction(this, INSERT_TEMPLATES[i]));
			}
		} catch (Exception e) {
			e.printStackTrace();
		}	
	}
	
	public ISourceViewer DrlGetSourceViewer(){
		return this.getSourceViewer();
	}
	
	public void editorContextMenuAboutToShow(IMenuManager menu) {
		super.editorContextMenuAboutToShow(menu);
		
		try {
			MenuManager subInsertTemplate = new MenuManager("Insert Template");
			TemplatesDocument templatesDocument = new TemplatesDocument();
			for(int i=0; i<templatesDocument.numOfTemplates; i++){
			    	addAction(subInsertTemplate, INSERT_TEMPLATES[i]);					
			}
			menu.add(subInsertTemplate);
		} catch (Exception e) {
			e.printStackTrace();
		}
	}
}