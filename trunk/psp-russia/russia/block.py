#!/usr/bin/env python
# -*- coding: utf-8 -*-

import operator
import unit_world
from util import log

#four style for every block
(S1, S2, S3, S4) = range(4)
(LEFT, RIGHT, BELOW) = range(3)
#block type
(I, Tian, T, L, L2, Z, Z2) = range(7);  
Block_Class_Map = { I    : I_Block,
                    Tian : Tian_Block,
                    T    : T_Block,
                    L    : L_Block,
                    L2   : L2_Block,
                    Z    : Z_Block,
                    Z2   : Z2_Block
                  }
Blocks = {} 

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
        
class Block:
    def __init__(self, units, value, style=S1, over=False):
        self.units = units
        self.v = value
        self.style = S1
        self.over = over
        self.pos = [ Pos() for i in range(4) ]
        self.move_action_map = { LEFT   : (lambda i: self.pos[i].left(), self.move_left, self.left_border_pos),
                                 RIGHT  : (lambda i: self.pos[i].right(), self.move_right, self.right_border_pos),
                                 DOWN   : (lambda i: self.pos[i].below(), self.move_right, self.bottom_border_pos),
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
        self.over = false;
        self.s = S1


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



I_Block::I_Block(UnitWorld& units, int val)
    : Block(units,val)
{
    reset();
    postMove();
}
I_Block::~I_Block()
{

}
void I_Block::reset()
{
    //style1
    pos[0].x = units.getMaxCol()/2 - 2; pos[0].y = 1;
    pos[1] = pos[0].right();
    pos[2] = pos[1].right();
    pos[3] = pos[2].right();
}

int I_Block::transform()
{
    qDebug("I_Block::transform()");
    if( style == style1 )
    {/*style1 -> style2
        x x x
        x x x
        0 1 2 3
            x x
     */
        if( !isEmpty(pos[0].up(), pos[1].up(), pos[2].up(), pos[2].down()) ||
            !isEmpty(pos[0].up(2), pos[1].up(2), pos[2].up(2), pos[3].down()) )
        {
            return -1;
        }
        preMove();
        pos[0] = pos[2].up(2);
        pos[1] = pos[2].up();
        pos[3] = pos[2].down();
        postMove();
        style = style2;
        return 0;
    }
    else 
    {/*style2 -> style1
        x x 0 
        x x 1
        x x 2 x
            3 x
    */
        if( !isEmpty(pos[0].left(), pos[1].left(), pos[2].left(), pos[2].right()) ||
            !isEmpty(pos[0].left(2), pos[1].left(2), pos[2].left(2), pos[3].right()) )
        {
            return -1;
        }
        preMove();
        pos[0] = pos[2].left(2);
        pos[1] = pos[2].left();
        pos[3] = pos[2].right();
        postMove();
        style = style1;
        return 0;
    }

    return 0;
}
int I_Block::left()   
{
    qDebug("I_Block::left()");

    if( style == style1 )
    {
        if( !isEmpty(pos[0].left()) )
            return -1;
    }
    else 
    {//style2

        if( !isEmpty(pos[0].left(), pos[1].left(), pos[2].left(), pos[3].left()) )
            return -1;
    }

    moveLeft();
    return 0;
}

int I_Block::right() 
{
    qDebug("I_Block::right()");

    if( style == style1 )
    {
        if( !isEmpty(pos[3].right()) )
            return -1;
    }
    else 
    {//style2
        if( !isEmpty(pos[0].right(), pos[1].right(), pos[2].right(), pos[3].right()) )

            return -1;
    }

    moveRight();
    return 0;
}

int I_Block::down() 
{
    qDebug("I_Block::down()");

    if( style == style2 )
    {
        if( !isEmpty(pos[3].down()) )
        {
            over = true;
            return -1;
        }
    }
    else 
    {//style1
        if( !isEmpty(pos[0].down(), pos[1].down(), pos[2].down(), pos[3].down()) )
        {
            over = true;
            return -1;
        }
    }

    moveDown();
    over = false;
    return 0;
}

#       0
#       1
#   0 1 2 3
#       3
class I_Block(Block):
    def init(self):
        Block.init(self)
        self.left_border_pos   = { STYLE1: [0], STYLE2: range(4) }
        self.right_border_pos  = { STYLE1: [3], STYLE2: range(4) }
        self.bottom_border_pos = { STYLE1: range(4), STYLE2: [0] }

    def transform(self):
    log('I_Block::transform()');
    pos = self.pos
    if self.style == S1: 
        #style1 -> style2
        #    x x x
        #    x x x
        #    0 1 2 3
        #        x x
        if self.is_empty(pos[0].above(), pos[1].above(), pos[2].above(), pos[2].below(), pos[0].above(2), pos[1].above(2), pos[2].above(2), pos[3].below()): 
            self._pre_move();
            pos[0] = pos[2].up(2);
            pos[1] = pos[2].up();
            pos[3] = pos[2].down();
            self._post_move();
            self.style = S2;
            return True;
    else: 
    #style2 -> style1
    #    x x 0 
    #    x x 1
    #    x x 2 x
    #        3 x
        if( !isEmpty(pos[0].left(), pos[1].left(), pos[2].left(), pos[2].right()) ||
            !isEmpty(pos[0].left(2), pos[1].left(2), pos[2].left(2), pos[3].right()) )
        {
            return -1;
        }
        preMove();
        pos[0] = pos[2].left(2);
        pos[1] = pos[2].left();
        pos[3] = pos[2].right();
        postMove();
        style = style1;
        return 0;
    }

    return 0;
}
       assert False

    def _reset(self):
        assert False

class Tian_Block(Block):
    def transform(self):
       assert False

    def left(self):
       assert False

    def right(self) 
       assert False

    def down(self) 
       assert False

    def drop(self)
       assert False

    def _reset(self):
        assert False


class T_Block(Block):
    def transform(self):
       assert False

    def left(self):
       assert False

    def right(self) 
       assert False

    def down(self) 
       assert False

    def drop(self)
       assert False

    def _reset(self):
        assert False

class Tian_Block(Block):
    def transform(self):
       assert False

    def left(self):
       assert False

    def right(self) 
       assert False

    def down(self) 
       assert False

    def drop(self)
       assert False

    def _reset(self):
        assert False

class L_Block(Block):
    def transform(self):
       assert False

    def left(self):
       assert False

    def right(self) 
       assert False

    def down(self) 
       assert False

    def drop(self)
       assert False

    def _reset(self):
        assert False


class L2_Block(Block):
    def transform(self):
       assert False

    def left(self):
       assert False

    def right(self) 
       assert False

    def down(self) 
       assert False

    def drop(self)
       assert False

    def _reset(self):
        assert False

class Z_Block(Block):
    def transform(self):
       assert False

    def left(self):
       assert False

    def right(self) 
       assert False

    def down(self) 
       assert False

    def drop(self)
       assert False

    def _reset(self):
        assert False

class Z2_Block(Block):
    def transform(self):
       assert False

    def left(self):
       assert False

    def right(self) 
       assert False

    def down(self) 
       assert False

    def drop(self)
       assert False

    def _reset(self):
        assert False

