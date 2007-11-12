#ifndef __RUSSIA_UNIT_WORLD_H__
#define __RUSSIA_UNIT_WORLD_H__

#define EMPTY -1
#define GRAY  -2
#include <assert.h>

//
// Unit
//
struct Unit 
{
    int value;
};

//
// Pos
//
struct Pos 
{
    int x;
    int y;
    Pos();
    Pos(int,int);
    Pos(const Pos& p);
    Pos& operator=(const Pos& p);

    Pos left(int dx=1) const;
    Pos right(int dx=1) const;
    Pos up(int dy=1) const;
    Pos down(int dy=1) const;

    Pos& move(int dx, int dy);
    Pos& move(const Pos& pos);
};

//
// UnitWorld
//
class UnitWorld 
{
    public:
        UnitWorld(int maxCol, int maxRow, int minCol=0, int minRow=0);
        ~UnitWorld();

    public:
        void init();
        void clear();

        void setEmpty(int x, int y);
        void setEmpty(const Pos& p);

        bool isEmpty(int x, int y) const;
        bool isEmpty(const Pos& p) const;

        int  value(int x, int y) const;
        int  value(const Pos& p) const;

        void setValue(int x, int y, int val);
        void setValue(const Pos& p, int val);

        int  getMaxCol() const;
        int  getMaxRow() const;

        int  getFullLineCount();
        void flagFullLines();
        void removeFullLines();

    protected:
        const int maxCol;
        const int maxRow;
        const int minCol;
        const int minRow;
        Unit** units;
        int fullLineCount;
        int fullLines[4];

    protected:
        void setEmpty(int row);
        void setGrayFlag(int row);
};

/////////////////////////////////////////////////////////////////////////////////////////////////////////////
// implement of Pos
//
inline Pos::Pos()
{ x = EMPTY; y = EMPTY; } 

inline Pos::Pos(int _x, int _y) 
{ x = _x ; y = _y ; } 

inline Pos& Pos::operator=(const Pos& p)
{ 
    if( this == &p )
        return *this; 
    x = p.x; y = p.y; 
    return *this; 
}

inline Pos::Pos(const Pos& p)
{ *this = p; }

inline Pos Pos::left(int dx) const
{ return Pos(x-dx,y); } 

inline Pos Pos::right(int dx) const
{ return Pos(x+dx,y); } 

inline Pos Pos::up(int dy) const
{ return Pos(x,y-dy); } 

inline Pos Pos::down(int dy) const
{ return Pos(x,y+dy); } 

inline Pos& Pos::move(int dx, int dy)
{ 
    x += dx; y += dy; 
    return *this; 
}

inline Pos& Pos::move(const Pos& p)
{
    x += p.x; y += p.y; 
    return *this; 
}

/////////////////////////////////////////////////////////////////////////////////////////
// implement of UnitWorld
//
inline UnitWorld::UnitWorld(int _maxCol, int _maxRow, int _minCol, int _minRow)
    : maxCol(_maxCol), maxRow(_maxRow), minCol(_minCol), minRow(0), fullLineCount(0)
{
    units = new Unit*[maxCol];
    for( int col = 0 ; col < maxCol ; ++col )
        units[col] = new Unit[maxRow];
    clear();
}

inline void  UnitWorld::init() 
{

}
inline void UnitWorld::clear() 
{
    for( int col = 0 ; col < maxCol ; ++col )
        for( int row = 0 ; row < maxRow ; ++row )
            units[col][row].value = EMPTY;
    for( int i = 0 ; i < 4 ; ++i )
        fullLines[i] = EMPTY;
    fullLineCount = 0;
}
inline void UnitWorld::setEmpty(int x, int y )
{ 
    assert(x >= 0 && x < maxCol); 
    assert(y >= 0 && y < maxRow); 
    units[x][y].value = EMPTY; 
}

inline void UnitWorld::setEmpty(const Pos& p)
{ 
    setEmpty(p.x, p.y); 
}

inline bool UnitWorld::isEmpty(int x, int y) const 
{ 
    if( x < minCol || x > maxCol-1 || y < 0 || y > maxRow-1 )
        return false;
    return ( units[x][y].value == EMPTY );
}

inline bool UnitWorld::isEmpty(const Pos& p) const 
{ 
    return isEmpty(p.x,p.y); 
}

inline int UnitWorld::value(int x, int y) const 
{ 
    return units[x][y].value; 
}

inline int UnitWorld::value(const Pos& p) const
{ 
    return value(p.x,p.y); 
}

inline void UnitWorld::setValue(int x, int y, int val) 
{ 
    assert(x >= 0 && x < maxCol); 
    assert(y >= 0 && y < maxRow); 
    units[x][y].value = val; 
}

inline void UnitWorld::setValue(const Pos& p, int val) 
{ 
    setValue(p.x,p.y,val); 
}

inline int UnitWorld::getMaxCol() const 
{ return maxCol; }

inline int UnitWorld::getMaxRow() const 
{ return maxRow; }


#endif /*__RUSSIA_UNIT_WORLD_H__*/
