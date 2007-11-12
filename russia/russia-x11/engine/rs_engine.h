#ifndef __RS_ENGINE_H__
#define __RS_ENGINE_H__

#include <qobject.h>
#include <qcolor.h>
#include "unitworld.h"
#include "blocks.h"

#define MAX_ROW 20
#define MAX_COL 10

#define DEFAULT_LEVEL 1

class QTimer;
class Block;
class RS_Engine : public QObject
{
    Q_OBJECT
    public:
        RS_Engine(QObject* parent = 0, const char* name = 0 );
        virtual ~RS_Engine(); 

        UnitWorld& data() { return units; }

    protected:
        void init();
        void clear();
        void new_block();
        void updateUI();

    private:
        QTimer* timer;
        int   level;
        Block* block;
        UnitWorld units;
        bool running;
        
    public slots:
        void start(bool autoplay=false);
        void pause();
        void stop();
        void setLevel(int level);

        void moveLeft();
        void moveRight();
        void moveDown();
        void quickDown();
        void transform();

    protected slots:
        void timeout();
        void doShake1();
        void doShake2();

    signals:
        void update();
};

#endif /* __RS_ENGINE_H__ */



