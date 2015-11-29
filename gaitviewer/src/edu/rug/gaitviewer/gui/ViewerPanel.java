package edu.rug.gaitviewer.gui;

import java.awt.Color;
import java.awt.Dimension;
import java.awt.Graphics;
import java.awt.Graphics2D;
import java.util.Collection;

import javax.swing.BorderFactory;
import javax.swing.JPanel;
import javax.swing.border.Border;

import org.apache.commons.math3.linear.RealMatrix;
import org.apache.commons.math3.linear.RealVector;

import edu.rug.gaitviewer.model.Record;
import edu.rug.gaitviewer.model.RecordViewer;

public class ViewerPanel extends JPanel implements RecordViewer {
	private RealMatrix transformMatrix; // 3 cols, 2 rows
	private RealVector centerPoint;
	private Record record;
	
	public ViewerPanel(int width,int height) {
		setPreferredSize(new Dimension(width, height));
		setMinimumSize(new Dimension(width, height));
		setMaximumSize(new Dimension(width, height));
		
		Border border = BorderFactory.createLineBorder(Color.WHITE, 3);
		setBorder(border);
	}
	
	
	
	public RealMatrix getTransformMatrix() {
		return transformMatrix;
	}



	public void setTransformMatrix(RealMatrix transformMatrix) {
		this.transformMatrix = transformMatrix;
	}



	public Record getRecord() {
		return record;
	}

	public void setRecord(Record record) {
		this.record = record;
	}
	
	@Override
	public void paintComponent(Graphics g1D) {
		Graphics2D g = (Graphics2D) g1D;

		g.setColor(Color.BLACK);
		g.fillRect(0, 0, getWidth(), getHeight());
		
		if (transformMatrix != null && record != null) {
			Collection<RealVector> coords = record.getAllCoords();
			for (RealVector coord: coords) {
				RealVector point = transformMatrix.operate(coord);
				point = point.add(centerPoint);
//				point.addToEntry(0, getWidth()/2);
//				point.addToEntry(1, getHeight()/2);
				drawPoint(g,(int)point.getEntry(0),(int)point.getEntry(1));
			}
		}
	}
	
	private void drawPoint(Graphics2D g,int x,int y) {
		g.setColor(Color.YELLOW);
		g.fillOval(x-2, y-2, 4, 4);
	}



	public RealVector getCenterPoint() {
		return centerPoint;
	}



	public void setCenterPoint(RealVector centerPoint) {
		this.centerPoint = centerPoint;
	}



	@Override
	public void showRecord(Record record) {
		setRecord(record);
		this.repaint();
	}
}
