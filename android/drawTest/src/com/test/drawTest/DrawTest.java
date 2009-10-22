package com.test.drawTest;

import android.app.Activity;
import android.os.*;
import android.view.Menu;
import android.view.MenuItem;
import android.app.Dialog;
import android.app.AlertDialog;
import android.content.DialogInterface;

import com.test.drawTest.MyView;
import com.test.drawTest.MyView.State;


public class DrawTest extends Activity {
	
	private static final int MENU_NEW_GAME = 0;
	private static final int MENU_REPLAY_GAME = 1;
	private static final int MENU_SELECT_GAME = 2;
	private static final int MENU_UNDO = 3;
	private static final int MENU_REDO = 4;
	private static final int MENU_SETTINGS = 5;
	
	private static final int DIALOG_NEW_GAME = 0;
	private static final int DIALOG_REPLAY_GAME = 1;
	private static final int DIALOG_CURRENT_GAME_DONE = 2;
	
	private MyView cardView;
	
    /** Called when the activity is first created. */
    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.main);
        cardView = (MyView)findViewById(R.id.cardView);
    }
    
    public boolean onCreateOptionsMenu(Menu menu) {
    	menu.add(0,MENU_NEW_GAME, 0, "New Game");
    	menu.add(0,MENU_REPLAY_GAME, 0, "Replay");
    	menu.add(0,MENU_SELECT_GAME, 0, "Select...");
    	menu.add(0,MENU_UNDO, 0, "Undo");
    	menu.add(0,MENU_REDO, 0, "Redo");
    	menu.add(0,MENU_SETTINGS, 0, "Settings");
    	return true;
    }
    
    public boolean onOptionsItemSelected(MenuItem item) {
    	switch(item.getItemId()) {
    	case MENU_NEW_GAME:
    		newGame(true);
    		break;
    	case MENU_REPLAY_GAME:
    		replayGame(true);
    		break;
    	case MENU_SELECT_GAME:
    		selectGameToPlay();
			break;
    	case MENU_UNDO:
			break;
    	case MENU_REDO:
			break;
    	case MENU_SETTINGS:
			break;	
    	}
    	return true;
    }    
    
    
    protected Dialog onCreateDialog(int id) {    	
    	AlertDialog.Builder builder = new AlertDialog.Builder(this);
    	switch(id) {
    	case DIALOG_NEW_GAME:    		
    		builder.setMessage("Are you sure you want to replay current game?");
    		builder.setCancelable(false);
    		builder.setPositiveButton("Yes", new DialogInterface.OnClickListener() {				
				public void onClick(DialogInterface dialog, int which) {					
					DrawTest.this.newGame(false);
				}
			});
    		builder.setNegativeButton("No", new DialogInterface.OnClickListener() {				
				public void onClick(DialogInterface dialog, int which) {
					dialog.cancel();					
				}
			});
    		break;
    	case DIALOG_REPLAY_GAME:
    		builder.setMessage("Are you sure you want to end current game?");
    		builder.setCancelable(false);
    		builder.setPositiveButton("Yes", new DialogInterface.OnClickListener() {				
				public void onClick(DialogInterface dialog, int which) {					
					DrawTest.this.replayGame(false);
				}
			});
    		builder.setNegativeButton("No", new DialogInterface.OnClickListener() {				
				public void onClick(DialogInterface dialog, int which) {
					dialog.cancel();					
				}
			});
    		break;
    	case DIALOG_CURRENT_GAME_DONE:
    		break;
    	}    	
    	return builder.create();    	
    }
    
    private void newGame(boolean showAlert) {
    	if(showAlert && cardView.getState() == State.Playing) {
    		showDialog(DIALOG_NEW_GAME);
    		return;
    	}
    	cardView.playNewGame();
    }
    
    private void replayGame(boolean showAlert) {
    	if(showAlert && cardView.getState() == State.Playing) {
    		showDialog(DIALOG_REPLAY_GAME);
    		return;
    	}
    	cardView.replayGame();
    }
    
    private void selectGameToPlay() {
    	
    }
}