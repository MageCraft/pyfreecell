
#include <ZApplication.h>
#include "FC_Container.h"
#include <qstring.h>

int main( int argc, char* argv[])
{
    ZApplication a( argc, argv );
    FC_Container c;
    a.connect( &a, SIGNAL(lastWindowClosed), &a, SLOT(quit()) );
    c.show();
    return a.exec();
}
