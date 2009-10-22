package com.test.drawTest;

import android.app.Activity;
import android.os.*;
import android.view.Menu;
import android.view.MenuItem;
import android.app.Dialog;
import android.app.AlertDialog;
import android.content.DialogInterface;
import android.view.LayoutInflater;
import android.view.View;
import android.widget.EditText;

import com.test.drawTest.MyView;
import com.test.drawTest.MyView.State;


public class DrawTest extends Activity {
	
	private static final int MENU_NEW_GAME = 0;
	private static final int MENU_RESTART_GAME = 1;
	private static final int MENU_SELECT_GAME = 2;
	private static final int MENU_UNDO = 3;
	private static final int MENU_REDO = 4;
	private static final int MENU_SETTINGS = 5;	
	
	private static final int DIALOG_CHOOSE_GAME = 0;
	private static final int DIALOG_CURRENT_GAME_DONE = 1;
	private static final int DIALOG_END_CURRENT_GAME = 2;
	private static final int DIALOG_PICK_ACTION_ON_START = 3;
	
	private MyView cardView;	
	
	enum GameAction { NewGame, SelectGame, RestartGame }
	private GameAction gameAction;
	
	
    /** Called when the activity is first created. */
    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.main);
        cardView = (MyView)findViewById(R.id.cardView); 
        showDialog(DIALOG_PICK_ACTION_ON_START);
    }
    
    public boolean onCreateOptionsMenu(Menu menu) {
    	menu.add(0,MENU_NEW_GAME, 0, "New Game");    	
    	menu.add(0,MENU_SELECT_GAME, 0, "Select Game");
    	menu.add(0,MENU_RESTART_GAME, 0, "Restart Game");
    	menu.add(0,MENU_UNDO, 0, "Undo");
    	menu.add(0,MENU_REDO, 0, "Redo");
    	menu.add(0,MENU_SETTINGS, 0, "Settings");
    	return true;
    }
    
    public boolean onOptionsItemSelected(MenuItem item) {
    	switch(item.getItemId()) {
    	case MENU_NEW_GAME:
    		gameAction = GameAction.NewGame;
    		if(!alertUserAboutEndCurrentGame())
    			newGame();
    		break;
    	case MENU_RESTART_GAME:
    		gameAction = GameAction.RestartGame;
    		if(!alertUserAboutEndCurrentGame())
    			restartGame();    		
    		break;
    	case MENU_SELECT_GAME:
    		gameAction = GameAction.SelectGame;
    		if(!alertUserAboutEndCurrentGame())
    			selectGameToPlay(-1);    		
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
    	case DIALOG_PICK_ACTION_ON_START:
    		final CharSequence[] items = { "New Game", "Select Game", "Load Game" };
    		builder.setTitle("Pick a action");
    		builder.setItems(items, new DialogInterface.OnClickListener() {				
				public void onClick(DialogInterface dialog, int item) {					
					switch(item) {
					case 0://New game
						newGame();
						break;
					case 1://Select game
						showDialog(DIALOG_CHOOSE_GAME);
						break;
					default:
						break;
					}
				}
			});
    		break;
    	case DIALOG_END_CURRENT_GAME:    		
    		builder.setMessage("Do you want to resign this game?");
    		builder.setCancelable(false);
    		builder.setPositiveButton("Yes", new DialogInterface.OnClickListener() {				
				public void onClick(DialogInterface dialog, int which) {
					switch(gameAction) {
					case NewGame:
						DrawTest.this.newGame();
						break;
					case RestartGame:
						DrawTest.this.restartGame();
						break;
					case SelectGame:
						DrawTest.this.selectGameToPlay(-1);
						break;
					default:
						break;
					}					
				}
			});
    		builder.setNegativeButton("No", new DialogInterface.OnClickListener() {				
				public void onClick(DialogInterface dialog, int which) {
					dialog.cancel();					
				}
			});
    		break;    	
    	case DIALOG_CHOOSE_GAME:
    		LayoutInflater factory = LayoutInflater.from(this);
    		final View selectGameView = factory.inflate(R.layout.select_game_dialog, null);
    		builder.setTitle("Game number");
    		builder.setView(selectGameView);
    		builder.setPositiveButton("OK", new DialogInterface.OnClickListener() {				
				public void onClick(DialogInterface dialog, int which) {					
					EditText seedEdit = (EditText)selectGameView.findViewById(R.id.seedEdit);
					String content = seedEdit.getText().toString();					
					int seed = Integer.parseInt(content);
					DrawTest.this.selectGameToPlay(seed);
				}
			});
    		
    		break;
    	case DIALOG_CURRENT_GAME_DONE:
    		break;
    	}    	
    	return builder.create();    	
    }
    
    private boolean alertUserAboutEndCurrentGame() {
    	if(cardView.getState() == State.Playing) {
    		showDialog(DIALOG_END_CURRENT_GAME);
    		return true;
    	}
    	return false;
    }
    
    private void newGame() {    	
    	cardView.playNewGame();
    }
    
    private void restartGame() {    	
    	cardView.replayGame();
    }
    
    private void selectGameToPlay(int seed) {
    	if(seed < 0) {
    		showDialog(DIALOG_CHOOSE_GAME);
    	} else {
    		cardView.playSpecGame(seed);
    	}
    }
}