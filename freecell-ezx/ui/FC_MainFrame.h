#ifndef __FC_MAINFRAME_H__
#define __FC_MAINFRAME_H__

#include <qwidget.h>
#include "FC_Recorder.h"

#define EMPTY  -1
typedef int CARD;

class CardsLoader;
class FC_MainFrame : public QWidget
{
    Q_OBJECT
    public:
        FC_MainFrame(QWidget* parent = 0, const char* name = 0 );
        virtual ~FC_MainFrame();
        bool init();

    protected:
        virtual void mousePressEvent( QMouseEvent* e );
        virtual void mouseReleaseEvent( QMouseEvent* e ); 
        virtual void mouseDoubleClickEvent(QMouseEvent* e);
        virtual void paintEvent(QPaintEvent* e);
        virtual void paintCards(QPainter& painter);
        virtual void paintUpView(QPainter& painter);

        bool shuffle(int seed);
        void draw3dRect(QPainter& painter, const QRect& rect, const QColor& clr1, const QColor& clr2);
        void clear();

        bool move2Home(int homeCol, bool move = true);
        bool move2Fields(int feildCol, bool move = true);
        bool move2Free(int freeCol, bool move = true);
        bool supermove(int srcCol, int dstCol, bool move = true);
        int  get_superMoveAavilableCount(int dst_col);
        void autoplay();
        bool safe_autoplay();
        bool isSafeMoveHome(CARD card);

        CARD getCard(int col);
        void removeCol(int col);

        bool queryUser();
        void random_seed();

    protected slots:
        void new_game();
        void restart_game();
        void seed_game();
        void undo();

    private:
        CardsLoader* m_cardLoader;
        FC_Recorder recorder;
        QValueList<CARD> m_cards[8];
        CARD  m_freecells[4];
        CARD  m_homecells[4];

        QRect m_rtFreecells;
        QRect m_rtHomecells;
        QRect m_rtFields;
        QRect m_rtFlag;

        int   m_selCol; 
        int   m_seed;

        struct FieldsPos {
            int col;
            int row;
            bool isEmpty() const { return row == EMPTY && col == EMPTY; }
            void setEmpty() { row = EMPTY ; col = EMPTY; }
            void setPos(int _col, int _row ) { row = _row ; col = _col; }
        };

        FieldsPos m_fieldPos;
};

#endif /*__FC_MAINFRAME_H__*/


