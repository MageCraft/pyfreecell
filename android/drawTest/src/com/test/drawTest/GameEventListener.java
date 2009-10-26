package com.test.drawTest;

public interface GameEventListener {
	abstract void onGameOver();
	abstract void onMoveNotAllowed();
	abstract void onSuperMoveNotEnoughSpace(int countToMoved, int freeSpace);
}
