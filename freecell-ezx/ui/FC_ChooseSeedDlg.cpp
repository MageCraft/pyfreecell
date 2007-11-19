#include "FC_ChooseSeedDlg.h"
#include <UTIL_DlgCST.h>
#include <qlineedit.h>
#include <qlabel.h>
#include <qlayout.h>
#include <qvalidator.h>
//#include <qtabbar.h>



FC_ChooseSeedDlg::FC_ChooseSeedDlg(QWidget* parent, const char* name, WFlags f)
    : UTIL_Dialog(UTIL_Dialog::DialogBC, TRUE, parent, name, 1, f ) 
{
    setDlgTitle("Input a seed value");

    //OK and Cancel buttons
    UTIL_DlgCST* cst = new UTIL_DlgCST(this, UTIL_DlgCST::Cst2a);
    cst->getBtn2()->setText(tr("Cancel", "2.1.16;SOFTKEY_2BUTTON"));
    cst->getBtn1()->setText(tr("OK",     "2.1.16;SOFTKEY_2BUTTON"));
    setDlgCst(cst);

    connect(cst->getBtn2(), SIGNAL(clicked()), this, SLOT(reject()));
    connect(cst->getBtn1(), SIGNAL(clicked()), this, SLOT(accept()));

    //content
    QWidget* content   = new QWidget(this);
    QVBoxLayout* vbox  = new QVBoxLayout(content);
    //QTabBar* bar = new QTabBar(content);

    QLabel* label   = new QLabel("Seed value:(1 - 32000)", content);
    edit = new QLineEdit(content);
    QIntValidator* v = new QIntValidator(1, 32000, edit);
    edit->setValidator(v);
    edit->setAlignment( QLineEdit::AlignRight );
    edit->setMaxLength(5);
    edit->setText("32000");
    edit->selectAll();

    //vbox->addWidget(bar,  0, Qt::AlignVCenter | Qt::AlignHCenter);
    vbox->addWidget(label,0, Qt::AlignVCenter | Qt::AlignHCenter);
    vbox->addWidget(edit, 0, Qt::AlignVCenter | Qt::AlignHCenter);


    setDlgContent(content);
}

FC_ChooseSeedDlg::~FC_ChooseSeedDlg()
{

}

int FC_ChooseSeedDlg::getSeed() const
{
    qDebug( "seed is %s", edit->text().latin1() );
    return edit->text().toUInt();
}

