#ifndef __FC_CONTAINER_H__
#define __FC_CONTAINER_H__

#include <ZMainWidget.h>

class UTIL_CST;
class FC_MainFrame;
class QPopupMenu;

class FC_Container : public ZMainWidget
{
    Q_OBJECT
    public:
        FC_Container();
        ~FC_Container();

    private:
        UTIL_CST* cst;
        FC_MainFrame* content;
        QPopupMenu* menu;

    protected slots:
        void menuShow();

};

#endif /*__FC_CONTAINER_H__*/
