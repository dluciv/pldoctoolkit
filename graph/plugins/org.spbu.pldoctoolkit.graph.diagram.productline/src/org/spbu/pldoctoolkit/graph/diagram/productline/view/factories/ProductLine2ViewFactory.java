
package org.spbu.pldoctoolkit.graph.diagram.productline.view.factories;

import java.util.ArrayList;
import java.util.List;

import org.eclipse.core.runtime.IAdaptable;

import org.eclipse.emf.ecore.EAnnotation;
import org.eclipse.emf.ecore.EcoreFactory;

import org.eclipse.gmf.runtime.diagram.core.util.ViewUtil;

import org.eclipse.gmf.runtime.diagram.ui.view.factories.AbstractShapeViewFactory;

import org.eclipse.gmf.runtime.notation.NotationFactory;
import org.eclipse.gmf.runtime.notation.View;

import org.spbu.pldoctoolkit.graph.diagram.productline.edit.parts.ProductLine2EditPart;
import org.spbu.pldoctoolkit.graph.diagram.productline.edit.parts.ProductLineDocumentationCoreCompartmentEditPart;
import org.spbu.pldoctoolkit.graph.diagram.productline.edit.parts.ProductLineEditPart;
import org.spbu.pldoctoolkit.graph.diagram.productline.edit.parts.ProductLineNameEditPart;
import org.spbu.pldoctoolkit.graph.diagram.productline.edit.parts.ProductLinePLSchemeCompartmentEditPart;

import org.spbu.pldoctoolkit.graph.diagram.productline.part.DrlModelVisualIDRegistry;

/**
 * @generated
 */
public class ProductLine2ViewFactory extends 
	AbstractShapeViewFactory
{

	/**
	 * @generated 
	 */
	protected List createStyles(View view) {
		List styles = new ArrayList();
		styles.add(NotationFactory.eINSTANCE.createFontStyle());
		styles.add(NotationFactory.eINSTANCE.createDescriptionStyle());
		styles.add(NotationFactory.eINSTANCE.createFillStyle());
		styles.add(NotationFactory.eINSTANCE.createLineStyle());
		return styles;
	}

	/**
	 * @generated
	 */
	protected void decorateView(View containerView, View view, IAdaptable semanticAdapter,
			String semanticHint, int index, boolean persisted) {
		if (semanticHint == null) { 
			semanticHint = DrlModelVisualIDRegistry.getType(ProductLine2EditPart.VISUAL_ID);
			view.setType(semanticHint);
		}
		super.decorateView(containerView, view, semanticAdapter, semanticHint, index, persisted);		
		if (!ProductLineEditPart.MODEL_ID.equals(DrlModelVisualIDRegistry.getModelID(containerView))) {
			EAnnotation shortcutAnnotation = EcoreFactory.eINSTANCE.createEAnnotation();
			shortcutAnnotation.setSource("Shortcut"); //$NON-NLS-1$
			shortcutAnnotation.getDetails().put("modelID", ProductLineEditPart.MODEL_ID); //$NON-NLS-1$
			view.getEAnnotations().add(shortcutAnnotation);
		}
		getViewService().createNode(semanticAdapter, view, DrlModelVisualIDRegistry.getType(ProductLineNameEditPart.VISUAL_ID),
			ViewUtil.APPEND, true, getPreferencesHint());
		getViewService().createNode(semanticAdapter, view, DrlModelVisualIDRegistry.getType(ProductLinePLSchemeCompartmentEditPart.VISUAL_ID),
			ViewUtil.APPEND, true, getPreferencesHint());
		getViewService().createNode(semanticAdapter, view, DrlModelVisualIDRegistry.getType(ProductLineDocumentationCoreCompartmentEditPart.VISUAL_ID),
			ViewUtil.APPEND, true, getPreferencesHint());
	}

}
