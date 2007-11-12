#include "view.h"
#include "rs_engine.h"
#include <qpainter.h>
#include <qcolor.h>
#include <qpixmap.h>
#include <qpen.h>
#include "block_colors.h"

const QColor bkClr(0,0,0);
const int ROW = 20;
const int COL = 10; 
const int BLOCK_W = 10;
const int BLOCK_H = 10;


RS_View::RS_View(QWidget* parent, const char* name, WFlags f)
    : QWidget( parent, name, f|WStyle_NoBorder), _engine( NULL )
{
    setCaption( tr("Russia") );
    setBackgroundMode(NoBackground);
    init();
}

RS_View::~RS_View()
{

}

void RS_View::paintBkgnd( QPainter* p )
{
    CHECK_PTR( p );

    p->fillRect(rect(), QBrush(bkClr));//fill whole rect
    //draw the split line
    static const QRect blocks_area( 0, 0, 10*BLOCK_W, 20*BLOCK_H );
    p->setPen( QPen(Qt::red,2) );
    p->drawLine( blocks_area.right()+1, 0 , blocks_area.right()+1, height() ); 
}

void RS_View::draw3dRect(QPainter* p, const QRect& rect, const QColor& clr1, const QColor& clr2)
{
    p->setPen(clr1);
    p->drawLine( rect.x(), rect.y(), rect.right()-1, rect.y() );
    p->drawLine( rect.x(), rect.y(), rect.x(), rect.bottom()-1 );
    p->setPen(clr2);
    p->drawLine( rect.right(), rect.y()+1, rect.right(), rect.bottom() );
    p->drawLine( rect.x()+1, rect.bottom(), rect.right(), rect.bottom() );
}

void RS_View::drawBlock(QPainter* p, const QRect& rect, const QColor& bkClr, const QColor& clr1, const QColor& clr2)
{
    CHECK_PTR(p);
    ASSERT( !rect.isNull() );

    p->fillRect(rect, QBrush(bkClr) );
    draw3dRect(p, rect, clr1, clr2);
}

void RS_View::paintForegnd(QPainter* p)
{
    CHECK_PTR( p );
    UnitWorld& units = engine()->data();

    for( int row = 0 ; row < MAX_ROW ; ++row )
    {
        for( int col = 0 ; col < MAX_COL ; ++col)
        {
            int value = units.value(col,row);
            if( value != EMPTY && value != GRAY )
            {
                const QColor& bkclr = getBlockNormalClr(units.value(col,row));
                QColor clr1, clr2;
                getBlock3DClr(bkclr, clr1, clr2);
                drawBlock(p, QRect(col*BLOCK_W, row*BLOCK_H, BLOCK_W, BLOCK_H), bkclr, clr1, clr2 );
            }
        }
    }

}

void RS_View::paintEvent( QPaintEvent* e )
{
    QWidget::paintEvent(e);

    QPixmap pixmap( rect().width(), rect().height() );
    QPainter painter;
    painter.begin(&pixmap);

    paintBkgnd(&painter);
    paintForegnd(&painter);
    
    painter.end();

    painter.begin(this);
    painter.drawPixmap(pixmap.rect(), pixmap);
    painter.end();
}

void RS_View::init()
{
    _engine = new RS_Engine(this);
    connect(_engine, SIGNAL( update() ), this, SLOT( repaint() ) );
}

RS_Engine* RS_View::engine()
{
    CHECK_PTR( _engine );
    return _engine;
}

void RS_View::keyPressEvent(QKeyEvent* e)
{
//    qDebug("key press");
    switch( e->key() )
    {
        case Key_F1:
            engine()->start();
            break;
        case Key_F2:
            engine()->pause();
            break;
        case Key_F3:
            engine()->stop();
            break;
        case Key_Space:
            engine()->quickDown();
            break;
        case Key_Left:
            engine()->moveLeft();
            break;
        case Key_Right:
            engine()->moveRight();
            break;
        case Key_Up:
            engine()->transform();
            break;
        case Key_Down:
            engine()->moveDown();
            break;
        default:
            QWidget::keyPressEvent(e);
            break;
    }
}
