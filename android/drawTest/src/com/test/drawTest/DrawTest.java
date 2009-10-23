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
import android.widget.TextView;
import java.text.MessageFormat;

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
    	menu.add(0,MENU_NEW_GAME, 0, getString(R.string.menu_new_game));    	
    	menu.add(0,MENU_SELECT_GAME, 0, getString(R.string.menu_select_game));
    	menu.add(0,MENU_RESTART_GAME, 0, getString(R.string.menu_restart_game));
    	menu.add(0,MENU_UNDO, 0, getString(R.string.menu_undo));
    	menu.add(0,MENU_REDO, 0, getString(R.string.menu_redo));
    	menu.add(0,MENU_SETTINGS, 0, getString(R.string.menu_settings));   
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
    		final CharSequence[] items = { getString(R.string.picker_opt_new_game),
    				 getString(R.string.picker_opt_select_game),
    				 getString(R.string.picker_opt_load_game)};
    		builder.setTitle(getString(R.string.picker_title));
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
    		builder.setMessage(getString(R.string.prompt_end_game));
    		builder.setCancelable(false);
    		CharSequence yes = getString(android.R.string.yes);
    		CharSequence no = getString(android.R.string.no);
    		builder.setPositiveButton(yes, new DialogInterface.OnClickListener() {				
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
    		builder.setNegativeButton(no, new DialogInterface.OnClickListener() {				
				public void onClick(DialogInterface dialog, int which) {
					dialog.cancel();					
				}
			});
    		break;    	
    	case DIALOG_CHOOSE_GAME:
    		LayoutInflater factory = LayoutInflater.from(this);
    		final View selectGameView = factory.inflate(R.layout.select_game_dialog, null);
    		TextView textView = (TextView)selectGameView.findViewById(R.id.text);
    		String prompt = getString(R.string.prompt_pick_game_number);
    		prompt = MessageFormat.format(prompt, Integer.toString(1), Integer.toString(30000));
    		textView.setText(prompt);
    		builder.setCancelable(false);
    		builder.setTitle(getString(R.string.dlg_title_game_number));
    		builder.setView(selectGameView);
    		CharSequence ok = getString(android.R.string.ok);
    		builder.setPositiveButton(ok, new DialogInterface.OnClickListener() {				
				public void onClick(DialogInterface dialog, int which) {					
					EditText seedEdit = (EditText)selectGameView.findViewById(R.id.seed_edit);
					String content = seedEdit.getText().toString();
					int seed = -1;
					try {
						seed = Integer.parseInt(content);
					} catch(NumberFormatException e) {
						seed = -1;
					}
					DrawTest.this.selectGameToPlay(seed);
				}
			});
    		
    		break;
    	case DIALOG_CURRENT_GAME_DONE:
    		break;
    	}    	
    	return builder.create();    	
    }
    
    private void setAppTitle(int seed) {
    	String title = getString(R.string.app_title);
    	title = MessageFormat.format(title, Integer.toString(seed));
    	setTitle(title);
    }
    
    private boolean validateSeed(int seed) {
    	return seed >= 1 && seed <= 30000;
    }
    
    private boolean alertUserAboutEndCurrentGame() {
    	if(cardView.getState() == State.Playing) {
    		showDialog(DIALOG_END_CURRENT_GAME);
    		return true;
    	}
    	return false;
    }
    
    private void newGame() {    	
    	int seed = cardView.playNewGame();
    	setAppTitle(seed);
    }
    
    private void restartGame() {    	
    	cardView.replayGame();
    }
    
    private void selectGameToPlay(int seed) {    	
		if(!validateSeed(seed)) {
			showDialog(DIALOG_CHOOSE_GAME);
		} else {
			cardView.playSpecGame(seed);
			setAppTitle(seed);
		}
			
    }
}