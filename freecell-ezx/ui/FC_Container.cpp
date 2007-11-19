#include "FC_Container.h"
#include "FC_MainFrame.h"
#include <UTIL_CST.h>
#include <ZPushButton.h>
#include <qfont.h>
#include <qpopmenu.h>
#include <qapplication.h>


FC_Container::FC_Container()
    : ZMainWidget(false,0)
{
    QFont font = qApp->font();
    font.setPointSize( DEFAULT_FONT_SIZE_MEDIUM);

    cst = new UTIL_CST(this, QObject::tr("freecell","2.26.1;CST_4BUTTON"));
    this->setCSTWidget(cst);
    cst->getLeftBtn()->setEnabled(true);
    cst->getRightBtn()->setResourceID("CST_Exit");

    connect( cst->getRightBtn(), SIGNAL(clicked()), qApp, SLOT(quit()) );
    connect( cst->getLeftBtn(), SIGNAL(clicked()), this, SLOT(menuShow()) );

    content = new FC_MainFrame(this);
    this->setContentWidget(content);

    //pop menu
    menu = new QPopupMenu(this);
    menu->insertItem(tr("New game", "1.1.2.2;MENU"), content, SLOT(new_game()) );
    menu->insertItem(tr("Restart game", "1.1.2.2;MENU"), content, SLOT(restart_game()) );
    menu->insertItem(tr("New game with seed...", "1.1.2.2;MENU"), content, SLOT(seed_game()) );
    menu->insertSeparator();
    menu->insertItem(tr("Undo move", "1.1.2.2;MENU"), content, SLOT(undo()));
    menu->insertSeparator();
    menu->insertItem(tr("Exit", "1.1.2.2;MENU"), qApp, SLOT(quit()) );
    
}

FC_Container::~FC_Container()
{

}

void FC_Container::menuShow()
{
    ZPushButton *menuButton  = cst->getLeftBtn();
    menu->exec(menuButton->mapToGlobal(menuButton->rect().topLeft() - QPoint(0, menu->sizeHint().height())));
}
