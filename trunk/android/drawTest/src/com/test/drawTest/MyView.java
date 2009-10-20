package com.test.drawTest;

import android.view.View;

import android.content.Context;
import android.content.res.*;
import android.util.*;
import android.graphics.*;

import android.graphics.drawable.*;

import android.view.*;
import android.widget.*;
import android.view.View.OnTouchListener;

import java.util.*;


enum Area { Free, Home, Field }

class Card {
	private Drawable drawable;
	private int id;	
	private boolean selected;
	private Area area;
	
	public static final int width = 29;
	public static final int height = 38;
	
	public static final int Club = 3;
	public static final int Heart = 2;
	public static final int Diamond = 1;
	public static final int Spade = 0;
	
	public static final int ACE = 0;
	public static final int Jacky = 10;
	public static final int Queen = 11;
	public static final int King = 12;
	
	private static final float[] a1 = {-1,0,0,0,255,0,-1,0,0,255,0,0,-1,0,255,0,0,0,1,0};
	private static final ColorMatrixColorFilter colorFilter1 = new ColorMatrixColorFilter(new ColorMatrix(a1));
	
	private static final float[] a2 = {-1,0,0,0,255,0,0,0,0,255,0,0,0,0,255,0,0,0,1,0};
	private static final ColorMatrixColorFilter colorFilter2 = new ColorMatrixColorFilter(new ColorMatrix(a2));
	
	public Card(int id, Drawable drawable) {
		this.id = id;
		this.drawable = drawable;
		area = Area.Field;
	}
	
	public void setArea(Area area) {
		this.area = area;
	}
	public Area getArea() {
		return area;
	}
	
	public int getValue() {
		return id / 4;
	}
	
	public int getSuit() {
		return id % 4;
	}
	
	public boolean isBlack() {
		return getSuit() == Club || getSuit() == Spade;
	}
	
	public boolean isRed() {
		return getSuit() == Heart || getSuit() == Diamond;
	}
	
	public boolean isJQK() {
		return getValue() == Jacky || getValue() == Queen || getValue() == King; 
	}
	
	public boolean fitHome(Card dst) {
		if(dst == null) {
			return getValue() == ACE;
		}		
		return getSuit() == dst.getSuit() && getValue() == dst.getValue() + 1;		
	}
	
	public boolean fitField(Card dst) {
		if(dst == null)
			return true;
		return getValue() == dst.getValue() - 1 && isBlack() ^ dst.isBlack(); 
	}
	
	public void setSelected(boolean selected) {
		this.selected = selected;
	}
	
	public boolean getSelected() {
		return selected;
	}
	
	public void setPosition(int x, int y) {
		drawable.setBounds(x,y,x+drawable.getIntrinsicWidth(),y+drawable.getIntrinsicHeight());
	}
	
	public void draw(Canvas canvas) {
		if(selected) 			
			drawable.setColorFilter(isRed() ? colorFilter1 : colorFilter2);			
		else
			drawable.clearColorFilter();			
			
		drawable.draw(canvas);
	}
	
	public boolean contains(int x, int y) {
		return drawable.getBounds().contains(x,y);
	}
}

class FreeSlot {
	private Card card;
	private int x;
	private int y;
	
	public static final int width = Card.width + 2;
	public static final int height = Card.height + 2;
	
	public FreeSlot(int x, int y) {
		this.x = x;
		this.y = y;
	}
	
	public void setPostion(int x, int y) {
		this.x = x;
		this.y = y;
	}
	
	public boolean empty() {
		return card == null;
	}
	public void setCard(Card card) {
		this.card = card;
		card.setPosition(x, y);
		card.setArea(Area.Free);
	}
	public void setEmpty() {
		card = null;
	}
	
	public boolean contains(int x1, int y1) {
		return new Rect(x,y,x+width, y+height).contains(x1,y1);
	}
	
	public void draw(Canvas canvas) {
		Paint p = new Paint();
		p.setColor(Color.BLUE);
		MyUtil.drawRectFrame(canvas, new Rect(x,y,x+width,y+height), p);
		if(card!=null) 
			card.draw(canvas);
	}
}

class HomeSlot {
	public static final int width = FreeSlot.width;
	public static final int height = FreeSlot.height;
	private Stack<Card> cards;
	private int x;
	private int y;
	
	
	public HomeSlot(int x, int y) {
		this.x = x;
		this.y = y;
		cards = new Stack<Card>();
	}
	public void setPosition(int x, int y) {
		this.x = x;
		this.y = y;
	}
	
	public boolean contains(int x1, int y1) {
		return new Rect(x,y,x+width, y+height).contains(x1,y1);
	}
	
	public boolean empty() {
		return cards.isEmpty();
	}
	
	public void setEmpty() {
		cards.removeAllElements();
	}
	
	public void setCard(Card card) {
		cards.push(card);
		card.setPosition(x, y);
		card.setArea(Area.Home);
	}
	
	public Card pop() {
		if(!cards.empty())
			return cards.pop();
		else
			return null;		
	}
	
	public void draw(Canvas canvas) {
		Paint p = new Paint();
		p.setColor(Color.YELLOW);
		MyUtil.drawRectFrame(canvas, new Rect(x,y,x+width,y+height), p);
		if(!cards.isEmpty())
			cards.lastElement().draw(canvas);
	}
}

class FieldColumn {
	public static final int VERTICAL_GAP = 15;
	
	private Vector<Card> cards;
	private int x;
	private int y;
	
	public FieldColumn(int x, int y) {
		this.x = x;
		this.y = y;
		cards = new Vector<Card>();
	}
	
	public void push(Card card) {
		cards.add(card);
		int cardY = y + (cards.size()-1) * VERTICAL_GAP;
		card.setPosition(x, cardY);
		card.setArea(Area.Field);
	}
	
	public void setPostion(int x, int y) {
		this.x = x;
		this.y = y;
	}
	
	
	public void setEmpty() {
		cards.removeAllElements();
	}
	
	public Card pop() {
		return cards.isEmpty() ? null : cards.remove(cards.size()-1);
	}
	
	public boolean empty() {
		return cards.isEmpty();
	}
	
	public Card last() {
		return cards.isEmpty() ? null : cards.lastElement();
	}
	
	public void draw(Canvas canvas) {
		for(Card card:cards) {
			card.draw(canvas);
		}
	}
	
	public boolean contains(int x1, int y1) {
		if(empty()) return false;
		int h = (cards.size()-1) * VERTICAL_GAP + Card.height;
		Rect r = new Rect(x,y,x+Card.width,y+h);
		return r.contains(x1,y1);
	}
	
}

class MyUtil {
	public static void drawRectFrame(Canvas canvas, Rect r, Paint paint) {
		float[] pts = { r.left, r.top, r.right, r.top, 
						r.right, r.top,r.right, r.bottom, 
						r.right, r.bottom,r.left, r.bottom,
						r.left, r.bottom, r.left, r.top 
					  };
		canvas.drawLines(pts, paint);
		
	}
}

public class MyView extends View{
	
	private static final String LOG_TAG = "MyView";
	private static final int RES_BASE_ID = R.drawable.card00;
	
	public static final int HORIZONTAL_GAP = 8;
	public static final int DECK_SIZE=52;
	
	private Card[] cards;	
	private FreeSlot[] freeSlots;
	private HomeSlot[] homeSlots;
	private FieldColumn[] fieldColumns;
	private int[] deck;
	private int seed;
	
	private Card selectedCard;
	
	
	private void init() {
		cards = new Card[DECK_SIZE];		
		Resources res = getContext().getResources();	
		Drawable drawable;		
		for( int i = 0 ; i < DECK_SIZE ; i++) {			
			drawable = res.getDrawable(RES_BASE_ID+i);
			Card card = new Card(i,drawable);			
			cards[i] = card;
		}
		
		freeSlots = new FreeSlot[4];
		homeSlots = new HomeSlot[4];
		fieldColumns = new FieldColumn[8];
		deck = new int[DECK_SIZE];
		Random r = new Random();
		seed = r.nextInt(30000);
		shuffle();
		
		int idx = 0;
		int left = ( 320 - Card.width * 8 - HORIZONTAL_GAP * 7 ) / 2;
		int startX = left;
		
		int freeTop = 5;
		for( int i = 0 ; i < 4 ; i++) {
			freeSlots[i] = new FreeSlot(startX,freeTop);
			startX += FreeSlot.width;
		}
		startX += Card.width * 8 + HORIZONTAL_GAP * 7 - FreeSlot.width * 8;		
		for( int i = 0 ; i < 4 ; i++) {
			homeSlots[i] = new HomeSlot(startX,freeTop);
			startX += HomeSlot.width;
		}
		
		int fieldTop = freeTop + FreeSlot.height + 12;		
		startX = left;
		for(int col = 0 ; col < 4 ; col++) {
			fieldColumns[col] = new FieldColumn(startX,fieldTop);			
			startX += Card.width + HORIZONTAL_GAP;
			for(int row = 0 ; row < 7 ; row++) {
				fieldColumns[col].push(cards[deck[idx++]]);
			}
		}
		
		for(int col = 4; col < 8 ; col++) {
			fieldColumns[col] = new FieldColumn(startX,fieldTop);			
			startX += Card.width + HORIZONTAL_GAP;
			for(int row = 0 ; row < 6 ; row++) {
				fieldColumns[col].push(cards[deck[idx++]]);
			}
		}
		
	}
	
	
	
	private boolean hasSelectedCard() {
		return selectedCard != null;
	}
	
	private void shuffle() {
		int wLeft = 52;
	    int i = 0, j=0;
	    int[] d =  new int[52];
	    for (i = 0; i < 52; i++)      // put unique card in each deck loc.
	    	d[i] = i;

	    Random r = new Random(seed);
	    for (i = 0; i < 52; i++)
	    {	    	
	    	j = r.nextInt(wLeft);
	    	deck[i] = d[j];	    
	    	d[j] = d[--wLeft];	     
	    }
	}
	
	public MyView(Context context) {
		super(context);
		init();
	}
	
	public MyView(Context context, AttributeSet attrs) {
		super(context, attrs);
		init();
		
	}
	
	protected void onDraw(Canvas canvas) {
		for(FreeSlot slot:freeSlots) {
			slot.draw(canvas);
		}
		for(HomeSlot slot:homeSlots) {
			slot.draw(canvas);
		}
		for(FieldColumn column:fieldColumns) {
			column.draw(canvas);
		}
	}
	
	private void selectCard(Card card) {
		if(hasSelectedCard()) {
			
		}
	}
	
	private FreeSlot ifClickFreeSlots(int x, int y) {
		for(FreeSlot slot:freeSlots) {
			if(slot.contains(x, y))
				return slot;
		}
		return null;
	}
	
	private HomeSlot ifClickHomeSlots(int x, int y) {
		for(HomeSlot slot:homeSlots) {
			if(slot.contains(x, y))
				return slot;
		}
		return null;
	}
	
	private FieldColumn ifClickFields(int x, int y) {
		for(FieldColumn fieldColumn:fieldColumns) {
			if(fieldColumn.contains(x, y))
				return fieldColumn;
		}
		return null;
	}
	
	public boolean onTouchEvent(MotionEvent event) {
		//Log.i(LOG_TAG, "onTouchEvent, action: " + event.getAction());
		if(event.getAction() == MotionEvent.ACTION_UP) {
			int x = (int)event.getX();
			int y = (int)event.getY();
			HomeSlot clickHomeSlot = ifClickHomeSlots(x, y);
			FreeSlot clickFreeSlot = ifClickFreeSlots(x, y);
			FieldColumn clickFieldColumn = ifClickFields(x,y); 
			if( clickHomeSlot != null) {
				Log.i(LOG_TAG, "onTouchEvent, click home slots");
				
			}
			else if( clickFreeSlot != null) {
				Log.i(LOG_TAG, "onTouchEvent, click free slots");
				
			}
			else if( clickFieldColumn != null) {
				Log.i(LOG_TAG, "onTouchEvent, click fields");
			} else {
				Log.i(LOG_TAG, "onTouchEvent, click empty field");
			}			
			invalidate();			
		}
		return true;
	}
}