#!/usr/bin/env python
# -*- coding: utf-8 -*-

EMPTY = -1
GRAY  = -2

class Unit: 
    def __init__(self, value=EMPTY):
        self.value = value

class Pos:
    def __init__(self, x=Empty, y=Empty):
        self.x = x
        self.y = y
    def left(self, dx=1): return Pos(self.x-dx, self.y)
    def right(self, dx=1): return Pos(self.x+dx, self.y)
    def up(self, dy=1): return Pos(self.x, self.y-dy)
    def down(self, dy=1): return Pos(self.x, self.y+dy)
    def move(self,dx,dy):
        self.x += dx
        self.y += dy
        return self

inline UnitWorld::UnitWorld(int _maxCol, int _maxRow, int _minCol, int _minRow)
    : maxCol(_maxCol), maxRow(_maxRow), minCol(_minCol), minRow(0), fullLineCount(0)
{
    units = new Unit*[maxCol];
    for( int col = 0 ; col < maxCol ; ++col )
        units[col] = new Unit[maxRow];
    clear();
}

class UnitWorld:
    def __init__(self, max_col, max_row, min_col=0, min_row=0):
        self.units = []
        self.full_lines = []
        self.max_col = max_col
        self.max_row = max_row

        #matrix
        for x in range(max_col):
            col = []
            for y in range(max_row):
                col.append(Unit())
            self.units.append(col)

    def init(self):
        pass

    def clear(self):
        for col in self.units:
            for u in col:
                u.value = EMPTY
        self.full_lines.clear()

    def set_empty(self, x,y): 
        self.units[x][y].value = EMPTY
    def is_empty(self, x,y): return self.units[x][y].value == EMPTY
    def value(self, x,y) return self.units[x][y].value
    def set_value(self, x,y, value) self.units[x][y].value = value
    def get_full_line_count(self): return len( filter(self.full_lines, lambda l: l!=EMPTY) )
            
        


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


