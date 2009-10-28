package com.frankz.aFreeCell;

import android.util.Log;

public class MyLog {
	private final String logTag;
	public MyLog(String tag) {
		logTag = tag;
	}
	
	public int i(String msg) {
		return Log.i(logTag,msg);
	}
	
}
