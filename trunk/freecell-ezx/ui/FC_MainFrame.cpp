#include "FC_MainFrame.h"
#include "cardsLoader.h"
#include "huffleLoader.h"
#include "FC_ChooseSeedDlg.h"
#include <ZMessageBox.h>
#include <qcolor.h>
#include <qpainter.h>
#include <qpixmap.h>
#include <qdatetime.h>
#include <math.h>
#include <stdlib.h>
#include <RES_ICON_Reader.h>


static const int w = 29;
static const int h = 38;
static const int split_h = 12;
static const int split_w = 1;
static const QColor clrBk(0,127,0);

static unsigned char Club    = 0;
static unsigned char Diamond = 1;
static unsigned char Heart   = 2;
static unsigned char Spade   = 3;

static int suit(CARD card) {
    return ((card) % 4);
}

static int value(CARD card) { 
    return ((card) / 4);
}

static bool isBlack(CARD card)
{
    return (suit(card) == Club || suit(card) == Spade);
}

static bool isRed(CARD card)
{
    return (suit(card) == Diamond || suit(card) == Heart);
}

static bool fit_home(CARD dst, CARD src)
{
    if(dst == EMPTY)
        return ( value(src) == 0 );

    return ( suit(src) == suit(dst) && value(src) == value(dst) + 1);
}

static bool fit_fields(CARD dst, CARD src)
{
    if( dst == EMPTY )
        return true;
    return  ( value(src) == value(dst) - 1 ) && ( isBlack(src) ^ isBlack(dst) ) ;
}

FC_MainFrame::FC_MainFrame(QWidget* parent, const char* name )
    : QWidget(parent, name), m_cardLoader(NULL), m_selCol(EMPTY) 
{
    init();
    new_game();
}

FC_MainFrame::~FC_MainFrame()
{

}



void FC_MainFrame::clear()
{
    for(int i = 0 ; i < 4 ; ++i )
    {
        m_freecells[i] = EMPTY;
        m_homecells[i] = EMPTY;
    }

    for( int j = 0 ; j < 8; ++j )
    {
        m_cards[j].clear();
    }
    m_selCol = EMPTY;
    m_fieldPos.setEmpty();
}

bool FC_MainFrame::init()
{
    setBackgroundMode(NoBackground);
    //setCursor(m_stdCursor);

    //init areas
    m_rtFreecells = QRect(0, 0, w*4, h);
    m_rtFlag      = QRect(m_rtFreecells.right()+1, 0, 7, h );
    m_rtHomecells = QRect(m_rtFlag.right()+1, 0, w*4, h);

    m_rtFields    = QRect(split_w, m_rtFreecells.height()+ 5, (w+split_w)*8, 0);
    //m_rtFields.setBottom( this->rect().bottom() );
    m_rtFields.setBottom(240);

    m_cardLoader = new CardsLoader;
    return m_cardLoader->init();
}

bool FC_MainFrame::shuffle(int seed)
{
    ASSERT( seed >= 0 && seed <= MAX_SEED );

    char deck[52];
    if( !HuffleLoader::load(seed, deck) )
    {
        qDebug("fail to load huffle!");
        return false;
    }

    int index = 0;
    for(int col = 0 ; col < 4; col++)
        for(int pos = 0 ; pos < 7; pos++, index++)
        {
            m_cards[col].append(deck[index]-1);
        }

    for(int col = 4 ; col < 8; col++)
        for(int pos = 0 ; pos < 6; pos++, index++)
        {
            m_cards[col].append(deck[index]-1);
        }

    return true;
}

void FC_MainFrame::paintEvent(QPaintEvent* e)
{
    QPainter painter;
    //QPixmap buffer(this->width(), this->height());
    QPixmap buffer(240, 240);
    painter.begin(&buffer);
    painter.setBrush(clrBk);
    painter.drawRect(buffer.rect());
    paintUpView(painter);
    paintCards(painter);
    painter.end();
    
    painter.begin(this);
    painter.drawPixmap( 0, 0, buffer);
    painter.end();
}

void FC_MainFrame::paintUpView( QPainter& painter )
{

    QRect cell(0,0, w, h);
    //paint freecell and homecell
    for( int i = 0 ; i < 4; ++i )
    {
        //draw freecell frames
        cell.moveTopLeft( QPoint(m_rtFreecells.x()+w*i, m_rtFreecells.y()) );
        draw3dRect(painter, cell, Qt::black, Qt::green);
        
        if( m_freecells[i] != EMPTY )
        {
            if( m_selCol - 8 == i )
                painter.drawPixmap(cell.x(), cell.y(), *m_cardLoader->loadInvertCard(m_freecells[i]));
            else
                painter.drawPixmap(cell.x(), cell.y(), *m_cardLoader->loadCard(m_freecells[i]));
        }

        //draw homesell frames
        cell.moveTopLeft( QPoint(m_rtHomecells.x()+w*i, m_rtHomecells.y()) );
        draw3dRect(painter, cell, Qt::black, Qt::green);

        if( m_homecells[i] != EMPTY )
        {
            painter.drawPixmap(cell.x(), cell.y(), *m_cardLoader->loadCard(m_homecells[i]));
        }

    }
    /*

    //paint flag
    QRect frameRt(m_rtFlag.x() + (m_rtFlag.width()-38)/2, 
            m_rtFlag.y() + (m_rtFlag.height()-38)/2,
            38,
            38);
    const QPixmap& pixmap = *m_flag;
    int x = frameRt.x() + ( frameRt.width() - pixmap.width() ) / 2;
    int y = frameRt.y() + ( frameRt.height() - pixmap.height() ) / 2;
    draw3dRect(painter, frameRt, Qt::green, Qt::black);
    painter.drawPixmap(x,y, pixmap);
    */
}
void FC_MainFrame::paintCards(QPainter& painter)
{
    int x,y;
    int pos,col;
    QPixmap* pixmap = NULL;

    QRect& area = m_rtFields;
    QValueList<int>::Iterator it;
    for( col = 0 ; col < 8 ; col ++ )
    {
        for(it = m_cards[col].begin(), pos = 0 ; it != m_cards[col].end() ; it++, pos++)
        {
            CARD num = *it;
            if( m_selCol == col && it == m_cards[col].fromLast() ) {
                pixmap = m_cardLoader->loadInvertCard(num);
            } else {
                pixmap = m_cardLoader->loadCard(num);
            }
            CHECK_PTR(pixmap);
            x = area.x() + (w+split_w) * col;
            y = area.y() + (split_h) * pos;
            painter.drawPixmap(x, y, *pixmap,
                    0, 0, pixmap->width(), pixmap->height());
        }
    }

    if( !m_fieldPos.isEmpty() )
    {
        col = m_fieldPos.col;
        pos = m_fieldPos.row;
        CARD card = m_cards[col][pos];
        ASSERT( card != EMPTY );
        pixmap = m_cardLoader->loadCard(card);
        CHECK_PTR(pixmap);
        x = area.x() + (w+split_w) * col;
        y = area.y() + (split_h) * pos;
        painter.drawPixmap(x, y, *pixmap,
                    0, 0, pixmap->width(), pixmap->height());
    }
}

inline void FC_MainFrame::draw3dRect(QPainter& painter, const QRect& rect, const QColor& clr1, const QColor& clr2)
{

    painter.setPen(clr1);
    painter.drawLine( rect.x(), rect.y(), rect.right()-1, rect.y() );
    painter.drawLine( rect.x(), rect.y(), rect.x(), rect.bottom()-1 );

    painter.setPen(clr2);
    painter.drawLine( rect.right(), rect.y()+1, rect.right(), rect.bottom() );
    painter.drawLine( rect.x()+1, rect.bottom(), rect.right(), rect.bottom() );
}

void FC_MainFrame::mousePressEvent( QMouseEvent * e)
{
    qDebug("press mouse");
    if( e->button() != Qt::LeftButton )
    {
        return;
    }

    const QPoint& pos = e->pos();

    if(m_rtFreecells.contains(pos))
    {
        qDebug("click freecells");
        QPoint rpos = pos - m_rtFreecells.topLeft();
        int select_col = pos.x() / w;

        if( m_selCol == EMPTY )
        {
            if( m_freecells[select_col] == EMPTY )
            {
                qDebug("choose empty freecell");
                return;
            }
            else 
            {
                qDebug("choose %d freecell", select_col);
                m_selCol = select_col + 8;//begin to track mouse move
            }
        }
        else
        {
            if( select_col + 8 == m_selCol )
            {
                qDebug("select the same freecell");
                m_selCol = EMPTY;//need stop track mouse
            }
            else 
            {
                if( !move2Free(select_col) )
                {
                    qDebug("error");
                    return;
                }
                else 
                {
                    m_selCol = EMPTY;
                    autoplay();
                }
            }
        }
    }
    else if( m_rtFields.contains(pos) )
    {
        qDebug("click fields");
        QPoint rpos  = pos - m_rtFields.topLeft();
        int select_col =  pos.x() / (w + split_w);
        int v = pos.x() % (w + split_w);
        if( v > w )
        {
            qDebug("select split space");
            return;
        }
#if ENABLE_LEFTBTN_HOLD
        
        int select_row = rpos.y() / split_h;
        qDebug("select %d col, %d row", select_col, select_row);

        if( select_row < m_cards[select_col].count()-1 && !m_cards[select_col].isEmpty() )
        {
            ASSERT( m_fieldPos.isEmpty() );
            m_fieldPos.setPos(select_col, select_row);
            update();
            return;
        }
#endif 
        if(m_selCol == select_col) 
        {
            m_selCol = EMPTY;//stop track mouse
        } 
        else
        {
            if( m_selCol == EMPTY ) 
            {
                if(m_cards[select_col].isEmpty()) 
                {
                    return;
                } 
                else 
                {
                    m_selCol = select_col;//begin track mouse
                }
            }
            else 
            {
                if( !move2Fields(select_col) )
                {
                    qDebug("error");
                    return;
                }
                else 
                {
                    m_selCol = EMPTY;
                    autoplay();
                }
            }
        }
    }
    else if(m_rtHomecells.contains(pos))
    {
        qDebug("click homecells");
        if( m_selCol == EMPTY ) 
        {
            return;
        }
        QPoint rpos  = pos - m_rtHomecells.topLeft();
        int select_col = rpos.x() / w;

        if( !move2Home(select_col) )
        {
            qDebug("error");
            return;
        }
        m_selCol = EMPTY;
        autoplay();
    }
    else 
    {
        return;
    }


    this->setMouseTracking(m_selCol != EMPTY);
    if( m_selCol == EMPTY )
    {
        //this->setCursor(m_stdCursor);
    }
    update();
}

void FC_MainFrame::mouseDoubleClickEvent(QMouseEvent* e)
{
    //qDebug("double click");
    if( e->button() != Qt::LeftButton )
        return;

    const QPoint& pos = e->pos();
    if( m_rtFields.contains(pos) )
    {
        qDebug("double click fields");
        QPoint rpos  = pos - m_rtFields.topLeft();
        int select_col =  pos.x() / (w + split_w);
        int v = pos.x() % (w + split_w);
        if( v > w )
        {
            qDebug("select split space");
            return;
        }

        if( m_cards[select_col].isEmpty() )
        {
            qDebug("double click the empty fields col");
            return;
        }
        m_selCol = select_col;
        int i=0;
        for( i = 0 ; i < 4 ; ++i )
        {
            if( move2Free(i) )
            {
                break;
            }
        }
        if( i == 4 )
        {
            qDebug("error: no empty freecard!");
        }
        else 
        {
            autoplay();
        }
        m_selCol = EMPTY;
        update();
    }
}

CARD FC_MainFrame::getCard(int col)
{
    ASSERT( col != EMPTY );
    ASSERT( col >= 0 && col < 12 );

    CARD card = EMPTY;
    if( col >= 8 ) 
    {
        card = m_freecells[col-8];
    }
    else 
    {
        if(!m_cards[col].isEmpty())
            card = m_cards[col].last();
    }

    return card;
}

void FC_MainFrame::removeCol(int col)
{
    ASSERT( col != EMPTY );
    ASSERT( col >= 0 && col < 12 );
    if( col >= 8 ) 
    {
        m_freecells[col-8] = EMPTY;
    }
    else 
    {
        ASSERT(!m_cards[col].isEmpty());
        m_cards[col].remove(m_cards[col].fromLast());
    }
}

bool FC_MainFrame::move2Home(int homeCol, bool move)
{
    ASSERT( m_selCol != EMPTY );
    ASSERT( homeCol >=0 && homeCol < 4 );

    CARD& rdst = m_homecells[homeCol];
    CARD src = getCard(m_selCol);

    if( !fit_home(rdst, src) ) {
        return false;
    }
    else
    {
        if(!move) 
        {
            return true;
        }
        rdst = src;
        removeCol(m_selCol);
        return true;
    }
}

bool FC_MainFrame::supermove(int srcCol, int dstCol, bool move )
{
    ASSERT( srcCol >= 0 && srcCol < 8 );
    ASSERT( dstCol >= 0 && dstCol < 8 );
    ASSERT( dstCol != srcCol);

    QValueList<CARD>& cards = m_cards[m_selCol];
    ASSERT(!cards.isEmpty());

    CARD dst = EMPTY;
    if(!m_cards[dstCol].isEmpty() )
        dst = m_cards[dstCol].last();

    //check if there are enough space for supermove
    int avail_count = get_superMoveAavilableCount(dstCol);
    //qDebug("there are %d space for super move", avail_count);
    if( avail_count == 0 )
        return false;

    //get series cards from srcCol
    QValueList<CARD> series;
    QValueList<CARD>::Iterator it,it1;
    //reverse browse
    for( it = cards.fromLast(); it != cards.end() ; --it)
    {
       it1 = it;
       series.prepend(*it);
       if( --it1 == cards.end() 
               || !fit_fields(*it1, *it) 
               || (dst != EMPTY) && fit_fields(dst, *it)
               || series.count() == avail_count )
           break;
    }

    const CARD& rsrc = series.first();
    if(!fit_fields(dst, rsrc))
        return false;
    if(!move)
        return true;

    for( it = series.begin(); it != series.end() ; ++it)
    {
        cards.remove(*it);//here need care about invalid interator when remove
        m_cards[dstCol].append(*it);
    }
    return true;
}

int  FC_MainFrame::get_superMoveAavilableCount(int dst_col)
{
    ASSERT( dst_col >= 0 && dst_col < 8 );

    int freecount = 0;
    int empty_col = 0;

    for(int i = 0 ; i < 4 ; ++i )
        if(m_freecells[i] == EMPTY )
            freecount++;

    for(int j = 0 ; j < 8 ; ++j )
        if( m_cards[j].isEmpty() && j != dst_col )
            empty_col++;

    return (freecount + 1) * int( pow(2, empty_col) );
}

bool FC_MainFrame::move2Fields(int fieldCol, bool move)
{
    ASSERT( m_selCol != EMPTY );
    ASSERT( fieldCol >=0 && fieldCol < 8 );

    QValueList<int>& cards = m_cards[fieldCol];
    CARD src = getCard(m_selCol);
    ASSERT(src != EMPTY);
    CARD dst = getCard(fieldCol);

    if( m_selCol >= 8 )
    {//freecells -> fields
        if( !fit_fields(dst, src) )
            return false;
        if(!move)
            return true;
        cards.append(src);
        removeCol(m_selCol);
        return true;
    }
    else 
    {//fields->fields
        if( dst == EMPTY )
        {
            return supermove(m_selCol, fieldCol, move);
        }
        if( fit_fields(dst, src) )
        {
            if( !move )
                return true;
            cards.append(src);
            removeCol(m_selCol);
            return true;
        }
        else
        {
            return supermove(m_selCol, fieldCol, move);
        }
    }
}

bool FC_MainFrame::move2Free(int freeCol, bool move)
{
    ASSERT( freeCol >= 0 && freeCol < 4 );
    CARD& rdst = m_freecells[freeCol];
    if( rdst != EMPTY )
        return false;

    if( !move )
        return true;

    CARD src = getCard(m_selCol);
    ASSERT( src != EMPTY );
    rdst = src;
    removeCol(m_selCol);

    //record for undo
    if( m_selCol < 8 )
    {//fields -> free
        recorder.add_fields2free(m_selCol, freeCol, FC_Recorder::normal);
    }
    else 
    {//free -> free
        recorder.add_free2free(m_selCol-8, freeCol, FC_Recorder::normal);
    }

    return true;
}

void FC_MainFrame::autoplay()
{
    while( safe_autoplay() )
    {
        qDebug("safe autoplay once!");
    }
}

bool FC_MainFrame::safe_autoplay()
{
    //first search homecells found all fit cards
    QValueList<CARD> fitCards;

    int selCol_org = m_selCol;
    //then search all fields for fit cards
    for(int i = 0 ; i < 12 ; ++i )
    {
        CARD card = getCard(i);
        if(card == EMPTY)
            continue;

        m_selCol = i;
        if( value(card) == 0 || value(card) == 1 )
        {//A or 2
           for(int j = 0 ; j < 4 ; ++j )
           {
               if(move2Home(j) ) 
               {
                   m_selCol = selCol_org;
                   return true;
               }
           }
        }
        else 
        {
            for(int j = 0; j < 4 ; ++j )
            {
                if( move2Home(j, false) && isSafeMoveHome(card) )
                {
                    move2Home(j);
                    m_selCol = selCol_org;
                    return true;
                }
            }
        }
    }
    m_selCol = selCol_org;
    return false;
}

bool FC_MainFrame::isSafeMoveHome(CARD card)
{
    int count = 0;

    for(int i = 0 ; i < 4 ; ++i )
    {
        if( (isBlack(m_homecells[i]) ^ isBlack(card)) && value(m_homecells[i]) >= value(card)-1 )
            count++;
    }

    if( count == 2 )
        return true;
    return false;
}

void FC_MainFrame::new_game()
{
    qDebug("new_game");
    static bool first = true;
    if( !first && !queryUser() )
    {
        return;
    }
    first = false;

    clear();

    random_seed();

    if(!shuffle(m_seed))
        return;
    update();

}
void FC_MainFrame::restart_game()
{
    qDebug("restart_game");
    if( !queryUser() )
        return;
    clear();
    if(!shuffle(m_seed))
        return;
    update();
}

void FC_MainFrame::seed_game()
{
    qDebug("seed_game");
    if( !queryUser() )
        return;
    FC_ChooseSeedDlg dlg;
    int ret = dlg.exec();
    if(!ret)
        return;
    m_seed = dlg.getSeed();
    qDebug("m_seed is %d", m_seed);

    clear();

    if(!shuffle(m_seed))
        return;
    update();

        
}

void FC_MainFrame::undo()
{
    qDebug("undo");
    FC_Recorder::MoveActions actions;
    recorder.undo(actions);
    const FC_Recorder::MOVE_ACTION a = actions.top();
    if( a.src == FC_Recorder::freecell && a.dst == FC_Recorder::fields )
    {
        m_cards[a.dst_col].append(m_freecells[a.src_col]);
        m_freecells[a.src_col] = EMPTY;
        update();
    }
    else if( a.src == FC_Recorder::freecell && a.dst == FC_Recorder::freecell )
    {
        
        m_freecells[a.dst_col] = m_freecells[a.src_col];
        m_freecells[a.src_col] = EMPTY;
        update();
    }
    else if( a.src == FC_Recorder::fields && a.dst == FC_Recorder::freecell )
    {
        
        m_freecells[a.dst_col] = m_cards[a.src_col].last();
        m_cards[a.src_col].remove(m_cards[a.src_col].fromLast());
        update();
    }
    else 
    {
        ASSERT(FALSE);
    }
}

bool FC_MainFrame::queryUser()
{
    static RES_ICON_Reader iconReader;
    static QPixmap icon = iconReader.getIcon("Dialog_Question_Mark.gif");
    ASSERT( !icon.isNull() );

    int ret  = ZMessageBox::information(this, 
                            icon,
                            "Exit this game?",
                            "Yes",
                            "No");
    return (ret == 0);
}

void FC_MainFrame::random_seed()
{
    QTime time = QTime::currentTime();
    srand(time.msec());
    m_seed = int ( rand()*1.0 / RAND_MAX * MAX_SEED ); 
}

void FC_MainFrame::mouseReleaseEvent( QMouseEvent* e )
{
#if ENABLE_LEFTBTN_HOLD

    if( e->button() != Qt::LeftButton )
        return;

    if( !m_fieldPos.isEmpty() )
    {
        m_fieldPos.setEmpty();
        update();
    }
#endif
    return QWidget::mouseReleaseEvent(e);
}
