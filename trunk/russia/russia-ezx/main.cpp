#include "mainwindow.h"
#include "view.h"
#include <qapplication.h>
#include <ZApplication.h>
#include <ZKbMainWidget.h>
#include <qt.h>


int main( int argc, char** argv )
{
    //ZApplication a( argc, argv );
    QApplication a( argc, argv );

    /*
    ZKbMainWidget mw;
    mw.setFullScreenMode(true);
    RS_View* v = new RS_View(&mw);
    mw.setContentWidget(v);
    mw.show();
    */

    RS_View v;
    v.show();
    
    a.connect( &a, SIGNAL(lastWindowClosed()), &a, SLOT(quit()) );

    return a.exec();
}
