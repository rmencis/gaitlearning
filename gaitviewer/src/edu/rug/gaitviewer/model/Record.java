package edu.rug.gaitviewer.model;

import java.util.Collection;
import java.util.HashMap;

import org.apache.commons.math3.linear.RealVector;

public class Record {
	private double timeStamp;
	private int frameNumber;
	private HashMap<String,RealVector> markerCoord = new HashMap<String,RealVector>();
	public double getTimeStamp() {
		return timeStamp;
	}
	public void setTimeStamp(double timeStamp) {
		this.timeStamp = timeStamp;
	}
	public int getFrameNumber() {
		return frameNumber;
	}
	public void setFrameNumber(int frameNumber) {
		this.frameNumber = frameNumber;
	}
	
	public void setMarkerCoord(String marker,RealVector coord) {
		markerCoord.put(marker, coord);
	}
	
	public RealVector getMarkerCoord(String marker) {
		return markerCoord.get(marker);
	}
	
	public Collection<RealVector> getAllCoords() {
		return markerCoord.values();
	}
}
