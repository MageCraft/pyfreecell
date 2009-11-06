package com.frankz.aFreeCell;

import android.os.Bundle;
import android.preference.PreferenceActivity;

public class Preferences extends PreferenceActivity {
	public static final String KEY_ALERT_ILLEGAL_MOVE = "pref_key_alert_illegal_move";
	public static final String KEY_DISPLAY_GAME_STATUS = "pref_key_display_game_status";
	

	@Override
	protected void onCreate(Bundle savedInstanceState) {		
		super.onCreate(savedInstanceState);
		
		// Load the preferences from an XML resource
        addPreferencesFromResource(R.xml.preferences);
	}
	
}
