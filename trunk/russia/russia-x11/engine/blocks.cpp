#include "blocks.h"
#include <qapplication.h>

////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
//
// BlockFactory
//
Block* BlockFactory::createBlock(BlockType type, int value, UnitWorld& units) 
{
    static Block* blocks[7] = { 0 };

    Block* block = blocks[type];
    if( 0 == block ) 
    {
        switch(type)
        {
            case Tian:
                block = new Tian_Block(units,value);
                break;
            case I:
                block = new I_Block(units,value);
                break;
            case T:
                block = new T_Block(units,value);
                break;
            case L:
                block = new L_Block(units,value);
                break;
            case L2:
                block = new L2_Block(units,value);
                break;
            case Z:
                block = new Z_Block(units,value);
                break;
            case Z2:
                block = new Z2_Block(units,value);
                break;
            default:
                ASSERT(false);
                break;
        }
        blocks[type] = block;
    }
    block->setValue(value);
    block->appear();

    CHECK_PTR( block );
    return block;
}

void BlockFactory::destroyBlock(Block* block) 
{
   block->do_reset();
}

////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
//
//
// Block
Block::Block(UnitWorld& world, int val)
    : units(world), value(val), style(style1), over(false)
{

}

Block::~Block()
{

}

void Block::do_reset()
{
    reset();
    over = false;
    style = style1;
}

inline void Block::preMove()
{
    for( int i = 0 ; i < 4 ; ++i )
        units.setEmpty(pos[i]);
}

inline void Block::postMove()
{
    for( int i = 0 ; i < 4 ; ++i )
        units.setValue(pos[i],value);
}

inline bool Block::isEmpty(const Pos& pos)
{
    return units.isEmpty(pos);
}

inline void Block::moveLeft()
{
    preMove();
    for( int i = 0 ; i < 4 ; ++i )
        pos[i].x--;
    postMove();
}

inline void Block::moveRight()
{
    preMove();
    for( int i = 0 ; i < 4 ; ++i )
        pos[i].x++;
    postMove();
}

inline void Block::moveDown()
{
    preMove();
    for( int i = 0 ; i < 4 ; ++i )
        pos[i].y++;
    postMove();
}

inline bool Block::isEmpty(const Pos& pos1,const Pos& pos2)
{
    return units.isEmpty(pos1) && units.isEmpty(pos2);
}

inline bool Block::isEmpty(const Pos& pos1,const Pos& pos2, const Pos& pos3)
{
    return units.isEmpty(pos1) && units.isEmpty(pos2) && units.isEmpty(pos3);
}

inline bool Block::isEmpty(const Pos& pos1,const Pos& pos2, const Pos& pos3, const Pos& pos4) 
{
    return units.isEmpty(pos1) && units.isEmpty(pos2) && units.isEmpty(pos3) && units.isEmpty(pos4);
}
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
//
//  0 3 
//  1 2
//
Tian_Block::Tian_Block(UnitWorld& world, int val)
    : Block(world, val)
{
    reset();
    postMove();
}

void Tian_Block::reset()
{
    qDebug("Tian_Block::reset");
    pos[0].x = units.getMaxCol()/2-1; pos[0].y = 1;
    pos[1] = pos[0].down();
    pos[2] = pos[1].right();
    pos[3] = pos[2].up();
}


Tian_Block::~Tian_Block()
{

}

int Tian_Block::transform()
{
    qDebug("Tian_Block::transform()");
    return -1;
}

int Tian_Block::left()   
{
    qDebug("Tian_Block::left()");
    
    if( isEmpty(pos[0].left(), pos[1].left()) )
    { 
        moveLeft();
        return 0;
    }
    return -1;
}

int Tian_Block::right() 
{
    qDebug("Tian_Block::right()");

    if( isEmpty(pos[2].right(), pos[3].right()) )
    { 
        moveRight();
        return 0;
    }
    return -1;
}

int Tian_Block::down() 
{
    qDebug("Tian_Block::down()");

    if( isEmpty(pos[1].down(), pos[2].down()) )
    { 
        moveDown();
        over = false;
        return 0;
    }
    over = true;
    return -1;
}

int Tian_Block::drop()
{
    qDebug("drop");
    while( down() == 0 )
    {
    }
    return 0;
}

////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
//
//       0
//       1
//   0 1 2 3
//       3
//
// style1 - vertical
// style2 - horizontal
//
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

int I_Block::drop()
{
    qDebug("drop");
    while( down() == 0 ) //could be optimized later
    {
    }
    return 0;
}

///////////////////////////////////////////////////////////////////////////////////////////////////////
//
// L_Block
//
L_Block::L_Block(UnitWorld& world, int val)
    : Block(world, val)
{
    reset();
    postMove();
}

L_Block::~L_Block()
{

}

void L_Block::reset()
{
    //style1
    pos[0].x = units.getMaxCol()/2 - 2; pos[0].y = 2;
    pos[1] = pos[0].right();
    pos[2] = pos[1].right();
    pos[3] = pos[2].down();
}

int L_Block::transform()
{
    qDebug("L_Block::transform()");

    if( style == style1 )
    {/*style1 -> style2
         x x     2 3
       0 1 2     1
       x x 3     0
     */
        if( !isEmpty(pos[0].down(), pos[1].up(), pos[2].up(), pos[3].left()) )
            return -1;
        preMove();
        pos[0] = pos[1].down();
        pos[2] = pos[1].up();
        pos[3] = pos[2].right();
        postMove();
        style = style2;
    }
    else if( style == style2 )
    {/*style2 -> style3
       x 2 3   3
       x 1 x   2 1 0
         0 x 
     */
        if( !isEmpty(pos[0].right(), pos[1].right(), pos[1].left(), pos[2].left()) )
            return -1;
        preMove();
        pos[0] = pos[1].right();
        pos[2] = pos[1].left();
        pos[3] = pos[2].up();
        postMove();
        style = style3;
    }
    else if( style == style3 )
    {/* style3 -> style4
       3 x x     0
       2 1 0     1  
       x x     3 2
     */
        if( !isEmpty(pos[0].up(), pos[1].up(), pos[1].down(), pos[2].down()) )
            return -1;
        preMove();
        pos[0] = pos[1].up();
        pos[2] = pos[1].down();
        pos[3] = pos[2].left();
        postMove();
        style = style4;
    }
    else 
    {/* style3 -> style4
         x 0       
         x 1 x    0 1 2
         3 2 x        3
    */
        if( !isEmpty(pos[0].left(), pos[1].left(), pos[1].right(), pos[2].right()) )
            return -1;
        preMove();
        pos[0] = pos[1].left();
        pos[2] = pos[1].right();
        pos[3] = pos[2].down();
        postMove();
        style = style1;
    }
    return 0;

}

int L_Block::left()   
{
    qDebug("L_Block::left()");

    if( style == style1 )
    {
        if( !isEmpty(pos[0].left(), pos[3].left()) )
            return -1;
    }
    else if( style == style2 )
    {
        if( !isEmpty(pos[0].left(), pos[1].left(), pos[2].left()) )
            return -1;
    }
    else if( style == style3 )
    {
        if( !isEmpty(pos[2].left(), pos[3].left()) )
            return -1;
    }
    else 
    {//style4
        if( !isEmpty(pos[0].left(), pos[1].left(), pos[3].left()) )
            return -1;
    }

    moveLeft();
    return 0;
}

int L_Block::right() 
{
    qDebug("L_Block::right()");

    if( style == style1 )
    {
        if( !isEmpty(pos[2].right(), pos[3].right()) )
            return -1;
    }
    else if( style == style2 )
    {
        if( !isEmpty(pos[0].right(), pos[1].right(), pos[3].right()) )
            return -1;
    }
    else if( style == style3 )
    {
        if( !isEmpty(pos[0].right(), pos[3].right()) )
            return -1;
    }
    else 
    {//style4
        if( !isEmpty(pos[0].right(), pos[1].right(), pos[2].right()) )
            return -1;
    }
    moveRight();
    return 0;
}

int L_Block::down() 
{
    qDebug("L_Block::down()");

    if( style == style1 )
    {
        if( !isEmpty(pos[0].down(), pos[1].down(), pos[3].down()) )
        {
            over = true;
            return -1;
        }
    }
    else if( style == style2 )
    {
        if( !isEmpty(pos[0].down(), pos[3].down()) )
        {
            over = true;
            return -1;
        }
    }
    else if( style == style3 )
    {
        if( !isEmpty(pos[0].down(), pos[1].down(), pos[2].down()) )
        {
            over = true;
            return -1;
        }
    }
    else 
    {//style4
        if( !isEmpty(pos[2].down(), pos[3].down()) )
        {
            over = true;
            return -1;
        }
    }
    moveDown();
    over = false;
    return 0;
}

int L_Block::drop()
{
    qDebug("drop");
    while( down() == 0 ) //could be optimized later
    {
    }
    return 0;
}

///////////////////////////////////////////////////////////////////////////////////////////////////////
//
// L2_Block
//
L2_Block::L2_Block(UnitWorld& world, int val)
    : Block(world, val)
{
    reset();
    postMove();
}

L2_Block::~L2_Block()
{

}

void L2_Block::reset()
{
    //style1
    pos[0].x = units.getMaxCol()/2 - 2; pos[0].y = 2;
    pos[1] = pos[0].up();
    pos[2] = pos[1].right();
    pos[3] = pos[2].right();
}

int L2_Block::transform()
{
    qDebug("L2_Block::transform()");

    if( style == style1 )
    {/*style1 -> style2
       x x       3 
       1 2 3     2 
       0 x x     1 0 
     */
        if( !isEmpty(pos[0].right(), pos[1].up(), pos[2].up(), pos[3].down()) )
            return -1;
        preMove();
        pos[1] = pos[2].down();
        pos[0] = pos[1].right();
        pos[3] = pos[2].up();
        postMove();
        style = style2;
    }
    else if( style == style2 )
    {/*style2 -> style3
       x 3 x       0
       x 2 x   3 2 1
         1 0 
     */
        if( !isEmpty(pos[2].left(), pos[2].right(), pos[3].left(), pos[3].right()) )
            return -1;
        preMove();
        pos[1] = pos[2].right();
        pos[0] = pos[1].up();
        pos[3] = pos[2].left();
        postMove();
        style = style3;
    }
    else if( style == style3 )
    {/* style3 -> style4
       x x 0   0 1
       3 2 1     2  
       x x       3
     */
        if( !isEmpty(pos[2].up(), pos[3].up(), pos[2].down(), pos[3].down()) )
            return -1;
        preMove();
        pos[1] = pos[2].up();
        pos[0] = pos[1].left();
        pos[3] = pos[2].down();
        postMove();
        style = style4;
    }
    else 
    {/* style3 -> style4
         0 1       
         x 2 x    1 2 3
         x 3 x    0    
    */
        if( !isEmpty(pos[2].left(), pos[3].left(), pos[2].right(), pos[3].right()) )
            return -1;
        preMove();
        pos[1] = pos[2].left();
        pos[0] = pos[1].down();
        pos[3] = pos[2].right();
        postMove();
        style = style1;
    }
    return 0;

}

int L2_Block::left()   
{
    qDebug("L2_Block::left()");

    if( style == style1 )
    {
        if( !isEmpty(pos[0].left(), pos[1].left()) )
            return -1;
    }
    else if( style == style2 )
    {
        if( !isEmpty(pos[1].left(), pos[2].left(), pos[3].left()) )
            return -1;
    }
    else if( style == style3 )
    {
        if( !isEmpty(pos[0].left(), pos[3].left()) )
            return -1;
    }
    else 
    {//style4
        if( !isEmpty(pos[0].left(), pos[2].left(), pos[3].left()) )
            return -1;
    }

    moveLeft();
    return 0;
}

int L2_Block::right() 
{
    qDebug("L2_Block::right()");

    if( style == style1 )
    {
        if( !isEmpty(pos[0].right(), pos[3].right()) )
            return -1;
    }
    else if( style == style2 )
    {
        if( !isEmpty(pos[0].right(), pos[2].right(), pos[3].right()) )
            return -1;
    }
    else if( style == style3 )
    {
        if( !isEmpty(pos[0].right(), pos[1].right()) )
            return -1;
    }
    else 
    {//style4
        if( !isEmpty(pos[1].right(), pos[2].right(), pos[3].right()) )
            return -1;
    }
    moveRight();
    return 0;
}

int L2_Block::down() 
{
    qDebug("L2_Block::down()");

    if( style == style1 )
    {
        if( !isEmpty(pos[0].down(), pos[2].down(), pos[3].down()) )
        {
            over = true;
            return -1;
        }
    }
    else if( style == style2 )
    {
        if( !isEmpty(pos[0].down(), pos[1].down()) )
        {
            over = true;
            return -1;
        }
    }
    else if( style == style3 )
    {
        if( !isEmpty(pos[1].down(), pos[2].down(), pos[3].down()) )
        {
            over = true;
            return -1;
        }
    }
    else 
    {//style4
        if( !isEmpty(pos[0].down(), pos[3].down()) )
        {
            over = true;
            return -1;
        }
    }
    moveDown();
    over = false;
    return 0;
}

int L2_Block::drop()
{
    qDebug("drop");
    while( down() == 0 ) //could be optimized later
    {
    }
    return 0;
}

//////////////////////////////////////////////////////////////////////////////////////////
//
// T_Block
//
T_Block::T_Block(UnitWorld& units, int val)
    : Block(units,val)
{
    reset();
    postMove();
}

T_Block::~T_Block()
{

}
void T_Block::reset()
{
    //style1
    pos[0].x = units.getMaxCol()/2 - 1; pos[0].y = 1;
    pos[1] = pos[0].right();
    pos[2] = pos[1].right();
    pos[3] = pos[1].down();
}
int T_Block::transform()
{
    qDebug("T_Block::transform()");

    if( style == style1 )
    {/*style1 -> style2
         x x   2
       0 1 2   1 3
       x 3 x   0
     */
        if( !isEmpty(pos[0].down(), pos[2].down(), pos[1].up(), pos[2].up()) )
        {
            return -1;
        }
        preMove();
        pos[0] = pos[1].down();
        pos[2] = pos[1].up();
        pos[3] = pos[1].right();
        postMove();
        style = style2;
        return 0;
    }
    else if( style == style2 ) 
    {/*style2 -> style3
     x 2 x       3
     x 1 3  -> 2 1 0
       0 x
    */
        if( !isEmpty(pos[0].right(), pos[2].right(), pos[1].left(), pos[2].left()) )
        {
            return -1;
        }
        preMove();
        pos[0] = pos[1].right();
        pos[2] = pos[1].left();
        pos[3] = pos[1].up();
        postMove();
        style = style3;
        return 0;
    }
    else if( style == style3 )
    {/* style3 -> style4
     x 3 x         0
     2 1 0  ->   3 1
     x x           2
    */
        if( !isEmpty(pos[0].up(), pos[2].up(), pos[1].down(), pos[2].down()) )
        {
            return -1;
        }
        preMove();
        pos[0] = pos[1].up();
        pos[2] = pos[1].down();
        pos[3] = pos[1].left();
        postMove();
        style = style4;
        return 0;
    }
    else
    {/* style4 -> style1
      x	0         
      3	1 x  ->  0 1 2
      x	2 x        3

    */
        if( !isEmpty(pos[0].left(), pos[2].left(), pos[1].right(), pos[2].right()) )
        {
            return -1;
        }
        preMove();
        pos[0] = pos[1].left();
        pos[2] = pos[1].right();
        pos[3] = pos[1].down();
        postMove();
        style = style1;
        return 0;
    }
}

int T_Block::left()   
{
    qDebug("T_Block::left()");

    if( style == style1 )
    {//style1
        if( !isEmpty(pos[0].left(), pos[3].left()) )
            return -1;
    }
    else if( style == style2 )
    {//style2
        if( !isEmpty(pos[0].left(), pos[1].left(), pos[2].left()) )
            return -1;
    }
    else if( style == style3 ) 
    {//style3
        if( !isEmpty(pos[3].left(), pos[2].left()) )  
            return -1;
    }
    else 
    {//style4
        if( !isEmpty(pos[0].left(), pos[3].left(), pos[2].left()) )  
            return -1;
    }
    moveLeft();
    return 0;
}

int T_Block::right() 
{
    if( style == style1 )
    {//style1
        if( !isEmpty(pos[2].right(), pos[3].right()) )
            return -1;
    }
    else if( style == style2 )
    {//style2
        if( !isEmpty(pos[0].right(), pos[3].right(), pos[2].right()) )
            return -1;
    }
    else if( style == style3 ) 
    {//style3
        if( !isEmpty(pos[0].right(), pos[3].right()) )  
            return -1;
    }
    else 
    {//style4
        if(!isEmpty(pos[0].right(), pos[1].right(), pos[2].right()) )  
            return -1;
    }
    moveRight();
    return 0;
}

int T_Block::down() 
{
    if( style == style1 )
    {//style1
        if( !isEmpty(pos[0].down(), pos[3].down(), pos[2].down()) )
	{
	    over = true;
            return -1;
	}
    }
    else if( style == style2 )
    {//style2
        if(!isEmpty(pos[0].down(), pos[3].down()) )
	{
	    over = true;
            return -1;
	}
    }
    else if( style == style3 ) 
    {//style3
        if(!isEmpty(pos[2].down(), pos[1].down(), pos[0].down()) )  
	{
	    over = true;
            return -1;
	}
    }
    else 
    {//style4
        if(!isEmpty(pos[2].down(), pos[3].down()) )
	{
	    over = true;
            return -1;
	}
    }
    moveDown();
    over = false;
    return 0;
}

int T_Block::drop()
{
    qDebug("drop");
    while( down() == 0 ) //could be optimized later
    {
    }
    return 0;
}

////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
//
// Z_Block
//
Z_Block::Z_Block(UnitWorld& units, int val)
    : Block(units,val)
{
    reset();
    postMove();
}

Z_Block::~Z_Block()
{

}

void Z_Block::reset()
{
    //style1
    pos[0].x = units.getMaxCol()/2 - 1; pos[0].y = 1;
    pos[1] = pos[0].right();
    pos[2] = pos[1].down();
    pos[3] = pos[2].right();
}

int Z_Block::transform()
{
    qDebug("Z_Block::transform()");
    if( style == style1 )
    {/*style1 -> style2
       0 1 x      3
       x 2 3    1 2
       x        0
     */
        if( !isEmpty(pos[0].down(), pos[0].down(2), pos[3].up()) )
        {
            return -1;
        }
        preMove();
        pos[1] = pos[2].left();
        pos[0] = pos[1].down();
        pos[3] = pos[2].up();
        postMove();
        style = style2;
        return 0;
    }
    else 
    {/*style2 -> style1
          x 3   0 1
          1 2 x   2 3
          0 x 
    */
        if( !isEmpty(pos[0].right(), pos[2].right(), pos[3].left()) )
        {
            return -1;
        }
        preMove();
        pos[1] = pos[2].up();
        pos[0] = pos[1].left();
        pos[3] = pos[2].right();
        postMove();
        style = style1;
        return 0;
    }

    return 0;
}
int Z_Block::left()   
{
    qDebug("Z_Block::left()");

    if( style == style1 )
    {
        if( !isEmpty(pos[0].left(), pos[2].left()) )
            return -1;
    }
    else 
    {//style2
        if( !isEmpty(pos[0].left(), pos[1].left(), pos[3].left()) )
            return -1;
    }

    moveLeft();
    return 0;
}

int Z_Block::right() 
{
    qDebug("Z_Block::right()");

    if( style == style1 )
    {
        if( !isEmpty(pos[1].right(), pos[3].right()) )
            return -1;
    }
    else 
    {//style2
        if( !isEmpty(pos[0].right(), pos[2].right(), pos[3].right()) )
            return -1;
    }

    moveRight();
    return 0;
}

int Z_Block::down() 
{
    qDebug("Z_Block::down()");

    if( style == style1 )
    {
        if( !isEmpty(pos[0].down(), pos[2].down(), pos[3].down()) )
        {
            over = true;
            return -1;
        }
    }
    else 
    {//style1
        if( !isEmpty(pos[0].down(), pos[2].down()) ) 
        {
            over = true;
            return -1;
        }
    }
    moveDown();
    over = false;
    return 0;
}

int Z_Block::drop()
{
    qDebug("drop");
    while( down() == 0 ) //could be optimized later
    {
    }
    return 0;
}

////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
//
// Z2_Block
//
Z2_Block::Z2_Block(UnitWorld& units, int val)
    : Block(units,val)
{
    reset();
    postMove();
}

Z2_Block::~Z2_Block()
{

}

void Z2_Block::reset()
{
    //style1
    pos[0].x = units.getMaxCol()/2 - 1; pos[0].y = 2;
    pos[1] = pos[0].right();
    pos[2] = pos[1].up();
    pos[3] = pos[2].right();
}

int Z2_Block::transform()
{
    qDebug("Z2_Block::transform()");
    if( style == style1 )
    {/*style1 -> style2
       x 2 3    3  
       0 1      2 1
       x x        0
     */
        if( !isEmpty(pos[0].down(), pos[1].down(), pos[0].up()) )
            return -1;
        preMove();
        pos[0] = pos[1].down();
        pos[2] = pos[1].left();
        pos[3] = pos[2].up();
        postMove();
        style = style2;
        return 0;
    }
    else 
    {/*style2 -> style1
          3 x x   2 3
          2 1 x 0 1  
            0 
    */
        if( !isEmpty(pos[1].right(), pos[3].right(), pos[3].right(2)) )
            return -1;
        preMove();
        pos[0] = pos[1].left();
        pos[2] = pos[1].up();
        pos[3] = pos[2].right();
        postMove();
        style = style1;
        return 0;
    }

    return 0;
}
int Z2_Block::left()   
{
    qDebug("Z2_Block::left()");

    if( style == style1 )
    {
        if( !isEmpty(pos[0].left(), pos[2].left()) )
            return -1;
    }
    else 
    {//style2
        if( !isEmpty(pos[0].left(), pos[2].left(), pos[3].left()) )
            return -1;
    }

    moveLeft();
    return 0;
}

int Z2_Block::right() 
{
    qDebug("Z2_Block::right()");

    if( style == style1 )
    {
        if( !isEmpty(pos[1].right(), pos[3].right()) )
            return -1;
    }
    else 
    {//style2
        if( !isEmpty(pos[0].right(), pos[1].right(), pos[3].right()) )
            return -1;
    }

    moveRight();
    return 0;
}

int Z2_Block::down() 
{
    qDebug("Z2_Block::down()");

    if( style == style1 )
    {
        if( !isEmpty(pos[0].down(), pos[1].down(), pos[3].down()) )
        {
            over = true;
            return -1;
        }
    }
    else 
    {//style1
        if( !isEmpty(pos[0].down(), pos[2].down()) ) 
        {
            over = true;
            return -1;
        }
    }
    moveDown();
    over = false;
    return 0;
}

int Z2_Block::drop()
{
    qDebug("drop");
    while( down() == 0 ) //could be optimized later
    {
    }
    return 0;
}
