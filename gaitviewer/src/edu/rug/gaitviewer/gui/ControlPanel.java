package edu.rug.gaitviewer.gui;

import java.awt.Dimension;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.io.File;
import java.util.Hashtable;

import javax.swing.BoxLayout;
import javax.swing.JButton;
import javax.swing.JFileChooser;
import javax.swing.JLabel;
import javax.swing.JPanel;
import javax.swing.JSlider;
import javax.swing.ProgressMonitor;
import javax.swing.event.ChangeEvent;
import javax.swing.event.ChangeListener;
import javax.swing.filechooser.FileFilter;

import edu.rug.gaitviewer.model.Recording;
import edu.rug.gaitviewer.model.RecordingLoadedListener;
import edu.rug.gaitviewer.model.RecordingPlayer;
import edu.rug.gaitviewer.model.RecordingPlayerStatus;
import edu.rug.gaitviewer.model.RecordingPlayerStatusListener;
import edu.rug.gaitviewer.model.RecordingReader;
import edu.rug.gaitviewer.model.RecordingReaderStatusListener;

public class ControlPanel extends JPanel implements RecordingLoadedListener, RecordingReaderStatusListener, RecordingPlayerStatusListener {
	private RecordingPlayer recordingPlayer;
	private JSlider slider;
	private JLabel statusLabel;
	private ProgressMonitor progressMonitor;
	private JFileChooser fileChooser;
	private RecordingReader recordingReader;
	private JButton playStopButton;
	private class SliderChangeListener implements ChangeListener {
		private boolean active = true;
		
		public void setActive(boolean active) {
			this.active = active;
		}
		
		@Override
		public void stateChanged(ChangeEvent e) {
			if (active) {
				recordingPlayer.setCurrentRecordIndex(slider.getValue());
			}
		}
	};
	private SliderChangeListener sliderChangeListener;
	
	public ControlPanel(RecordingPlayer recordingPlayer) {
		this.recordingPlayer = recordingPlayer;
		
		setLayout(new BoxLayout(this, BoxLayout.PAGE_AXIS));
		setPreferredSize(new Dimension(800,120));
		
		recordingPlayer.addRecordingPlayerStatusListener(this);
		
		initSlider();
		initStatusLabel();
		initOpenFileButton();
		initPlayStopButton();
		initFileChooser();
	}
	
	private void initSlider() {
		slider = new JSlider(JSlider.HORIZONTAL);
		slider.setAlignmentX(CENTER_ALIGNMENT);
		slider.setPreferredSize(new Dimension(800,20));
		slider.setMinimum(0);
		sliderChangeListener = new SliderChangeListener();
		slider.addChangeListener(sliderChangeListener);
		slider.setValue(0);
		slider.setVisible(false);

		add(slider);
	}
	
	private void initStatusLabel() {
/*		statusLabel = new JLabel("No file loaded");
		statusLabel.setHorizontalAlignment(JLabel.CENTER);
		statusLabel.setAlignmentY(CENTER_ALIGNMENT);
		
		add(statusLabel);*/
	}
	
	private void initOpenFileButton() {
		JButton button = new JButton("Open MOCAP file");
		button.setAlignmentX(CENTER_ALIGNMENT);
		button.addActionListener(new ActionListener() {

			@Override
			public void actionPerformed(ActionEvent e) {
				openFile();
			}});
		add(button);
	}
	
	private void initFileChooser() {
		fileChooser = new JFileChooser();
		fileChooser.setFileFilter(new FileFilter() {

			@Override
			public boolean accept(File f) {
				return f.getName().contains("mocap");
			}

			@Override
			public String getDescription() {
				// TODO Auto-generated method stub
				return "MOCAP file filter";
			}});
	}
	
	private void openFile() {
		stopRecording();
		int returnVal = fileChooser.showOpenDialog(this);
		if (returnVal == JFileChooser.APPROVE_OPTION) {
			File file = fileChooser.getSelectedFile();
			loadRecording(file);
		}
	}
	
	private void initPlayStopButton() {
		playStopButton = new JButton("Play");
		playStopButton.setAlignmentX(CENTER_ALIGNMENT);
		playStopButton.addActionListener(new ActionListener() {

			@Override
			public void actionPerformed(ActionEvent e) {
				if (recordingPlayer.isPlaying()) {
					stopRecording();
				} else {
					playRecording();
				}
			}});
		playStopButton.setVisible(false);
		add(playStopButton);
	}
	
	private void playRecording() {
		recordingPlayer.play();
		playStopButton.setText("Stop");
	}
	
	private void stopRecording() {
		recordingPlayer.stop();
		playStopButton.setText("Play");
	}

	@Override
	public void onRecordingLoaded(Recording recording) {
		progressMonitor.close();
		progressMonitor = null;
		
		recordingPlayer.setRecording(recording);
		
		int recordCount = recording.getRecordCount()-1;
		double seconds = recording.getDurationInSeconds();
		//System.out.println("Seconds = " + seconds);
		int oneSecondInRecords = (int)(recordCount / seconds);
		slider.setMaximum(recordCount);
		slider.setValue(0);
		Hashtable labelTable = new Hashtable();
		int s = 0;
		while (s < seconds) {
			labelTable.put(oneSecondInRecords*s, new JLabel(s + "s"));
			s = s + (int)(seconds / 10);
		}
		slider.setLabelTable(labelTable);
		
		//slider.setMajorTickSpacing(1000);
		//slider.setPaintTicks(true);
		slider.setPaintLabels(true);
		slider.setVisible(true);
		
		playStopButton.setVisible(true);
	}
	
	private void loadRecording(File file) {
		progressMonitor = new ProgressMonitor(this,
                "Loading file: " + file.getName(),
                "", 0, 100);
		progressMonitor.setMillisToDecideToPopup(0);
		
		recordingReader = new RecordingReader(file);
		recordingReader.setRecordingReaderStatusListener(this);
		recordingReader.setRecordingLoadedListener(this);
		new Thread(recordingReader).start();
	}

	@Override
	public void onRecordingReaderStatusUpdate(double progress) {
		progressMonitor.setProgress((int)(progress*100.0));
		
		if (progressMonitor.isCanceled()) {
			recordingReader.stopRecording();
			progressMonitor.close();
		}
		
	}

	@Override
	public void onRecordingPlayerStatusUpdate(RecordingPlayerStatus status) {
		sliderChangeListener.setActive(false);
		slider.setValue(status.getCurrentRecordIndex());
		sliderChangeListener.setActive(true);
	}
}
