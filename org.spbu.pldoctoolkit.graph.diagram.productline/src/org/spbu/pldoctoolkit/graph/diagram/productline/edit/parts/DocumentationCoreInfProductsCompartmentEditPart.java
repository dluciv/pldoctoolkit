package org.spbu.pldoctoolkit.graph.diagram.productline.edit.parts;

import org.eclipse.draw2d.IFigure;
import org.eclipse.emf.common.notify.Notification;
import org.eclipse.gef.EditPart;
import org.eclipse.gef.EditPolicy;
import org.eclipse.gef.Request;
import org.eclipse.gef.commands.Command;
import org.eclipse.gef.commands.UnexecutableCommand;
import org.eclipse.gef.editpolicies.LayoutEditPolicy;
import org.eclipse.gef.editpolicies.NonResizableEditPolicy;
import org.eclipse.gef.requests.CreateRequest;
import org.eclipse.gef.requests.GroupRequest;
import org.eclipse.gmf.runtime.diagram.ui.editparts.ListCompartmentEditPart;
import org.eclipse.gmf.runtime.diagram.ui.editpolicies.ComponentEditPolicy;
import org.eclipse.gmf.runtime.diagram.ui.editpolicies.CreationEditPolicy;
import org.eclipse.gmf.runtime.diagram.ui.editpolicies.DragDropEditPolicy;
import org.eclipse.gmf.runtime.diagram.ui.editpolicies.EditPolicyRoles;
import org.eclipse.gmf.runtime.diagram.ui.figures.ResizableCompartmentFigure;
import org.eclipse.gmf.runtime.draw2d.ui.figures.ConstrainedToolbarLayout;
import org.eclipse.gmf.runtime.notation.View;
import org.spbu.pldoctoolkit.graph.diagram.productline.edit.policies.DocumentationCoreInfProductsCompartmentCanonicalEditPolicy;
import org.spbu.pldoctoolkit.graph.diagram.productline.edit.policies.DocumentationCoreInfProductsCompartmentItemSemanticEditPolicy;
import org.spbu.pldoctoolkit.graph.diagram.productline.edit.policies.PLSchemeProductsCompartmentItemSemanticEditPolicy;
import org.spbu.pldoctoolkit.graph.diagram.productline.part.Messages;

/**
 * @generated
 */
public class DocumentationCoreInfProductsCompartmentEditPart extends
		ListCompartmentEditPart {

	/**
	 * @generated
	 */
	public static final int VISUAL_ID = 5005;

	/**
	 * @generated
	 */
	public DocumentationCoreInfProductsCompartmentEditPart(View view) {
		super(view);
	}

	/**
	 * @generated
	 */
	protected boolean hasModelChildrenChanged(Notification evt) {
		return false;
	}

	/**
	 * @generated
	 */
	public String getCompartmentName() {
		return Messages.DocumentationCoreInfProductsCompartmentEditPart_title;
	}

	/**
	 * @generated NOT
	 */
	public IFigure createFigure() {
		ResizableCompartmentFigure result = (ResizableCompartmentFigure) super
				.createFigure();
		result.setTitleVisibility(false);
		result.setBorder(null);

		ConstrainedToolbarLayout layout = (ConstrainedToolbarLayout) result
				.getContentPane().getLayoutManager();
		layout.setSpacing(3);
		layout.setStretchMinorAxis(true);
		layout.setStretchMajorAxis(false);

		return result;
	}

	/**
	 * @generated NOT
	 */
	protected void createDefaultEditPolicies() {
		super.createDefaultEditPolicies();
		installEditPolicy(EditPolicyRoles.CREATION_ROLE,
				new CreationEditPolicy());

		removeEditPolicy(EditPolicyRoles.DRAG_DROP_ROLE);

		//HAND
		installEditPolicy(
				EditPolicyRoles.CANONICAL_ROLE,
				new DocumentationCoreInfProductsCompartmentCanonicalEditPolicy());

		installEditPolicy(EditPolicy.LAYOUT_ROLE, createLayoutEditPolicy());
		installEditPolicy(EditPolicy.COMPONENT_ROLE,
				createComponentEditPolicy());
		installEditPolicy(EditPolicyRoles.SEMANTIC_ROLE,
				new PLSchemeProductsCompartmentItemSemanticEditPolicy());
		installEditPolicy(
				EditPolicyRoles.SEMANTIC_ROLE,
				new DocumentationCoreInfProductsCompartmentItemSemanticEditPolicy());
	}

	/**
	 * HAND
	 */
	protected LayoutEditPolicy createLayoutEditPolicy() {
		LayoutEditPolicy lep = new LayoutEditPolicy() {

			protected EditPolicy createChildEditPolicy(EditPart child) {
				EditPolicy result = child
						.getEditPolicy(EditPolicy.PRIMARY_DRAG_ROLE);
				if (result == null) {
					result = new NonResizableEditPolicy();
				}
				return result;
			}

			protected Command getMoveChildrenCommand(Request request) {
				return null;
			}

			protected Command getCreateCommand(CreateRequest request) {
				return null;
			}
		};
		return lep;
	}

	/**
	 * @return
	 */
	protected ComponentEditPolicy createComponentEditPolicy() {
		return new ComponentEditPolicy() {
			@Override
			protected Command createDeleteSemanticCommand(
					GroupRequest deleteRequest) {
				return UnexecutableCommand.INSTANCE;
			}

			@Override
			protected Command createDeleteViewCommand(GroupRequest deleteRequest) {
				return UnexecutableCommand.INSTANCE;
			}
		};
	}

	/**
	 * @generated
	 */
	protected void setRatio(Double ratio) {
		if (getFigure().getParent().getLayoutManager() instanceof ConstrainedToolbarLayout) {
			super.setRatio(ratio);
		}
	}

}
