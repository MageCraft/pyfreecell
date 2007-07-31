#!/usr/bin/env python

import random
import sys

#suit
(
 Club, 
 Heart,
 Diamond, 
 Spade
) = range(4)

ACE = 0

#area
(
 IDLE, 
 FREE, 
 HOME, 
 FIELD
) = range(4)

suit = lambda card: card % 4
value = lambda card: card / 4
is_black = lambda card: suit(card) == Club or suit(card) == Spade
is_red = lambda card: suit(card) == Diamond or suit(card) == Heart

EMPTY = -1
def is_empty(v):
    if type(v) == list: 
        return len(v) == 0
    elif type(v) == int:
        return v is EMPTY
    else:
        assert( False )

def not_empty(v):
    return not is_empty(v)

DECK_SIZE=52
RAND_MAX = sys.maxint

def fit_home(dst,src):
    if dst == EMPTY:
        return value(src) == ACE
    return suit(src) == suit(dst) and value(src) == value(dst)+1

def fit_field(dst,src):
    if dst == EMPTY:
        return True;
    return value(src) == value(dst)-1 and (is_black(src) ^ is_black(dst))

def shuffle(seed, cards):
    random.seed(seed)
    deck = range(0,DECK_SIZE)
    left = DECK_SIZE 
    for i in range(DECK_SIZE):
        k = random.randrange(0, RAND_MAX) % left
        cards[i%8][i/8]= deck[k]
        left -= 1
        deck[k] = deck[left]



