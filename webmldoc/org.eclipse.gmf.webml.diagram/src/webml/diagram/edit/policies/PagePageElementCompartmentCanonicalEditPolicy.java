/*
 * 
 */
package webml.diagram.edit.policies;

import java.util.Collection;
import java.util.HashSet;
import java.util.Iterator;
import java.util.LinkedList;
import java.util.List;
import java.util.Set;

import org.eclipse.gmf.runtime.diagram.ui.editpolicies.CanonicalEditPolicy;
import org.eclipse.gmf.runtime.notation.View;

import webml.WebmlPackage;
import webml.diagram.edit.parts.ContentUnit2EditPart;
import webml.diagram.edit.parts.Page2EditPart;
import webml.diagram.part.WebmlDiagramUpdater;
import webml.diagram.part.WebmlNodeDescriptor;
import webml.diagram.part.WebmlVisualIDRegistry;

/**
 * @generated
 */
public class PagePageElementCompartmentCanonicalEditPolicy extends
		CanonicalEditPolicy {

	/**
	 * @generated
	 */
	Set myFeaturesToSynchronize;

	/**
	 * @generated
	 */
	protected List getSemanticChildrenList() {
		View viewObject = (View) getHost().getModel();
		List result = new LinkedList();
		for (Iterator it = WebmlDiagramUpdater
				.getPagePageElementCompartment_7004SemanticChildren(viewObject)
				.iterator(); it.hasNext();) {
			result.add(((WebmlNodeDescriptor) it.next()).getModelElement());
		}
		return result;
	}

	/**
	 * @generated
	 */
	protected boolean isOrphaned(Collection semanticChildren, final View view) {
		int visualID = WebmlVisualIDRegistry.getVisualID(view);
		switch (visualID) {
		case Page2EditPart.VISUAL_ID:
		case ContentUnit2EditPart.VISUAL_ID:
			if (!semanticChildren.contains(view.getElement())) {
				return true;
			}
		}
		return false;
	}

	/**
	 * @generated
	 */
	protected String getDefaultFactoryHint() {
		return null;
	}

	/**
	 * @generated
	 */
	protected Set getFeaturesToSynchronize() {
		if (myFeaturesToSynchronize == null) {
			myFeaturesToSynchronize = new HashSet();
			myFeaturesToSynchronize.add(WebmlPackage.eINSTANCE
					.getPage_Element());
		}
		return myFeaturesToSynchronize;
	}

}
