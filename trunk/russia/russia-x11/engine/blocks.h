#ifndef __RUSSIA_BLOCKS_H__
#define __RUSSIA_BLOCKS_H__

#include "unitworld.h"

class Block 
{
    public:
       Block(UnitWorld& world, int val);
       virtual ~Block();

    public:
       virtual int transform()     = 0;
       virtual int left()          = 0;
       virtual int right()         = 0;
       virtual int down()          = 0;
       virtual int drop()          = 0;

       void appear();
       bool isOver() const;
       void do_reset();
       void setValue(int val);
       int  getValue() const;

    protected:
       virtual void reset() = 0;
       void preMove();
       void postMove();
       void moveLeft();
       void moveRight();
       void moveDown();

       bool isEmpty(const Pos& pos);
       bool isEmpty(const Pos& pos1,const Pos& pos2);
       bool isEmpty(const Pos& pos1,const Pos& pos2, const Pos& pos3); 
       bool isEmpty(const Pos& pos1,const Pos& pos2, const Pos& pos3, const Pos& pos4); 

    protected:
       UnitWorld& units;
       int value;
       Pos pos[4];
       enum Style { style1, style2, style3, style4 };
       Style style;
       bool over;
};

inline bool Block::isOver() const 
{ return over; }

inline void Block::setValue(int val)
{ value = val; }

inline int Block::getValue() const
{ return value; }

inline void Block::appear() 
{ postMove(); }





class Tian_Block : public Block
{
    public:
        Tian_Block(UnitWorld& world, int val);
        ~Tian_Block();
    public:
        int transform();
        int left();   
        int right(); 
        int down(); 
        int drop();

    protected:
        void reset();
};

class I_Block : public Block
{
    public:
        I_Block(UnitWorld& world, int val);
        ~I_Block();
    public:
        int transform();
        int left();   
        int right(); 
        int down(); 
        int drop();
    protected:
        void reset();
        
};

class T_Block : public Block
{
    public:
        T_Block(UnitWorld& world, int val);
        ~T_Block();
    public:
        int transform();
        int left();   
        int right(); 
        int down(); 
        int drop();
    protected:
        void reset();
};

class L_Block : public Block
{
    public:
        L_Block(UnitWorld& world, int val);
        ~L_Block();
    public:
        int transform();
        int left();   
        int right(); 
        int down(); 
        int drop();
    protected:
        void reset();
};

class L2_Block : public Block
{
    public:
        L2_Block(UnitWorld& world, int val);
        ~L2_Block();
    public:
        int transform();
        int left();   
        int right(); 
        int down(); 
        int drop();
    protected:
        void reset();
};

class Z_Block : public Block
{
    public:
        Z_Block(UnitWorld& world, int val);
        ~Z_Block();
    public:
        int transform();
        int left();   
        int right(); 
        int down(); 
        int drop();
    protected:
        void reset();
};

class Z2_Block : public Block
{
    public:
        Z2_Block(UnitWorld& world, int val);
        ~Z2_Block();
    public:
        int transform();
        int left();   
        int right(); 
        int down(); 
        int drop();
    protected:
        void reset();
};
        

enum BlockType { I, Tian, T, L, L2, Z, Z2 };  

struct BlockFactory 
{
    static Block* createBlock(BlockType type, int value, UnitWorld& units);
    static void destroyBlock(Block* block);
};


#endif /*__RUSSIA_BLOCKS_H__*/
