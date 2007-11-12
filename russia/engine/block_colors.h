#ifndef __BLOCKS_COLORS_H__
#define __BLOCKS_COLORS_H__

#include <qcolor.h>

const QColor BLOCK_NORMAL_CLR_TABLES[] = {
    QColor(191,0,0),
    QColor(0,191,0),
    QColor(0,0,191),
    QColor(191,191,0),
    QColor(191,0,191),
    QColor(0,191,191)
};

const QColor BLOCK_DARK_CLR_TABLES[] = {
    Qt::darkGray,
    Qt::darkRed,
    Qt::darkGreen,
    Qt::darkBlue,
    Qt::darkCyan,
    Qt::darkMagenta,
    Qt::darkYellow
};

const QColor& getBlockNormalClr(int unit_value)
{
    return BLOCK_NORMAL_CLR_TABLES[unit_value];
}

const QColor& getBlockDarkClr(int unit_value)
{
    return BLOCK_DARK_CLR_TABLES[unit_value];
}

inline int lighter(int c)
{ return c > 0 ? 255 : 0; }

inline int darker(int c)
{ return c > 0 ? 128 : 0; }

void getBlock3DClr(const QColor& clr, QColor& clr1, QColor& clr2)
{
    int red   = clr.red();
    int green = clr.green();
    int blue  = clr.blue();
    clr1.setRgb(lighter(red), 
                lighter(green), 
                lighter(blue));
    clr2.setRgb(darker(red), 
                darker(green), 
                darker(blue));
}

void getBlock3DClr(int unit_value, QColor& clr1, QColor& clr2)
{
    const QColor& clr = getBlockNormalClr(unit_value);
    getBlock3DClr(clr, clr1, clr2 );
}



#endif /*__BLOCKS_COLORS_H__*/
