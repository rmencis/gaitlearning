package edu.rug.gaitviewer;

import java.io.IOException;

import javax.swing.JFrame;

import edu.rug.gaitviewer.gui.MainFrame;
import edu.rug.gaitviewer.model.RecordingPlayer;

public class GaitViewer {

	public static void main(String[] args) throws IOException {
		//Recording recording = RecordingReader.readRecording(new File("/Users/rmencis/RUG/Machine_Learning/project/perturbed-walking-data-01/T031/mocap-031.txt"));
		RecordingPlayer recordingPlayer = new RecordingPlayer();

		MainFrame mainFrame = new MainFrame(recordingPlayer);
		mainFrame.setVisible(true);
		mainFrame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
	}

}
