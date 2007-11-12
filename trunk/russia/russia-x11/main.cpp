#include "mainwindow.h"
#include "view.h"
#include <qapplication.h>
#include <qt.h>


int main( int argc, char** argv )
{
    QApplication a( argc, argv );
    a.setStyle("Windows");

    RS_View mw;
    mw.setFixedSize(176, 220);
    mw.show();
    
    a.connect( &a, SIGNAL(lastWindowClosed()), &a, SLOT(quit()) );

    return a.exec();
}
