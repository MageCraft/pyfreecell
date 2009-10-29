package com.frankz.aFreeCell;

import android.view.View;

import android.content.Context;
import android.content.res.*;
import android.util.*;
import android.graphics.*;

import android.graphics.drawable.*;

import android.view.*;
//import android.widget.*;

import java.util.*;


enum Area { Free, Home, Field }


class Card {
	
	private Drawable drawable;
	private int id;	
	private boolean selected;
	private Area area;
	private CardOwner owner;
	public static final int width = 36;
	public static final int height = 48;
	
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
	
	public int getId() {
		return id;
	}
	
	public void setOwner(CardOwner owner) {
		this.owner = owner;
	}
	
	public CardOwner getOwner() {
		return owner;
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

class CardOwner {
	
}

class FreeSlot extends CardOwner {
	private Card card;
	private int x;
	private int y;
	
	public static final int width = Card.width;
	public static final int height = Card.height;
	
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
		card.setOwner(this);
	}
	public Card getCard() {
		return card;
	}
	public void setEmpty() {
		card = null;
	}
	
	public boolean contains(int x1, int y1) {
		return new Rect(x,y,x+width, y+height).contains(x1,y1);
	}
	
	public void draw(Canvas canvas) {		
		MyUtil.drawRectFrameWithShawdowColor(canvas, new Rect(x,y,x+width,y+height), 
				Color.BLACK, Color.GREEN);
		if(card!=null) 
			card.draw(canvas);
	}
}

class HomeSlot extends CardOwner {
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
		card.setOwner(this);
	}
	public Card getCard() {		
		return cards.isEmpty() ? null : cards.lastElement(); 
	}
	
	public Card pop() {
		if(!cards.empty())
			return cards.pop();
		else
			return null;		
	}
	
	public void draw(Canvas canvas) {		
		MyUtil.drawRectFrameWithShawdowColor(canvas, new Rect(x,y,x+width,y+height), 
				Color.BLACK, Color.GREEN);
		if(!cards.isEmpty())
			cards.lastElement().draw(canvas);
	}
}

class FieldColumn extends CardOwner {
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
		card.setOwner(this);
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
	
	public Vector<Card> getCards() {
		return cards;
	}
	
	public void draw(Canvas canvas) {
		for(Card card:cards) {
			card.draw(canvas);
		}
	}
	
	public boolean contains(int x1, int y1) {
		if(empty()) {
			return x1 >= x && x1 <= x+Card.width && y1 >= y;
		}
		int h = (cards.size()-1) * VERTICAL_GAP + Card.height;
		Rect r = new Rect(x,y,x+Card.width,y+h);
		return r.contains(x1,y1);
	}
	
}

class MyUtil {
	public static void drawRectFrame(Canvas canvas, Rect r, Paint paint) {
		float[] pts = { r.left, r.top, r.right-1, r.top, 
						r.right-1, r.top, r.right-1, r.bottom, 
						r.right, r.bottom-1, r.left, r.bottom-1,
						r.left, r.bottom-1, r.left, r.top 
					  };
		canvas.drawLines(pts, paint);		
	}
	
	public static void drawRectFrameWithShawdowColor(Canvas canvas, Rect r, int clr1, int clr2) {
		Paint p1 = new Paint();
		p1.setColor(clr1);
		Paint p2 = new Paint();
		p2.setColor(clr2);
		float[] pts1 = { 
				r.left, r.top, r.right-1, r.top,				
				r.left, r.bottom-1, r.left, r.top 
			  };
		float[] pts2 = {  
				r.right-1, r.top, r.right-1, r.bottom, 
				r.right, r.bottom-1, r.left, r.bottom-1,				 
			  };
		canvas.drawLines(pts1,p1);
		canvas.drawLines(pts2,p2);
	}
}

public class FreeCellView extends View{
	
	private static final int RES_BASE_ID = R.drawable.card00;
	
	public static final int HORIZONTAL_GAP = 3;
	public static final int DECK_SIZE = 52;
	public static final int GAME_MAX_SIZE = 30000;
	
	private Card[] cards;	
	private FreeSlot[] freeSlots;
	private HomeSlot[] homeSlots;
	private FieldColumn[] fieldColumns;
	private int[] deck;
	private int seed;	
	private Card selectedCard; 
	private State state;
	private Drawable flag;
	private GameEventListener gameEventListener;	
	private Vector<MoveStepT> moveSteps;
	private boolean illegalMoveAlert;
	
	private final MyLog log = new MyLog("MyView");
	
	public enum State { Idle, Playing }
	
	enum MoveType { SuperMove, NormalMove, Undo, AutoPlay, SuperMoveBegin, SuperMoveEnd }
	
	abstract class MoveFunction {				
		abstract void call(FreeCellView funcOwner, CardOwner src, CardOwner dst, MoveType moveType);
	}
	
	class MoveFunc_free2field extends MoveFunction {		
		public void call(FreeCellView funcOwner, CardOwner src, CardOwner dst, MoveType moveType) {
			funcOwner.free2field((FreeSlot)src, (FieldColumn)dst, moveType, false);
		}
	}
	
	class MoveFunc_field2field extends MoveFunction {
		public void call(FreeCellView funcOwner, CardOwner src, CardOwner dst, MoveType moveType) {
			funcOwner.field2field((FieldColumn)src, (FieldColumn)dst, moveType);
		}
	}
	
	class MoveFunc_field2free extends MoveFunction {
		public void call(FreeCellView funcOwner, CardOwner src, CardOwner dst, MoveType moveType) {
			funcOwner.field2free((FieldColumn)src, (FreeSlot)dst, moveType);
		}
	}
	
	class MoveFunc_move2home extends MoveFunction {
		public void call(FreeCellView funcOwner, CardOwner src, CardOwner dst, MoveType moveType) {
			funcOwner.move2Home(src, (HomeSlot)dst, false, false);
		}
	}
	
	class MoveFunc_moveFromHome extends MoveFunction {
		public void call(FreeCellView funcOwner, CardOwner src, CardOwner dst, MoveType moveType) {
			funcOwner.moveFromHome((HomeSlot)src, dst);
		}
	}
	
	private MoveFunction moveFuncFactory(CardOwner src, CardOwner dst) {
		MoveFunction func = null;
		if(src instanceof FreeSlot && dst instanceof FieldColumn)
			func = new MoveFunc_free2field();
		else if(src instanceof FieldColumn && dst instanceof FieldColumn)
			func = new MoveFunc_field2field();
		else if(src instanceof FieldColumn && dst instanceof FreeSlot)
			func = new MoveFunc_field2free();
		else if(dst instanceof HomeSlot) 
			func = new MoveFunc_move2home();
		else if(src instanceof HomeSlot)
			func = new MoveFunc_moveFromHome();		
		return func;
	}
	
	class MoveStep {
		public final CardOwner src;
		public final CardOwner dst;
		public MoveStep(CardOwner src, CardOwner dst) {
			this.src = src;
			this.dst = dst;
		}
	}
	
	class MoveStepT extends MoveStep{
		public final MoveType moveType;
		public MoveStepT(MoveType moveType, CardOwner src, CardOwner dst) {
			super(src, dst);
			this.moveType = moveType;
		}
	}
	
	public void setGameEventListener(GameEventListener listener) {
		gameEventListener = listener;
	}
	
	private void init() {
		cards = new Card[DECK_SIZE];		
		Resources res = getContext().getResources();	
		Drawable drawable;		
		for( int i = 0 ; i < DECK_SIZE ; i++) {			
			drawable = res.getDrawable(RES_BASE_ID+i);
			Card card = new Card(i,drawable);			
			cards[i] = card;
		}
		flag = res.getDrawable(R.drawable.flag);		
		
		freeSlots = new FreeSlot[4];
		homeSlots = new HomeSlot[4];
		fieldColumns = new FieldColumn[8];
		deck = new int[DECK_SIZE];			
		
		int left = ( 320 - Card.width * 8 - HORIZONTAL_GAP * 7 ) / 2;
		int startX = left;
		
		int freeTop = 5;
		for( int i = 0 ; i < 4 ; i++) {
			freeSlots[i] = new FreeSlot(startX,freeTop);
			startX += FreeSlot.width;
		}
		int gap = Card.width * 8 + HORIZONTAL_GAP * 7 - FreeSlot.width * 8;
		int flagX = startX + (gap-flag.getIntrinsicWidth())/2;
		int flagY = freeTop + (FreeSlot.height - flag.getIntrinsicHeight())/2;
		Rect flagR = new Rect(flagX, flagY, flagX+flag.getIntrinsicWidth(), flagY+flag.getIntrinsicHeight());
		flag.setBounds(flagR);
		
		startX += gap;		
		for( int i = 0 ; i < 4 ; i++) {
			homeSlots[i] = new HomeSlot(startX,freeTop);
			startX += HomeSlot.width;
		}
		
		int fieldTop = freeTop + FreeSlot.height + 12;		
		startX = left;
		for(int col = 0 ; col < 8 ; col++) {
			fieldColumns[col] = new FieldColumn(startX,fieldTop);			
			startX += Card.width + HORIZONTAL_GAP;
		}	
		seed = -1;
		state = State.Idle;
		moveSteps = new Vector<MoveStepT>();
	}
	public int getSeed() {
		return seed;
	}
	public State getState() {
		return state;
	}
	public boolean isUndoEnabled() {
		return !moveSteps.isEmpty();
	}
	public void setIllegalMoveAlert(boolean showAlert) {
		illegalMoveAlert = showAlert;
	}
	
	public int playNewGame() {
		Random r = new Random();
		seed = r.nextInt(30000);
		playGame();
		return seed;
	}
	
	public void replayGame() {
		playGame();//with current seed
	}
	
	public void playSpecGame(int seed) {
		this.seed = seed;
		playGame();
	}
	
	public void playSavedGame(int seed, 
			String freeSlotsSavedString, String homeSlotsSavedString, String fieldColumnsSavedString) {
		this.seed = seed;
		state = State.Playing;
		shuffle();
		freeSlotsLoadFromString(freeSlotsSavedString);
		homeSlotsLoadFromString(homeSlotsSavedString);
		fieldColumnsFromString(fieldColumnsSavedString);
		invalidate();		
	}
	
	
	//return true means can contiune undo
	public void undo() {
		boolean moved = false;
		while(!moveSteps.isEmpty()) {
			MoveStepT lastStep = moveSteps.lastElement();
			MoveType moveType = lastStep.moveType;
			CardOwner src = lastStep.src;
			CardOwner dst = lastStep.dst;
			boolean go = false;
			if(moveType == MoveType.AutoPlay || moveType == MoveType.SuperMove)
				go = true;
			if(moveType == MoveType.SuperMoveEnd) {
				moveSteps.remove(lastStep);
				continue;
			}
			if(moveType == MoveType.SuperMoveBegin) {
				moveSteps.remove(lastStep);
				break;
			}
			MoveFunction mvFunc = moveFuncFactory(dst, src);
			mvFunc.call(this, dst, src, MoveType.Undo);
			moveSteps.remove(lastStep);	
			moved = true;
			if(!go) break;
		}
		if(moved) {
			invalidate();			
		}
	}
	
	private void playGame() {
		state = State.Playing;
		shuffle();
		cleanup();
		int idx = 0;
		for(int col = 0 ; col < 4 ; col++) {			
			for(int row = 0 ; row < 7 ; row++) {
				fieldColumns[col].push(cards[deck[idx++]]);
			}
		}		
		for(int col = 4; col < 8 ; col++) {			
			for(int row = 0 ; row < 6 ; row++) {
				fieldColumns[col].push(cards[deck[idx++]]);
			}
		}
		invalidate();
	}
	
	private void cleanup() {
		for(FreeSlot slot:freeSlots) 
			slot.setEmpty();
		for(HomeSlot slot:homeSlots) 
			slot.setEmpty();
		for(FieldColumn col:fieldColumns)
			col.setEmpty();
		moveSteps.removeAllElements();
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
	
	public FreeCellView(Context context) {
		super(context);
		init();
	}
	
	public FreeCellView(Context context, AttributeSet attrs) {
		super(context, attrs);
		init();
		
	}
	
	protected void onDraw(Canvas canvas) {
		for(FreeSlot slot:freeSlots) {
			slot.draw(canvas);			
		}
		
		//flag.draw(canvas);
		
		for(HomeSlot slot:homeSlots) {
			slot.draw(canvas);
		}
		
		for(FieldColumn column:fieldColumns) {
			column.draw(canvas);
		}
		
	}
	
	private Vector<FreeSlot> getEmptyFreeSlots() {
		Vector<FreeSlot> slots = new Vector<FreeSlot>();
		for(FreeSlot slot:freeSlots) {
			if(slot.empty())
				slots.add(slot);
		}
		return slots;
	}
	
	private Vector<FieldColumn> getEmptyFieldColumns(FieldColumn dst) {
		Vector<FieldColumn> cols = new Vector<FieldColumn>();
		for(FieldColumn col:fieldColumns) {
			if(col.empty() && col != dst)
				cols.add(col);
		}
		return cols;
	}
	
	private int getSuperMoveMax(Vector<FreeSlot> slots, Vector<FieldColumn> cols) {
		int m = slots.size();
		int n = cols.size();
		return (n+1)*(2*m+n)/2 + 1;
	}
	
	//used in normal move and super, undo 
	private boolean move2Free(CardOwner src, FreeSlot dst, boolean disableAuto, MoveType moveType) {
		//if src is HomeSlot, should return false
		if(src instanceof FreeSlot)
			return false;
		//if dst is null, will find the empty slot automaticlly, for double click field cards cases
		boolean auto = false;
		if(src instanceof FieldColumn) {
			//field ==> free
			FieldColumn srcCol = (FieldColumn)src;
			dst.setCard(srcCol.last());
			srcCol.pop();
			recordStep(moveType, src, dst);
			auto = true;		
		}
		if(src instanceof FreeSlot) {
			//free => free
			FreeSlot srcSlot = (FreeSlot)src;
			if(src != dst) {
				dst.setCard(srcSlot.getCard());
				srcSlot.setEmpty();
				recordStep(moveType, src, dst);
			}
		}
		emptySelectedCard();
		if( auto && !disableAuto) {
			//auto play
			autoPlay();
		}
		return true;
	}
	
	private boolean field2free(FieldColumn src, FreeSlot dst, MoveType moveType) {
		return move2Free(src, dst, true, moveType);
	}
	
	private void field2field(FieldColumn src, FieldColumn dst, MoveType moveType) {
		dst.push(src.last());
		src.pop();
		recordStep(moveType,src,dst);
	}
	//used in normal move and super move, undo
	private boolean free2field(FreeSlot src, FieldColumn dst, MoveType moveType, boolean test) {
		if( src.getCard().fitField(dst.last()) || moveType == MoveType.Undo ) {
			if(test)
				return true;
			dst.push(src.getCard());
			src.setEmpty();
			emptySelectedCard();
			recordStep(moveType, src, dst);
			return true;
		}
		return false;
	}
	
	//only used in undo
	private void moveFromHome(HomeSlot src, CardOwner dst) {
		if(dst instanceof FieldColumn)
			((FieldColumn)dst).push(src.getCard());
		if(dst instanceof FreeSlot)
			((FreeSlot)dst).setCard(src.getCard());
		src.pop();
		//notify left card
	}
	
	//used in normal move and auto play
	private boolean move2Home(CardOwner src, HomeSlot dst, boolean autoPlay, boolean test) {
		boolean moved = false;
		MoveType moveType = autoPlay ? MoveType.AutoPlay : MoveType.NormalMove;
		if(src instanceof FieldColumn) {
			FieldColumn srcCol = (FieldColumn)src;
			//field => home
			if(srcCol.last().fitHome(dst.getCard())) {
				if(test) return true;
				dst.setCard(srcCol.last());
				srcCol.pop();
				recordStep(moveType, src, dst);
				moved = true;			
			}		
		}
		if(src instanceof FreeSlot) {
			//free => home
			FreeSlot srcSlot = (FreeSlot)src;
			if(srcSlot.getCard().fitHome(dst.getCard())) {
				if(test) return true;
				dst.setCard(srcSlot.getCard());
				srcSlot.setEmpty();
				recordStep(moveType, src, dst);
				moved = true;
			}
		}
		if(moved) {
			//notify left card
			return true;
		}
		return false;
	}
	
	private void superMovePack(Vector<FreeSlot> emptySlots, Vector<FieldColumn> emptyColumns, 
			FieldColumn src, Card end, Vector<MoveStep> stack) {
		if(src.empty() || src.last() == end)
			return;
		//move cards to free slot at first
		for(FreeSlot slot:emptySlots) {
			field2free(src, slot, MoveType.SuperMove);
			stack.add(0,new MoveStep(src,slot));
			if(src.empty() || src.last() == end)
				return;				
		}
		//move cards to empty field from left to right
		for(FieldColumn col:emptyColumns) {
			field2field(src, col, MoveType.SuperMove);
			stack.add(0,new MoveStep(src,col));
			if(src.empty() || src.last() == end)
				return;	
		}
		//move cards from (n-2),(n-3)....,0 to n-1 field col
		for(int i = emptyColumns.size()-2 ; i >= 0 ; i--) {
			field2field(emptyColumns.get(i), emptyColumns.lastElement(), MoveType.SuperMove);
			stack.add(0,new MoveStep(emptyColumns.get(i), emptyColumns.lastElement()));
		}
		//move card from free to field, from right to left
		for(int i = emptySlots.size()-1 ; i >= 0 ; i--) {
			free2field(emptySlots.get(i), emptyColumns.lastElement(),MoveType.SuperMove, false);
			stack.add(0, new MoveStep(emptySlots.get(i), emptyColumns.lastElement()));
		}
		
		emptyColumns.remove(emptyColumns.lastElement()); //remove last
		//call me again
		superMovePack(emptySlots, emptyColumns, src, end, stack);		
	}
	
	private void superMoveUnPack(Vector<MoveStep> stack, FieldColumn oldSrcCol, FieldColumn newSrcCol) {
		for(MoveStep step:stack) {
			CardOwner src = step.src;
			CardOwner dst = step.dst;
			if(src instanceof FieldColumn && src == oldSrcCol)
				src = newSrcCol;
			MoveFunction moveFunc = moveFuncFactory(dst, src);
			moveFunc.call(this, dst, src, MoveType.SuperMove);			
		}
	}
	
	private boolean superMove(FieldColumn src, FieldColumn dst, boolean test) {
		Vector<FreeSlot> emptyFree = getEmptyFreeSlots();
		Vector<FieldColumn> emptyCol = getEmptyFieldColumns(dst);
		int max = getSuperMoveMax(emptyFree,emptyCol);
		Vector<Card> series = new Vector<Card>();
		Card dstCard = dst.empty() ? null : dst.last();
		Vector<Card> srcCards = src.getCards();
		for(int row = srcCards.size()-1 ; row >= 0; row--) {
			series.add(0,srcCards.get(row));
			if(row-1<0 ||
					!srcCards.get(row).fitField(srcCards.get(row-1)) ||
					dstCard != null && srcCards.get(row).fitField(dstCard) ||
					series.size() == max) 
						break;					
		}
		Card srcCard = series.firstElement();
		if(!srcCard.fitField(dstCard))
			return false;
		if(test)
			return true;
		
		if(dst.empty() && series.size() > 1) {
			//if super move to empty column, need alert user if move column or single card
			//defer it, always move entire column
		}
		emptySelectedCard();
		Vector<MoveStep> stack = new Vector<MoveStep>();
		MoveStepT stepSuperMoveBegin = recordStep(MoveType.SuperMoveBegin,null,null);
		superMovePack(emptyFree, emptyCol, src, srcCard, stack);
		if(stack.isEmpty()) {
			moveSteps.remove(stepSuperMoveBegin);//not super move 
			field2field(src, dst, MoveType.NormalMove);
		} else {
			field2field(src, dst, MoveType.SuperMove);
			superMoveUnPack(stack, src, dst);
			recordStep(MoveType.SuperMoveEnd,null,null);
		}	
		return true;
	}
	
	private boolean move2Field(CardOwner src, FieldColumn dst, boolean test) {
		if(src instanceof FieldColumn) {
			FieldColumn srcCol = (FieldColumn)src;
			if(srcCol == dst) {
				log.i("select same field column");
				emptySelectedCard();
				return true;//not alert user
			}
			//super move
			if(superMove(srcCol,dst,test)) {
				if(!test)
					autoPlay();				
				return true;
			}
		}		
		if(src instanceof FreeSlot) {
			FreeSlot srcSlot = (FreeSlot)src;
			return free2field(srcSlot, dst, MoveType.NormalMove, test);
		}		
		return false;
	}
	
	private boolean isSafeAutoPlay(Card card) {
		if(card.getValue() == Card.ACE || card.getValue() == 1)
			return true; //A or 2
		int count = 0;
		for(HomeSlot slot:homeSlots) {
			if(!slot.empty()) {
				Card card1 = slot.getCard();
				if( (card1.isBlack() ^ card.isBlack()) && (card1.getValue() >= card.getValue()-1) ) {
					count += 1;
				}
			}
		}
		return count == 2;	
	}
	
	private void autoPlay() {
		//scan every last card in field col and free, check if fit home
		boolean auto = false;
		//scan every card in free slot, check if it fit home and safe to do auto play
		for(FreeSlot src:freeSlots) {
			if(src.empty()) continue;
			for(HomeSlot dst:homeSlots) {
				if(src.getCard().fitHome(dst.getCard()) && isSafeAutoPlay(src.getCard())) {
					move2Home(src,dst,true,false);//auto play
					auto = true;
					break;		
				}
			}
		}
		//scan every last card in field column, check if it fit home and safe to auto play
		for(FieldColumn src:fieldColumns) {
			if(src.empty()) continue;
			for(HomeSlot dst:homeSlots) {
				if(src.last().fitHome(dst.getCard()) && isSafeAutoPlay(src.last()) ) {
					move2Home(src, dst, true, false);//auto play
					auto = true;
					break;
				}
			}
		}
		//keep call me until auto is false;
		if(auto) {
			autoPlay();
		}

	}
	
	private void emptySelectedCard() {
		if(hasSelectedCard()) {
			selectedCard.setSelected(false);
			selectedCard = null;
		}
	}
	
	private void selectCard(Card card) {
		if(hasSelectedCard())
			selectedCard.setSelected(false);		
		card.setSelected(true);
		selectedCard = card;		
	}
	
	private boolean clickFreeSlots(int x, int y) {
		FreeSlot clickedSlot = null;
		for(FreeSlot slot:freeSlots) {
			if(slot.contains(x, y)) {
				clickedSlot = slot;
				break;
			}
				
		}
		if( clickedSlot == null ) {
			return false;
		}
		//select card in free slot
	    //1. no select before, just highlight it
	    //2. selected card before
	    //   a. card in free ==> card in free, just switch highlight
	    //   b. card in field ==> card in free, just switch highlight
		if(!hasSelectedCard()) {
			if(clickedSlot.empty()) 
				log.i("clicked the empty free slot");				
			else 
				selectCard(clickedSlot.getCard());
		} else {
			if(!clickedSlot.empty()) {
				if(selectedCard == clickedSlot.getCard()) {
					log.i("select same card in free slot again");
					emptySelectedCard();
				}
				else {
					alertUserAboutIllegalMove();//alert user
				}
				return true;
			} else 
				move2Free(selectedCard.getOwner(), clickedSlot, false, MoveType.NormalMove);			
		}	
		checkGameOver();		
		return true;		
	}
	
	private boolean clickHomeSlots(int x, int y) {
		HomeSlot clickedSlot = null;
		for(HomeSlot slot:homeSlots) {
			if(slot.contains(x, y)) {
				clickedSlot = slot;
				break;
			}
		}
		if(clickedSlot == null) {
			return false;
		}
		if(!move2Home(selectedCard.getOwner(), clickedSlot, false, false)) {
			alertUserAboutIllegalMove();//alert user
			return true;
		}
		emptySelectedCard();
		autoPlay();
		checkGameOver();		
		return true;
	}
	
	
	private boolean clickFieldColumns(int x, int y) {
		FieldColumn clickedColumn = null;
		for(FieldColumn fieldColumn:fieldColumns) {
			if(fieldColumn.contains(x, y)) {
				clickedColumn = fieldColumn;
				break;
			}
		}
		if(clickedColumn == null) {
			//1. doesn't click field column
			//2. click a empty column
			return false;
		}
		if(!hasSelectedCard()) {
			//1. no select before, just highlight the column's last card	
			if(clickedColumn.empty()) {
				log.i("select empty column");				
			} else {
				Card card = clickedColumn.last();
				selectCard(card);
			}
		} else {
			//2. selected before
		    //   a. card in free ==> card in field, if fit, move to it, or, do nothing
		    //   b. card in field ==> card in field
			if(!move2Field(selectedCard.getOwner(), clickedColumn, false)) {
				alertUserAboutIllegalMove();//alert user
				return true;
			}
			
		}
		checkGameOver();		
		return true;
		
	}
	
	private void alertUserAboutIllegalMove() {
		if(illegalMoveAlert) {
			if(gameEventListener!=null) {
				gameEventListener.onMoveNotAllowed();
				emptySelectedCard();
			}
		}
	}
	
	private void checkGameOver() {
		if(getLeftCardCount() == 0) {
			//game over
			if(gameEventListener != null)
				gameEventListener.onGameOver();
		}			
	}
	
	public String freeSlotsSave2String() {
		String str = "";
		for(FreeSlot slot:freeSlots) {
			str += slot.empty() ? "-1" : slot.getCard().getId();
			str += ",";
		}
		return str;	
	}
	
	public boolean freeSlotsLoadFromString(String savedString) {
		String[] array = savedString.split(",");		
		if(array.length != 4) return false;
		for(int i = 0 ; i < array.length ; i++)
		{
			try {
				int id = Integer.parseInt(array[i]);
				if(id != -1) 
					freeSlots[i].setCard(cards[id]);				
			} catch (NumberFormatException e) {
				return false;
			}
		}
		return true;			
	}
	
	public String homeSlotsSave2String() {
		String str = "";
		for(HomeSlot slot:homeSlots) {
			str += slot.empty() ? "-1" : slot.getCard().getId();
			str += ",";
		}
		return str;
	}
	
	public boolean homeSlotsLoadFromString(String savedString) {
		String[] array = savedString.split(",");		
		if(array.length != 4) return false;
		for(int i = 0 ; i < array.length ; i++)
		{
			try {
				int id = Integer.parseInt(array[i]);	
				if(id != -1)
					homeSlots[i].setCard(cards[id]);
			} catch (NumberFormatException e) {
				return false;
			}
		}
		return true;
	}
	
	public String fieldColumnsSave2String() {
		String str = "";
		for(FieldColumn col:fieldColumns) {			
			for(Card card:col.getCards()) {
				str += card.getId();
				str += ",";
			}
			str += 	"#";			
		}
		return str;
	}
	
	public boolean fieldColumnsFromString(String savedString) {
		String[] cols = savedString.split("#");
		if(cols.length != 8) return false;
		for(int i = 0 ; i < cols.length ; i++) {
			if(cols[i].equals("")) 
				continue;
			String[] colCards = cols[i].split(",");
			for(int j = 0 ; j < colCards.length ; j++) {
				try {
					int id = Integer.parseInt(colCards[j]);
					fieldColumns[i].push(cards[id]);
				} catch(NumberFormatException e) {
					return false;
				}
			}
		}		
		return true;
	}
	
	public int getLeftCardCount() {
		int count = 0;
		for(FreeSlot slot:freeSlots) {
			if(!slot.empty())
				count++;
		}
		for(FieldColumn col:fieldColumns)
			count += col.getCards().size();
		log.i("getLeftCardCount, left card is "+count);
		return count;
	}
	
	public boolean onTouchEvent(MotionEvent event) {
		//Log.i(LOG_TAG, "onTouchEvent, action: " + event.getAction());
		if(event.getAction() == MotionEvent.ACTION_UP) {
			int x = (int)event.getX();
			int y = (int)event.getY();			 
			if(clickHomeSlots(x,y)) {
				log.i("onTouchEvent, click home slots");
				
			}
			else if(clickFreeSlots(x,y) ) {
				log.i("onTouchEvent, click free slots");
				
			}
			else if(clickFieldColumns(x,y)) {
				log.i("onTouchEvent, click fields");
			} else {
				log.i("onTouchEvent, click empty field");
			}			
			invalidate();			
		}
		return true;
	}
	
	private MoveStepT recordStep(MoveType moveType, CardOwner src, CardOwner dst) {
		MoveStepT moveStep = null;
		if(moveType != MoveType.Undo) {
			moveStep = new MoveStepT(moveType,src,dst);
			moveSteps.add(moveStep);
		}
		return moveStep;
	}
}
