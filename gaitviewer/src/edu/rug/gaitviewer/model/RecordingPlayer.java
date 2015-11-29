package edu.rug.gaitviewer.model;

import java.util.ArrayList;
import java.util.List;

public class RecordingPlayer{
	private Recording recording;
	private List<RecordViewer> recordViewers = new ArrayList<RecordViewer>();
	private int currentRecordIndex = 0;
	private Thread playerThread;
	private List<RecordingPlayerStatusListener> statusListeners = new ArrayList<RecordingPlayerStatusListener>();

	public RecordingPlayer() {
	}
	
	public RecordingPlayer(Recording recording) {
		setRecording(recording);
	}
	
	public void addRecordViewer(RecordViewer recordViewer) {
		this.recordViewers.add(recordViewer);
	}
	
	public void addRecordingPlayerStatusListener(RecordingPlayerStatusListener statusListener) {
		statusListeners.add(statusListener);
	}
	
	public Recording getRecording() {
		return this.recording;
	}
	
	public void setRecording(Recording recording) {
		stop();
		this.recording = recording;
	}

	public Record getCurrentRecord() {
		if (recording != null) {
			return recording.getRecord(currentRecordIndex);
		} else {
			return null;
		}
	}
	
	public void setCurrentRecordIndex(int currentRecordIndex) {
		//System.out.println("Current record index = " + currentRecordIndex);
		this.currentRecordIndex = currentRecordIndex;
		refreshViewers();
	}
	
	public boolean increaseCurrentRecordIndex(int step) {
		if (currentRecordIndex + step < recording.getRecordCount()) {
			setCurrentRecordIndex(currentRecordIndex + step);
			return true;
		} else {
			return false;
		}
	}
	
	public boolean increaseTimeStamp(double seconds) {
		double currentTimeStamp = getCurrentRecord().getTimeStamp();
		double targetTimeStamp = currentTimeStamp + seconds;
		int index = currentRecordIndex;
		while (index < recording.getRecordCount()) {
			double timeStamp = recording.getRecord(index).getTimeStamp();
			if (timeStamp > targetTimeStamp) {
				setCurrentRecordIndex(index);
				return true;
			}
			index++;
		}
		return false;
	}
	
	public boolean isPlaying() {
		return playerThread != null && !playerThread.isInterrupted();
	}
	
	public RecordingPlayerStatus getStatus() {
		RecordingPlayerStatus status = new RecordingPlayerStatus();
		
		status.setCurrentRecordIndex(currentRecordIndex);
		
		return status;
	}
	
	public void play() {
		playerThread = new Thread() {
			@Override
			public void run() {
				long t = System.currentTimeMillis();
				while (!isInterrupted()) {
					long td = System.currentTimeMillis() - t;
					if (td >= 100) {
						t = System.currentTimeMillis();
						if (!increaseTimeStamp(td*0.001)) {
							setCurrentRecordIndex(0);
						}
						for (RecordingPlayerStatusListener statusListener: statusListeners) {
							RecordingPlayerStatus status = getStatus();
							statusListener.onRecordingPlayerStatusUpdate(status);
						}
					}
				}
			}
		};
		playerThread.start();
	}
	
	public void stop() {
		if (playerThread != null) {
			playerThread.interrupt();
		}
		playerThread = null;
	}
	
	private void refreshViewers() {
		Record record = getCurrentRecord();
		if (record != null) {
			for (RecordViewer recordViewer: recordViewers) {
				recordViewer.showRecord(record);
			}
		}
	}
}
