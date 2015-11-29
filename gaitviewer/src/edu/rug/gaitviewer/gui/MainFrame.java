package edu.rug.gaitviewer.gui;

import java.io.IOException;

import javax.swing.BoxLayout;
import javax.swing.JFrame;

import edu.rug.gaitviewer.model.RecordingPlayer;

public class MainFrame extends JFrame {
	public MainFrame(RecordingPlayer recordingPlayer) throws IOException {
		setLayout(new BoxLayout(getContentPane(), BoxLayout.PAGE_AXIS));

		DisplayPanel displayPanel = new DisplayPanel(recordingPlayer);
		getContentPane().add(displayPanel);
		
		ControlPanel controlPanel = new ControlPanel(recordingPlayer);
		getContentPane().add(controlPanel);
		
		pack();
	}
}
