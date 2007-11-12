#include "unitworld.h"
#include <qapplication.h>


UnitWorld::~UnitWorld()
{
    for( int col = 0 ; col < maxCol ; ++col )
        delete[] units[col]; 

    delete[] units;
}

inline void UnitWorld::setEmpty(int row)
{
    assert(row >= 0 && row < maxRow);
    for( int col = 0 ; col < maxCol ; ++col )
    {
        units[col][row].value = EMPTY;
    }
}

inline void UnitWorld::setGrayFlag(int row)
{
    assert(row >= 0 && row < maxRow);
    for( int col = 0 ; col < maxCol ; ++col )
    {
        units[col][row].value = GRAY;
    }
}

void UnitWorld::flagFullLines()
{
    for( int i = 0; i < 4 ; ++i )
    {
        if( fullLines[i] == EMPTY )
            break;
        setGrayFlag(fullLines[i]);
    }
}

void UnitWorld::removeFullLines()
{
    if( fullLineCount == 0 )
        return;

    int row=0;
    int col=0;
    int row2=0;
    int line=0;
    for( row = 0; row < fullLineCount; ++row)
    {
        for( col = 0 ; col < maxCol; ++col)
        {
            units[col][row].value = EMPTY;
        }
    }

    for( row = maxRow-1, row2 = maxRow-1 ; row >= fullLineCount ; --row, --row2 )
    {
        while( line < 4 && fullLines[line] != EMPTY && row2 == fullLines[line])
        {
            row2--;
            line++;
        }
        for( col = 0 ; col < maxCol; ++col)
        {
            units[col][row] = units[col][row2];
        }
    }

    for( int i = 0 ; i < fullLineCount; ++i )
        fullLines[i] = EMPTY;
    fullLineCount=0;
}

int UnitWorld::getFullLineCount()
{
    fullLineCount = 0;
    int emptyUnitPerLine = 0;

    for( int row = maxRow-1 ; row >= 0 ; --row )
    {
        emptyUnitPerLine = 0;
        for( int col = 0 ; col < maxCol ; ++col )
        {
            if( units[col][row].value == EMPTY )
                emptyUnitPerLine++;
        }
        if( emptyUnitPerLine == maxCol )
            break;
        if( emptyUnitPerLine == 0 )
        {
            fullLineCount++;
            fullLines[fullLineCount-1] = row;
        }
        if( fullLineCount == 4 )
            break;
    }
    return fullLineCount;
}
