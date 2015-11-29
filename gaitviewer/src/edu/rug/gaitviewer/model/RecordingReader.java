package edu.rug.gaitviewer.model;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;
import java.util.StringTokenizer;

import org.apache.commons.math3.linear.ArrayRealVector;

public class RecordingReader implements Runnable {
	private File file;
	private Recording recording;
	private RecordingReaderStatusListener statusListener;
	private RecordingLoadedListener loadedListener;
	private boolean running = false;
	
	public RecordingReader(File file) {
		this.file = file;
	}
	
	public void setRecordingReaderStatusListener(RecordingReaderStatusListener statusListener) {
		this.statusListener = statusListener;
	}
	
	public void setRecordingLoadedListener(RecordingLoadedListener loadedListener) {
		this.loadedListener = loadedListener;
	}
	
	private void readRecording() throws IOException {
		recording = new Recording();

		List<String> headerColumns = null;

		BufferedReader br = new BufferedReader(new FileReader(file));
		long totalBytes = file.length();
		long readBytes = 0;
		String line;
		long t0 = System.currentTimeMillis();
		while ((line = br.readLine()) != null) {
			if (!running) {
				recording = null;
				System.out.println("Recording reader cancelled");
				break;
			}
			int byteCount = line.getBytes().length;
			readBytes = readBytes + byteCount;
			if (System.currentTimeMillis() - t0 > 500) {
				t0 = System.currentTimeMillis();
				if (statusListener != null) {
					statusListener.onRecordingReaderStatusUpdate((double)readBytes / (double)totalBytes);
				}
			}
			
			List<String> columns = splitLine(line);
			if (headerColumns == null) {
				headerColumns = columns;
			} else {
				Record record = new Record();
				
				int i = 0;
				while (i < headerColumns.size()) {
					String headerColumn = headerColumns.get(i);
					if ("TimeStamp".equals(headerColumn)) {
						record.setTimeStamp(Double.valueOf(columns.get(i)));
					} else if ("FrameNumber".equals(headerColumn)) {
						record.setFrameNumber(Integer.valueOf(columns.get(i)));
					} else {
						if (headerColumn.endsWith(".PosX")) {
							String marker = headerColumn.replace(".PosX", "");
							double x = Double.valueOf(columns.get(i));
							i++;
							double y = Double.valueOf(columns.get(i));
							i++;
							double z = Double.valueOf(columns.get(i));
							record.setMarkerCoord(marker, new ArrayRealVector(new double[]{x,y,z}));
						}
					}
					
					i++;
				}
				
				recording.addRecord(record);
				
				/*if (recording.getRecordCount() == 5000) {
					break;
				}*/
			}
		}
		br.close();
		if (loadedListener != null && recording != null) {
			loadedListener.onRecordingLoaded(recording);
		}
		System.out.println("Recording reader finished");
	}
	
	public void stopRecording() {
		running = false;
	}
	
	public Recording getRecording() {
		return recording;
	}

	private static List<String> splitLine(String line) {
		List<String> list = new ArrayList<String>();
		StringTokenizer st = new StringTokenizer(line, "\t");
		while (st.hasMoreTokens()) {
			String str = st.nextToken().trim();
			list.add(str);
		}
		return list;
	}

	@Override
	public void run() {
		try {
			running = true;
			readRecording();
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
	}
}
