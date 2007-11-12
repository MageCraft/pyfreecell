#include "mainwindow.h"
#include "view.h"


MainWindow::MainWindow()
    : QMainWindow()
{
    RS_View* view = new RS_View(this);
    view->setFocus();
    setCentralWidget(view);

    setFixedSize(176,220);
}

MainWindow::~MainWindow()
{

}
