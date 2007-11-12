#include "rs_engine.h"
#include "blocks.h"
#include <qtimer.h>
#include <qdatetime.h>

#include <qwidget.h>



//libc
//#include <math.h>
#include <stdlib.h>
#include <time.h>

RS_Engine::RS_Engine(QObject* parent, const char* name )
    : QObject(parent, name), timer(NULL), level(DEFAULT_LEVEL), block(NULL), units(MAX_COL, MAX_ROW, 0, 1)
{
    init();
}

RS_Engine::~RS_Engine()
{

}

inline void RS_Engine::updateUI()
{
    emit update();
}

void RS_Engine::init()
{
    clear();
    timer = new QTimer(this);
    connect( timer, SIGNAL( timeout() ), this, SLOT( timeout() ) );
    srand(time(0));
}

void RS_Engine::clear()
{
    units.clear();
    level = DEFAULT_LEVEL;
}

void RS_Engine::start(bool autoplay)
{
    qDebug("start");
    ASSERT( !autoplay );

    CHECK_PTR( timer );
    if( timer->isActive() )
    {
        timer->stop();
    }

    new_block();
    updateUI();
    timer->start(1000);
}

void RS_Engine::timeout()
{
   //qDebug("timeout");
    CHECK_PTR(block);

    if( block->isOver() )
    {
        start();
        return;
    }
    moveDown();
}

void RS_Engine::pause()
{
    //qDebug("pause");
    CHECK_PTR( timer );
    timer->stop();
}

void RS_Engine::stop()
{
    qDebug("stop");
    CHECK_PTR( timer );
    timer->stop();
}

void RS_Engine::setLevel(int level)
{

}

void RS_Engine::moveLeft()
{
    //qDebug("move left");
    if( block->left() == 0 )
        updateUI();
}

void RS_Engine::moveRight()
{
    //qDebug("move right");
    if( block->right() == 0 )
        updateUI();
}

void RS_Engine::moveDown()
{
    //qDebug("move down");
    if( block->down() == 0 )
        updateUI();
}

void RS_Engine::quickDown()
{
    //qDebug("quick down");
    block->drop();
    updateUI();
    if(units.getFullLineCount() == 0)
    {
        start();
    }
    else
    {
        timer->stop();
        QTimer::singleShot(200, this, SLOT(doShake1()));
    }
}

void RS_Engine::transform()
{
    //qDebug("transform");
    if( block->transform() == 0 )
        updateUI();
}

//
// generate a randmn number [min,max]
int myRand(int max, int min=0)
{
    while( true )
    {
        int r = rand();
        if( r != RAND_MAX )
            return int( (r*1.0/RAND_MAX*(max-min)) + min );
    }
}

void RS_Engine::new_block()
{
    if( block != NULL )
    {
        BlockFactory::destroyBlock( block );
    }

    BlockType newType = (BlockType)myRand(7);
    int unit_value = myRand(6);
    qDebug("type:%d, color:%d", newType, unit_value);
    block = BlockFactory::createBlock( newType , unit_value , units );
}

void RS_Engine::doShake1()
{
    units.flagFullLines();
    updateUI();
    QTimer::singleShot(200, this, SLOT(doShake2()));
}

void RS_Engine::doShake2()
{
    units.removeFullLines();
    updateUI();
    start();
}
