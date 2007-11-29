#!/usr/bin/env python
# -*- coding: utf-8 -*-

from unit_world import UnitWorld
from block import create_block, destroy_block, BLOCK_KINDS
import random
from util import log

BLOCK_COLOR_KINDS = 6

#play state
(PLAY, PAUSE, STOP) = range(3)

class RS_Ctrl:
    def __init__(self, max_col, max_row):
        self.units = UnitWorld(max_col, max_row)
        self.state = STOP
        self.block = None
        self.rand = random.Random()

    def _clear(self):
        self.units.clear()

    def _new_block(self):
        if not block is None:
            destroy_block(block)
        block_type = self.rand.choice(range(BLOCK_KINDS))
        block_clr = self.rand.choice(range(BLOCK_COLOR_KINDS))
        log('block_type: %d, block_color: %d', block_type, block_clr)
        self.block = create_block( block_type, block_clr, self.units)

    def start(self):
        self._new_block()
        self.state = PLAY

    def pause(self):
        self.state = PAUSE

    def stop(self):
        self.state = STOP

    def set_level(level):
        pass

    def move_left(self):
        return block.left()

    def move_right(self):
        return block.right()

    def move_down(self):
        return block.down()

    def drop(self):
        return block.drop()

    def transform(self):
        return block.transform()
