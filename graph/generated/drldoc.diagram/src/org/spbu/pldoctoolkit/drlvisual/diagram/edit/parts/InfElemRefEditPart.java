package org.spbu.pldoctoolkit.drlvisual.diagram.edit.parts;

import java.beans.PropertyChangeEvent;

import org.eclipse.core.runtime.IStatus;
import org.eclipse.core.runtime.Status;
import org.eclipse.draw2d.Connection;
import org.eclipse.draw2d.PolygonDecoration;
import org.eclipse.draw2d.RotatableDecoration;
import org.eclipse.draw2d.geometry.PointList;
import org.eclipse.emf.common.notify.Notification;
import org.eclipse.gmf.runtime.diagram.ui.editparts.ConnectionNodeEditPart;
import org.eclipse.gmf.runtime.diagram.ui.editpolicies.EditPolicyRoles;
import org.eclipse.gmf.runtime.draw2d.ui.figures.PolylineConnectionEx;
import org.eclipse.gmf.runtime.notation.View;
import org.spbu.pldoctoolkit.drlvisual.InfElemRef;
import org.spbu.pldoctoolkit.drlvisual.diagram.edit.policies.InfElemRefItemSemanticEditPolicy;
import org.spbu.pldoctoolkit.drlvisual.diagram.part.DrlModelDiagramEditorPlugin;

/**
 * @generated
 */
public class InfElemRefEditPart extends ConnectionNodeEditPart {

	/**
	 * @generated
	 */
	public static final int VISUAL_ID = 3001;

	/**
	 * @generated
	 */
	public InfElemRefEditPart(View view) {
		super(view);
	}

	/**
	 * @generated
	 */
	protected void createDefaultEditPolicies() {
		super.createDefaultEditPolicies();
		installEditPolicy(EditPolicyRoles.SEMANTIC_ROLE,
				new InfElemRefItemSemanticEditPolicy());
	}

	/**
	 * Creates figure for this edit part.
	 *
	 * Body of this method does not depend on settings in generation model
	 * so you may safely remove <i>generated</i> tag and modify it.
	 *
	 * @generated NOT
	 */
	protected Connection createConnectionFigure() {
		return new InfElemRefFigure();
	}

	/* (non-Javadoc)
	 * @see org.eclipse.gmf.runtime.diagram.ui.editparts.ConnectionNodeEditPart#handleNotificationEvent(org.eclipse.emf.common.notify.Notification)
	 */
	@Override
	protected void handleNotificationEvent(Notification notification) {
		super.handleNotificationEvent(notification);

		((InfElemRefFigure) getFigure()).updateTargetDecoration();
	}

	/**
	 * @generated
	 */
	public class InfElemRefFigure extends
			org.eclipse.gmf.runtime.draw2d.ui.figures.PolylineConnectionEx {

		PolygonDecoration circleDecoration;

		/**
		 * @generated NOT
		 */
		public InfElemRefFigure() {
			circleDecoration = createTargetCircleDecoration();

			updateTargetDecoration();
		}

		public void updateTargetDecoration() {
			InfElemRef infElemRefInstance = (InfElemRef) ((View)getModel()).getElement();
			boolean isShowCircle = infElemRefInstance.isOptional();

			RotatableDecoration decoration;
			if(isShowCircle) {
				decoration = circleDecoration;
			} else {
				decoration = null;
			}

			setTargetDecoration(decoration);
		}


		/**
		 * @generated NOT
		 */
		private PolygonDecoration createTargetCircleDecoration() {
			PolygonDecoration df = new PolygonDecoration();
			// dispatchNext?

			PointList pl = new PointList();
			pl.addPoint(1, 4);
			pl.addPoint(3, 3);
			pl.addPoint(4, 1);
			pl.addPoint(4, -1);
			pl.addPoint(3, -3);
			pl.addPoint(1, -4);
			pl.addPoint(-1, -4);
			pl.addPoint(-3, -3);
			pl.addPoint(-4, -1);
			pl.addPoint(-4, 1);
			pl.addPoint(-3, 3);
			pl.addPoint(-1, 4);
			pl.addPoint(1, 4);
			df.setTemplate(pl);
			df.setScale(getMapMode().DPtoLP(1), getMapMode().DPtoLP(1));
			df.setFill(false);

			return df;
		}

	}

}