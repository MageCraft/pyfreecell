#!/usr/bin/env python
# -*- coding: utf-8 -*-

import operator
import unit_world
from util import log

#four style for every block
(S1, S2, S3, S4) = range(4)
(LEFT, RIGHT, BELOW) = range(3)
#block type
(I, Tian, T, L, L2, Z, Z2) = range(7)  
Block_Class_Map = { I    : I_Block,
                    Tian : Tian_Block,
                    T    : T_Block,
                    L    : L_Block,
                    L2   : L2_Block,
                    Z    : Z_Block,
                    Z2   : Z2_Block
                  }
Blocks = {} 

BLOCK_KINDS = len(Block_Class_Map)


def create_block(type, value, units):
    block = None
    if blocks.has_key(type):
        block = Blocks[type]
        block.set_value(value)
        block.appear()
    else:
        Class = Block_Class_Map[type]
        block = Class(value, units)
        Blocks[type] = block
    return block

def destroy_block(block):
    block.do_reset()
        
class Block:
    def __init__(self, units, value, style=S1, over=False):
        self.units = units
        self.v = value
        self.style = S1
        self.over = over
        self.pos = [ Pos() for i in range(4) ]
        self.move_action_map = { LEFT   : (lambda i: self.pos[i].left(),  self.move_left,  self.left_border_pos),
                                 RIGHT  : (lambda i: self.pos[i].right(), self.move_right, self.right_border_pos),
                                 DOWN   : (lambda i: self.pos[i].below(), self.move_down,  self.bottom_border_pos),
                               }
        self.init()

    def init(self):
        self._reset()
        self.appear()

    def appear(self):
        self._post_move()

    def transform(self):
       assert False

    def move(self, action):
        pos_func, move_func, border_pos = self.move_action_map[action]
        check_pos = map(pos_func, border_pos[self.style])
        if self.is_empty(*left_pos):
            move_func()
            over = False
        else:
            over = True
        return !over
        
    def left(self):
        log('left')
        return self.move(LEFT)

    def right(self):
        log('right')
        return self.move(RIGHT)

    def down(self): 
        log('down')
        return self.move(DOWN)

    def drop(self):
        log('drop')
        while self.down()
        return True

    def _reset(self):
        assert False

    def appear(self):
        self.post_move()

    def is_over(self):
        return self.over

    def do_reset(self):
        self._reset()
        self.over = false
        self.style = S1


    def _pre_move(self):
        for p in self.pos:
            self.units.set_empty(*p)
        
    def _post_move(self):
        for p in self.pos:
            self.units.set_value(self.v)

    def move_left(self):
        self._pre_move()
        for p in self.pos:
            p.x -= 1
        self._post_move()

    def move_right(self):
        self._pre_move():
            for p in self.pos:
                p.x += 1
        self._post_move()

    def move_down(self):
        self._pre_move():
            for p in self.pos:
                p.y += 1
        self._post_move()

    def is_empty(*pos_array):
        return reduce(operator.and_, [self.units.is_empty(*pos) for pos in pos_array])


#       0
#       1
#   0 1 2 3
#       3
class I_Block(Block):
    def init(self):
        Block.init(self)
        self.left_border_pos   = [ [0], range(4) ]
        self.right_border_pos  = [ [3], range(4) ]
        self.bottom_border_pos = [ range(4), [0] ]

    def _reset(self):
        #style1
        pos = self.pos
        pos[0].x = self.units.max_col/2 - 2 
        pos[0].y = 0
        pos[1] = pos[0].right()
        pos[2] = pos[1].right()
        pos[3] = pos[2].right()

    def transform(self):
        log('I_Block::transform()')
        pos = self.pos
        if self.style == S1: 
            #style1 -> style2
            #    x x x
            #    x x x
            #    0 1 2 3
            #        x x
            if self.is_empty(pos[0].above(), pos[1].above(), pos[2].above(), pos[2].below(), pos[0].above(2), pos[1].above(2), pos[2].above(2), pos[3].below()): 
                self._pre_move()
                pos[0] = pos[2].above(2)
                pos[1] = pos[2].above()
                pos[3] = pos[2].below()
                self._post_move()
                self.style = S2
                return True
        else: 
            #style2 -> style1
            #    x x 0 
            #    x x 1
            #    x x 2 x
            #        3 x
            if self.is_empty(pos[0].left(), pos[1].left(), pos[2].left(), pos[2].right(), pos[0].left(2), pos[1].left(2), pos[2].left(2), pos[3].right()):
                self._pre_move()
                pos[0] = pos[2].left(2)
                pos[1] = pos[2].left()
                pos[3] = pos[2].right()
                self._post_move()
                self.style = S1
                return True
        return False


#  0 3 
#  1 2
class Tian_Block(Block):
    def init(self):
        Block.init(self)
        self.left_border_pos    = [ [0,1] ]
        self.right_border_pos   = [ [2,3] ]
        self.bottom_border_pos  = [ [1,2] ]

    def _reset(self):
        pos = self.pos
        pos[0].x = self.units.max_col/2-1 
        pos[0].y = 0
        pos[1] = pos[0].below()
        pos[2] = pos[1].right()
        pos[3] = pos[2].above()

    def transform(self):
        log('Tian_Block::transform')
        pass

#  0 1 2 
#    3
class T_Block(Block):
    def init(self):
        Block.init(self)
        self.left_border_pos    = [ [0,3], [0,1,2], [3,2], [0,3,2] ]
        self.right_border_pos   = [ [2,3], [0,3,2], [0,3], [0,1,2] ]
        self.bottom_border_pos  = [ [0,3,2], [0,3], [2,1,0], [2,3] ]

    def _reset(self):
         #style1
         pos = self.pos
         pos[0].x = self.units.max_col/2-1 
         pos[0].y = 0
         pos[1] = pos[0].right()
         pos[2] = pos[1].right()
         pos[3] = pos[1].below()

    def transform(self):
        log("T_Block::transform()")
        pos = self.pos
    if self.style == S1: 
        #style1 -> style2
        #     x x   2
        #   0 1 2   1 3
        #   x 3 x   0
        if self.is_empty(pos[0].below(), pos[2].below(), pos[1].above(), pos[2].above()): 
            self._pre_move()
            pos[0] = pos[1].below()
            pos[2] = pos[1].above()
            pos[3] = pos[1].right()
            self._post_move()
            self.style = S2
            return True
    elif self.style == S2: 
         #style2 -> style3
         #x 2 x       3
         #x 1 3  -> 2 1 0
         #  0 x
        if self.is_empty(pos[0].right(), pos[2].right(), pos[1].left(), pos[2].left()): 
            self._pre_move()
            pos[0] = pos[1].right()
            pos[2] = pos[1].left()
            pos[3] = pos[1].above()
            self._post_move()
            self.style = S3
            return True
    elif self.style == S3: 
        # style3 -> style4
        # x 3 x         0
        # 2 1 0  ->   3 1
        # x x           2
        if self.is_empty(pos[0].above(), pos[2].above(), pos[1].below(), pos[2].below()): 
            self._pre_move()
            pos[0] = pos[1].above()
            pos[2] = pos[1].below()
            pos[3] = pos[1].left()
            self._post_move()
            self.style = S4
            return True
    else:
        #style4 -> style1
        # x 0         
        # 3 1 x  ->  0 1 2
        # x 2 x        3
        if self.is_empty(pos[0].left(), pos[2].left(), pos[1].right(), pos[2].right()): 
            self._pre_move()
            pos[0] = pos[1].left()
            pos[2] = pos[1].right()
            pos[3] = pos[1].below()
            self._post_move()
            style = S1
            return True
    return False

#
# 0 1 2
#     3
class L_Block(Block):
    def init(self):
        Block.init(self)
        self.left_border_pos    = [ [0,3], [0,1,2], [2,3], [0,1,3] ]
        self.right_border_pos   = [ [2,3], [0,1,3], [0,3], [0,1,2] ]
        self.bottom_border_pos  = [ [0,1,3], [0,3], [0,1,2], [2,3] ]

    def _reset(self):
        #style1
        pos = self.pos
        pos[0].x = self.units.max_col/2 - 2 
        pos[0].y = 1
        pos[1] = pos[0].right()
        pos[2] = pos[1].right()
        pos[3] = pos[2].below()

    def transform(self):
        log("L_Block::transform()");
        pos = self.pos
        if self.style == S1: 
            #style1 -> style2
            #     x x     2 3
            #   0 1 2     1
            #   x x 3     0
            if self.is_empty(pos[0].below(), pos[1].above(), pos[2].above(), pos[3].left()): 
                self._pre_move();
                pos[0] = pos[1].below();
                pos[2] = pos[1].above();
                pos[3] = pos[2].right();
                self._post_move();
                self.style = S2;
                return True
        elif self.style == S2: 
            #/*style2 -> style3
            #   x 2 3   3
            #   x 1 x   2 1 0
            #     0 x 
            if self.is_empty(pos[0].right(), pos[1].right(), pos[1].left(), pos[2].left()): 
                self._pre_move();
                pos[0] = pos[1].right();
                pos[2] = pos[1].left();
                pos[3] = pos[2].above();
                self._post_move();
                self.style = style3;
                return True
        elif self.style == S3: 
            # style3 -> style4
            #   3 x x     0
            #   2 1 0     1  
            #   x x     3 2
            if self.is_empty(pos[0].above(), pos[1].above(), pos[1].below(), pos[2].below()): 
                self._pre_move();
                pos[0] = pos[1].above();
                pos[2] = pos[1].below();
                pos[3] = pos[2].left();
                self._post_move();
                self.style = S4;
                return True
        else:
            # style3 -> style4
            #     x 0       
            #     x 1 x    0 1 2
            #     3 2 x        3
            if self.is_empty(pos[0].left(), pos[1].left(), pos[1].right(), pos[2].right()): 
                self._pre_move();
                pos[0] = pos[1].left();
                pos[2] = pos[1].right();
                pos[3] = pos[2].below();
                self._post_move();
                self.style = S1;
                return True
        return False

#
# 1 2 3
# 0
class L2_Block(Block):
    def init(self):
        Block.init(self)
        self.left_border_pos    = [ [0,1], [1,2,3], [0,3], [0,2,3] ]
        self.right_border_pos   = [ [0,3], [0,2,3], [0,1], [1,2,3] ]
        self.bottom_border_pos  = [ [0,2,3], [0,1], [1,2,3], [0,3] ]

    def _reset(self):
        #style1
        pos = self.pos
        pos[0].x = self.units.max_col/2-2 
        pos[0].y = 2
        pos[1] = pos[0].above()
        pos[2] = pos[1].right()
        pos[3] = pos[2].right()

    def transform(self):
        log("L2_Block::transform()")
        pos = self.pos
        if self.style == S1: 
            #style1 -> style2
            #     x x     3 
            #   1 2 3     2 
            #   0 x x     1 0 
            if self.is_empty(pos[0].right(), pos[2].above(), pos[3].above(), pos[3].below()): 
                self._pre_move()
                pos[1] = pos[2].below()
                pos[0] = pos[1].right()
                pos[3] = pos[2].above()
                self._post_move()
                self.style = S2
                return True
        elif self.style == S2: 
            #style2 -> style3
            #   x 3 x       0
            #   x 2 x   3 2 1
            #     1 0 
            if self.is_empty(pos[2].left(), pos[2].right(), pos[3].left(), pos[3].right()): 
                self._pre_move()
                pos[1] = pos[2].right()
                pos[0] = pos[1].above()
                pos[3] = pos[2].left()
                self._post_move()
                self.style = S3
                return True
        elif self.style == S3: 
            # style3 -> style4
            #   x x 0   0 1
            #   3 2 1     2  
            #   x x       3
            if self.is_empty(pos[2].above(), pos[3].above(), pos[2].below(), pos[3].below()): 
                self._pre_move()
                pos[1] = pos[2].above()
                pos[0] = pos[1].left()
                pos[3] = pos[2].below()
                self._post_move()
                self.style = S4
                return True
        else: 
            # style3 -> style4
            #     0 1       
            #     x 2 x    1 2 3
            #     x 3 x    0    
            if self.is_empty(pos[2].left(), pos[3].left(), pos[2].right(), pos[3].right()): 
                self._pre_move()
                pos[1] = pos[2].left()
                pos[0] = pos[1].below()
                pos[3] = pos[2].right()
                self._post_move()
                self.style = S1
                return True
        return False

# 0 1
#   2 3
class Z_Block(Block):
    def init(self):
        Block.init(self)
        self.left_border_pos    = [ [0,2], [0,1,3] ]
        self.right_border_pos   = [ [1,3], [0,2,3] ]
        self.bottom_border_pos  = [ [0,2,3], [0,2] ]

    def _reset(self):
        #style1
        pos = self.pos
        pos[0].x = self.units.max_col/2-1 
        pos[0].y = 0
        pos[1] = pos[0].right()
        pos[2] = pos[1].below()
        pos[3] = pos[2].right()

    def transform(self):
        log("Z_Block::transform()")
        pos = self.pos
        if self.style == S1: 
            #style1 -> style2
            #   0 1 x      3
            #   x 2 3    1 2
            #   x        0
            if self.is_empty(pos[0].below(), pos[0].below(2), pos[3].above()): 
                self._pre_move()
                pos[1] = pos[2].left()
                pos[0] = pos[1].below()
                pos[3] = pos[2].above()
                self._post_move()
                self.style = S2
                return True
        else: 
            #style2 -> style1
            #  x 3 x  0 1
            #  1 2 x    2 3
            #  0  
            if self.is_empty(pos[3].right(), pos[2].right(), pos[3].left()): 
                self._pre_move()
                pos[1] = pos[2].above()
                pos[0] = pos[1].left()
                pos[3] = pos[2].right()
                self._post_move()
                self.style = S1
                return True
        return False

#   2 3
# 0 1
class Z2_Block(Block):
    def init(self):
        Block.init(self)
        self.left_border_pos    = [ [0,2],[0,2,3] ]
        self.right_border_pos   = [ [1,3],[0,1,3] ]
        self.bottom_border_pos  = [ [0,1,3],[0,2] ]

    def _reset(self):
        #style1
        pos = self.pos
        pos[0].x = self.units.max_col/2-1 
        pos[0].y = 1
        pos[1] = pos[0].right()
        pos[2] = pos[1].above()
        pos[3] = pos[2].right()

    def transform(self):
        log("Z2_Block::transform()")
        pos = self.pos
        if self.style == S1: 
            #style1 -> style2
            #   x 2 3    3  
            #   0 1      2 1
            #   x x        0
            if self.is_empty(pos[0].below(), pos[1].below(), pos[0].above()): 
                self._pre_move()
                pos[0] = pos[1].below()
                pos[2] = pos[1].left()
                pos[3] = pos[2].above()
                self._post_move()
                self.style = S2
                return True
        else:
            #style2 -> style1
            #      3 x x    2 3
            #      2 1    0 1  
            #      x 0 
            if self.is_empty(pos[0].left(), pos[3].right(), pos[3].right(2)): 
                self._pre_move()
                pos[0] = pos[1].left()
                pos[2] = pos[1].above()
                pos[3] = pos[2].right()
                self._post_move()
                self.style = S1
                return True
        return False
