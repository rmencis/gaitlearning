package edu.rug.gaitviewer.model;

public class RecordingPlayerStatus {
	private int currentRecordIndex;
	private double currentRecordTimeStampFromStart;

	public int getCurrentRecordIndex() {
		return currentRecordIndex;
	}

	public void setCurrentRecordIndex(int currentRecordIndex) {
		this.currentRecordIndex = currentRecordIndex;
	}

	public double getCurrentRecordTimeStampFromStart() {
		return currentRecordTimeStampFromStart;
	}

	public void setCurrentRecordTimeStampFromStart(
			double currentRecordTimeStampFromStart) {
		this.currentRecordTimeStampFromStart = currentRecordTimeStampFromStart;
	}
	
	
}
