package org.spbu.pldoctoolkit.drlvisual.diagram.edit.parts;

import org.eclipse.draw2d.IFigure;
import org.eclipse.draw2d.geometry.Dimension;
import org.eclipse.draw2d.geometry.Point;
import org.eclipse.gef.GraphicalEditPart;
import org.eclipse.gmf.runtime.diagram.ui.editparts.LabelEditPart;
import org.eclipse.gmf.runtime.diagram.ui.figures.LabelLocator;
import org.eclipse.gmf.runtime.notation.NotationPackage;
import org.eclipse.gmf.runtime.notation.View;

/**
 * @generated
 */
public class DrlModelExtNodeLabelEditPart extends LabelEditPart {

	/**
	 * @generated
	 */
	public DrlModelExtNodeLabelEditPart(View view) {
		super(view);
	}

	/**
	 * @generated
	 */
	public void refreshBounds() {
		IFigure refFigure = ((GraphicalEditPart) getParent()).getFigure();
		int dx = ((Integer) getStructuralFeatureValue(NotationPackage.eINSTANCE
				.getLocation_X())).intValue();
		int dy = ((Integer) getStructuralFeatureValue(NotationPackage.eINSTANCE
				.getLocation_Y())).intValue();
		Point offset = new Point(dx, dy);
		getFigure().getParent().setConstraint(getFigure(),
				new LabelLocator(refFigure, offset, getKeyPoint()) {

					public void relocate(IFigure target) {
						Point location = getReferencePoint().getTranslated(
								getOffset());
						location.translate(-target.getBounds().width / 2, 0);
						target.setLocation(location);
						target.setSize(new Dimension(
								target.getPreferredSize().width, target
										.getPreferredSize().height));
					}

					protected Point getReferencePoint() {
						return getLabelLocation(parent);
					}
				});
	}

	/**
	 * @generated
	 */
	public Point getReferencePoint() {
		return getLabelLocation(((GraphicalEditPart) getParent()).getFigure());
	}

	/**
	 * @generated
	 */
	protected Point getLabelLocation(IFigure parent) {
		return parent.getBounds().getBottom();
	}
}