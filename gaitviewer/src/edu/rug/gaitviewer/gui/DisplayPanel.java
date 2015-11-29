package edu.rug.gaitviewer.gui;

import java.io.File;
import java.io.IOException;

import javax.swing.BoxLayout;
import javax.swing.JPanel;

import org.apache.commons.math3.linear.Array2DRowRealMatrix;
import org.apache.commons.math3.linear.ArrayRealVector;

import edu.rug.gaitviewer.model.Recording;
import edu.rug.gaitviewer.model.RecordingPlayer;
import edu.rug.gaitviewer.model.RecordingReader;

public class DisplayPanel extends JPanel {
	public DisplayPanel(RecordingPlayer recordingPlayer) throws IOException {
		setLayout(new BoxLayout(this, BoxLayout.LINE_AXIS));
		
		int width = 300;
		int height = 300;

		// BACK
		ViewerPanel backViewPanel = new ViewerPanel(width,height);
		Array2DRowRealMatrix backTM = new Array2DRowRealMatrix(2,3);
		backTM.setEntry(0, 0, 150); backTM.setEntry(0, 1, 0); backTM.setEntry(0, 2, 0);
		backTM.setEntry(1, 0, 0); backTM.setEntry(1, 1, -150); backTM.setEntry(1, 2, 0);
		backViewPanel.setTransformMatrix(backTM);
		backViewPanel.setCenterPoint(new ArrayRealVector(new double[]{width/2,height}));
		add(backViewPanel);
		recordingPlayer.addRecordViewer(backViewPanel);
		
		// RIGHT SIDE
		ViewerPanel rightSideViewPanel = new ViewerPanel(width,height);
		Array2DRowRealMatrix rightTM = new Array2DRowRealMatrix(2,3);
		rightTM.setEntry(0, 0, 0); rightTM.setEntry(0, 1, 0); rightTM.setEntry(0, 2, -150);
		rightTM.setEntry(1, 0, 0); rightTM.setEntry(1, 1, -150); rightTM.setEntry(1, 2, 0);
		rightSideViewPanel.setTransformMatrix(rightTM);
		rightSideViewPanel.setCenterPoint(new ArrayRealVector(new double[]{width/2,height}));
		add(rightSideViewPanel);
		recordingPlayer.addRecordViewer(rightSideViewPanel);

		// TOP
		ViewerPanel topViewPanel = new ViewerPanel(width,height);
		Array2DRowRealMatrix topTM = new Array2DRowRealMatrix(2,3);
		topTM.setEntry(0, 0, 150); topTM.setEntry(0, 1, 0); topTM.setEntry(0, 2, 0);
		topTM.setEntry(1, 0, 0); topTM.setEntry(1, 1, 0); topTM.setEntry(1, 2, 150);
		topViewPanel.setTransformMatrix(topTM);
		topViewPanel.setCenterPoint(new ArrayRealVector(new double[]{width/2,height/2}));
		add(topViewPanel);
		recordingPlayer.addRecordViewer(topViewPanel);
		
	}
}
