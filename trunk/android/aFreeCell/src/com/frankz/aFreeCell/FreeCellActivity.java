package com.frankz.aFreeCell;

import android.app.Activity;
import android.os.*;
import android.preference.PreferenceManager;
import android.view.Menu;
import android.view.MenuItem;
import android.app.Dialog;
import android.app.AlertDialog;
import android.content.DialogInterface;
import android.content.SharedPreferences;
import android.view.LayoutInflater;
import android.view.View;
import android.view.View.OnClickListener;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;
import android.widget.Toast;
import android.content.Intent;
import android.content.pm.PackageInfo;
import android.content.pm.PackageManager;
import android.content.res.Configuration;

import java.text.MessageFormat;

import com.frankz.aFreeCell.FreeCellView.State;


public class FreeCellActivity extends Activity implements GameEventListener										
{
	
	private static final int MENU_NEW_GAME = 0;
	private static final int MENU_RESTART_GAME = 1;
	private static final int MENU_SELECT_GAME = 2;
	private static final int MENU_UNDO = 3;	
	private static final int MENU_SETTINGS = 5;
	private static final int MENU_ABOUT = 6;
	
	private static final int DIALOG_CHOOSE_GAME = 0;
	private static final int DIALOG_GAME_OVER = 1;
	private static final int DIALOG_END_CURRENT_GAME = 2;
	private static final int DIALOG_PICK_ACTION_ON_START = 3;
	private static final int DIALOG_MOVE_NOT_ALLOWED = 4;
	private static final int DIALOG_SUPERMOVE_NOT_ENOUGH_SPACE = 5;
	private static final int DIALOG_MOVE_TO_EMPTY_COLUMN = 6;
	private static final int DIALOG_ABOUT = 7;
	private static final int DIALOG_PICK_ACTION_ON_START_RESUME = 8;
	
	private static final int REQUEST_CODE_PREFERENCES = 0;	
	
	private FreeCellView cardView;
	private final MyLog log = new MyLog("FreeCellActivity"); 
	
	enum GameAction { NewGame, SelectGame, RestartGame }
	private GameAction gameAction;
	private Toast toastInvalidGameNumber;
	private String superMoveNotEnoughSpaceMsg;
	private Toast toastMoveNotAllowed;
	
    /** Called when the activity is first created. */
    @Override
    public void onCreate(Bundle savedInstanceState) {    	
        super.onCreate(savedInstanceState);
        log.i("onCreate");
        setContentView(R.layout.main);
        cardView = (FreeCellView)findViewById(R.id.cardView);
        cardView.setGameEventListener(this);        
        checkIllegalMoveAlertPref();
        if(playingGameWhenLastClose()) {
        	showDialog(DIALOG_PICK_ACTION_ON_START_RESUME);
        } else {
        	showDialog(DIALOG_PICK_ACTION_ON_START);
        }        
    }    
    
    public boolean onCreateOptionsMenu(Menu menu) {
    	menu.add(0,MENU_NEW_GAME, 0, getString(R.string.menu_new_game));    	
    	menu.add(0,MENU_SELECT_GAME, 0, getString(R.string.menu_select_game));
    	menu.add(0,MENU_RESTART_GAME, 0, getString(R.string.menu_restart_game));
    	menu.add(0,MENU_UNDO, 0, getString(R.string.menu_undo));    	
    	menu.add(0,MENU_SETTINGS, 0, getString(R.string.menu_settings));//.setIcon(android.R.drawable.ic_menu_preferences);
    	menu.add(0,MENU_ABOUT, 0, getString(R.string.menu_about));//.setIcon(android.R.drawable.ic_menu_info_details);
    	return true;
    }
    
    @Override
	public boolean onPrepareOptionsMenu(Menu menu) {
		MenuItem menuItemUndo = menu.findItem(MENU_UNDO);
		if(menuItemUndo!=null) {
			menuItemUndo.setEnabled(cardView.isUndoEnabled());
		}
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
    			selectGameToPlay(-1,false);    		
			break;
    	case MENU_UNDO:
    		undoGame();
			break;
    	case MENU_ABOUT:
    		showDialog(DIALOG_ABOUT);
			break;
    	case MENU_SETTINGS:
    		settings();
			break;	
    	}
    	return true;
    }    
    
    
    protected Dialog onCreateDialog(int id) {    	
    	AlertDialog.Builder builder = new AlertDialog.Builder(this);
    	LayoutInflater factory = LayoutInflater.from(this);
    	switch(id) {
    	case DIALOG_PICK_ACTION_ON_START_RESUME:
    		String resumeGameStr = MessageFormat.format(getString(R.string.picker_opt_resume_game), 
    												 Integer.toString(getLastPlayedGameNumber()));
    		final CharSequence[] items = { resumeGameStr, 
    				getString(R.string.picker_opt_new_game),
   				 	getString(R.string.picker_opt_select_game)};
    		builder.setCancelable(false);
    		builder.setTitle(R.string.picker_title);
    		builder.setItems(items, new DialogInterface.OnClickListener() {				
				public void onClick(DialogInterface dialog, int item) {					
					switch(item) {
					case 0://resume game
						load();
						break;
					case 1://New game
						newGame();
						break;
					case 2://Select game
						showDialog(DIALOG_CHOOSE_GAME);
						break;
					default:
						break;
					}
				}
			});
    		break;    		
    	case DIALOG_PICK_ACTION_ON_START:
    		final CharSequence[] items1 = { getString(R.string.picker_opt_new_game),
    				 getString(R.string.picker_opt_select_game)};
    		builder.setCancelable(false);
    		builder.setTitle(R.string.picker_title);
    		builder.setItems(items1, new DialogInterface.OnClickListener() {				
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
    		builder.setPositiveButton(R.string.yes, new DialogInterface.OnClickListener() {				
				public void onClick(DialogInterface dialog, int which) {
					switch(gameAction) {
					case NewGame:
						FreeCellActivity.this.newGame();
						break;
					case RestartGame:
						FreeCellActivity.this.restartGame();
						break;
					case SelectGame:
						FreeCellActivity.this.selectGameToPlay(-1,false);
						break;
					default:
						break;
					}					
				}
			});
    		builder.setNegativeButton(R.string.no, new DialogInterface.OnClickListener() {				
				public void onClick(DialogInterface dialog, int which) {
					//do nothing				
				}
			});
    		break;    	
    	case DIALOG_CHOOSE_GAME:    		
    		final View selectGameView = factory.inflate(R.layout.select_game_dialog, null);
    		TextView textView = (TextView)selectGameView.findViewById(R.id.text);
    		String prompt = getString(R.string.prompt_pick_game_number);
    		prompt = MessageFormat.format(prompt, Integer.toString(1), Integer.toString(30000));
    		textView.setText(prompt);
    		builder.setCancelable(false);
    		builder.setTitle(R.string.dlg_title_game_number);
    		builder.setView(selectGameView);    		
    		builder.setPositiveButton(R.string.ok, new DialogInterface.OnClickListener() {				
				public void onClick(DialogInterface dialog, int which) {					
					EditText seedEdit = (EditText)selectGameView.findViewById(R.id.seed_edit);
					String content = seedEdit.getText().toString();
					int seed = -1;
					try {
						seed = Integer.parseInt(content);
					} catch(NumberFormatException e) {
						seed = -1;
					}
					seedEdit.setText("");
					FreeCellActivity.this.selectGameToPlay(seed,true);
				}
			});    		
    		break;
    	case DIALOG_ABOUT:
    		final View aboutView = factory.inflate(R.layout.about_dialog, null);
    		TextView textAbout = (TextView)aboutView.findViewById(R.id.text_about);
    		PackageManager pm = getPackageManager();
    		String versionName = null;
    		try {
    			PackageInfo pi = pm.getPackageInfo(getPackageName(), 0);
    			versionName = pi.versionName;
    		} catch(PackageManager.NameNotFoundException ex) {
    			versionName = "";
    		}
    		String about = MessageFormat.format(getString(R.string.prompt_about), versionName);
    		textAbout.setText(about);
    		builder.setTitle(R.string.dlg_title_about);
    		builder.setView(aboutView);
    		  		
    		builder.setPositiveButton(R.string.ok, new DialogInterface.OnClickListener() {				
				public void onClick(DialogInterface dialog, int which) {
					//do nothing					
				}
			});
    		break;
    	case DIALOG_GAME_OVER: 
    		final CharSequence[] items2 = { getString(R.string.picker_opt_new_game),
    									getString(R.string.picker_opt_select_game) };
    		builder.setCancelable(false);
    		builder.setTitle(R.string.prompt_you_win);
    		builder.setItems(items2, new DialogInterface.OnClickListener() {				
				public void onClick(DialogInterface dialog, int item) {					
					switch(item) {
					case 0://New game
						newGame();
						break;
					case 1://Select game
						selectGameToPlay(-1,false);
						break;
					default:
						break;
					}
				}
			});    		
    		break;
    	case DIALOG_MOVE_NOT_ALLOWED:
    	case DIALOG_SUPERMOVE_NOT_ENOUGH_SPACE:
    		final View illegalMoveAlertView = factory.inflate(R.layout.illegal_move_alert, null);
    		TextView msg = (TextView)illegalMoveAlertView.findViewById(R.id.text);    		
    		if(id == DIALOG_MOVE_NOT_ALLOWED) {
    			msg.setText(R.string.prompt_move_not_allowed);
    		} else if(id == DIALOG_SUPERMOVE_NOT_ENOUGH_SPACE){    			
    			msg.setText(superMoveNotEnoughSpaceMsg);
    		}
    		builder.setView(illegalMoveAlertView);
    		builder.setTitle(R.string.dlg_title_illegal_move);
    		builder.setCancelable(false);    		
    		builder.setPositiveButton(R.string.ok, new DialogInterface.OnClickListener() {				
				public void onClick(DialogInterface dialog, int which) {					
					//do nothing
				}
			});
    		break;
    	case DIALOG_MOVE_TO_EMPTY_COLUMN:
    		final View move2EmptyColumnView = factory.inflate(R.layout.move_to_empty_column_dialog, null);
    		builder.setView(move2EmptyColumnView);
    		builder.setTitle(R.string.dlg_title_move_to_empty_column);    		
    		builder.setNegativeButton(R.string.cancel, new DialogInterface.OnClickListener() {				
				public void onClick(DialogInterface dialog, int which) {
					//do nothing					
				}
			});
    		final Dialog dlg = builder.create();
    		Button btn1 = (Button)move2EmptyColumnView.findViewById(R.id.btn_move_column);
    		btn1.setOnClickListener(new OnClickListener() {				
				public void onClick(View arg0) {
					dlg.dismiss();					
				}    			
    		});
    		Button btn2 = (Button)move2EmptyColumnView.findViewById(R.id.btn_move_single_card);
    		btn2.setOnClickListener(new OnClickListener() {				
				public void onClick(View arg0) {
					dlg.dismiss();					
				}    			
    		});
    		return dlg;
    		
    	default:    		
    		break;
    	}    	
    	return builder.create();   	
    } 
    
    
	@Override
	protected void onPause() {
		// TODO Auto-generated method stub
		super.onPause();
		log.i("onPause");		
	}

	@Override
	protected void onStop() {
		// TODO Auto-generated method stub
		super.onStop();
		log.i("onStop");
	}

	@Override
	protected void onDestroy() {		
		super.onDestroy();
		log.i("onDestroy");	
		save();
	}
	
	@Override
	public void onConfigurationChanged(Configuration newConfig) {		
		super.onConfigurationChanged(newConfig);
		//screen orientation changed
		//cardView.changeScreenOrientation();
	}

	private int getLastPlayedGameNumber() {
		SharedPreferences pref = PreferenceManager.getDefaultSharedPreferences(this);
		int gameNumber = pref.getInt("gameNumber", -1);
		return gameNumber;
	}
	
	private boolean playingGameWhenLastClose() {
		return getLastPlayedGameNumber() != -1;
	}
	
	private boolean load() {
		SharedPreferences pref = PreferenceManager.getDefaultSharedPreferences(this);
		int gameNumber = getLastPlayedGameNumber();
		//int leftCard = pref.getInt("leftCard", -1);
		String freeSlotsSavedString = pref.getString("freeSlots", "");
		String homeSlotsSavedString = pref.getString("homeSlots", "");
		String fieldColumnsSavedString = pref.getString("fieldColumns", "");
		if(gameNumber != -1) {
			cardView.playSavedGame(gameNumber, freeSlotsSavedString, homeSlotsSavedString, fieldColumnsSavedString);
			setAppTitle(gameNumber);
			return true;
		}
		return false;
	}
	
	private void save() {
		//game number - int, -1 means first time
		//left card - int, 0 means game over
		//free slots - string, v1,v2,v3,v4, -1 means empty
		//home slots - string, v1,v2,v3,v4, -1 means empty
		//field columns - string, v1,v2...#v1,v2...#v1,v2#...		
		SharedPreferences pref = PreferenceManager.getDefaultSharedPreferences(this);
		SharedPreferences.Editor editor = pref.edit();
		editor.putInt("gameNumber", cardView.getSeed());
		editor.putInt("leftCard", cardView.getLeftCardCount());
		if(true) {
			editor.putString("freeSlots", cardView.freeSlotsSave2String());
			editor.putString("homeSlots", cardView.homeSlotsSave2String());
			editor.putString("fieldColumns", cardView.fieldColumnsSave2String());
		}
		editor.commit();		
	}

	private void setAppTitle(int number) {
    	String title = getString(R.string.app_title);
    	title = MessageFormat.format(title, Integer.toString(number));
    	setTitle(title);
    }
    
    private boolean validateSeed(int number) {
    	return number >= 1 && number <= 30000;
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
    
    private void undoGame() {
    	cardView.undo();
    }
    
    private void settings() {
    	Intent settingsActivity = new Intent().setClass(this, Preferences.class);
    	startActivityForResult(settingsActivity, REQUEST_CODE_PREFERENCES);
    }
    
	@Override
	protected void onActivityResult(int requestCode, int resultCode, Intent data) {
		super.onActivityResult(requestCode, resultCode, data);
		if(requestCode == REQUEST_CODE_PREFERENCES) {
			checkIllegalMoveAlertPref();			
		}
	}
	
	private void checkIllegalMoveAlertPref() {
		SharedPreferences sharedPref = PreferenceManager.getDefaultSharedPreferences(this);
		final boolean showAlert = sharedPref.getBoolean(Preferences.KEY_ALERT_ILLEGAL_MOVE, false);
		cardView.setIllegalMoveAlert(showAlert);
	}

	protected void onPrepareDialog(int id, Dialog dialog) {		
		super.onPrepareDialog(id, dialog);
	}
	
	private void showInvalidGameNumberPrompt() {
    	if(toastInvalidGameNumber == null) {
	    	String text = getString(R.string.prompt_invalid_game_number);
	    	text = MessageFormat.format(text, Integer.toString(1), Integer.toString(30000));
	        int duration = Toast.LENGTH_SHORT;
	        toastInvalidGameNumber = Toast.makeText(getApplicationContext(), text, duration);
    	}
    	toastInvalidGameNumber.show();
    }
    
    private void selectGameToPlay(int number, boolean validate) {
    	
    	if(!validate) {
    		//removeDialog(DIALOG_CHOOSE_GAME);
    		showDialog(DIALOG_CHOOSE_GAME);
    		return;
    	}
		if(!validateSeed(number)) {	
			removeDialog(DIALOG_CHOOSE_GAME);
			showInvalidGameNumberPrompt();
			showDialog(DIALOG_CHOOSE_GAME);
		} else {
			cardView.playSpecGame(number-1);
			setAppTitle(number);
		}			
    }

	
	public void onGameOver() {
		showDialog(DIALOG_GAME_OVER);
		
	}
	
	public void onMoveNotAllowed() {
		//showDialog(DIALOG_MOVE_NOT_ALLOWED);
		if(toastMoveNotAllowed == null) {		
			toastMoveNotAllowed = Toast.makeText(this, R.string.prompt_move_not_allowed, Toast.LENGTH_SHORT);
		}
		toastMoveNotAllowed.show();
	}
	
	public void onSuperMoveNotEnoughSpace(int countToMoved, int freeSpace) {
		superMoveNotEnoughSpaceMsg = MessageFormat.format(getString(R.string.prompt_supermove_not_enough_space), countToMoved, freeSpace);
		//showDialog(DIALOG_SUPERMOVE_NOT_ENOUGH_SPACE);		
	}
	
}