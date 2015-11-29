package edu.rug.gaitviewer.model;

import java.util.ArrayList;
import java.util.List;

public class Recording {
	private List<Record> records = new ArrayList<Record>();
	private double minTimeStamp = -1;
	private double maxTimeStamp = -1;
	
	public void addRecord(Record record) {
		records.add(record);
		if (minTimeStamp < 0 || record.getTimeStamp() < minTimeStamp) {
			minTimeStamp = record.getTimeStamp();
		}
		if (maxTimeStamp < 0 || record.getTimeStamp() > maxTimeStamp) {
			maxTimeStamp = record.getTimeStamp();
		}
	}
	
	public int getRecordCount() {
		return records.size();
	}
	
	public Record getRecord(int index) {
		return records.get(index);
	}
	
	public double getDurationInSeconds() {
		return maxTimeStamp - minTimeStamp;
	}
}
