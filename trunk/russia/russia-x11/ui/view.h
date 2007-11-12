#ifndef __UI_VIEW_H__
#define __UI_VIEW_H__

#include <qwidget.h>

class RS_Engine;
class QPainter;
class RS_View : public QWidget
{
    public:
        RS_View(QWidget* parent = 0, const char* name = 0, WFlags f = 0);
        ~RS_View();

    protected:
        virtual void paintEvent( QPaintEvent* );
        void paintBkgnd( QPainter* );
        void paintForegnd( QPainter* );
        void draw3dRect(QPainter*, const QRect& rt, const QColor& Clr1, const QColor& Clr2);
        void drawBlock(QPainter*, const QRect& rt, const QColor& bkClr, const QColor& Clr1, const QColor& Clr2);
        
        virtual void keyPressEvent( QKeyEvent* );

    private:
        void init();
        RS_Engine* engine();

    private:
        RS_Engine* _engine;
};
#endif /*__UI_VIEW_H__*/
