#ifndef __FC_CHOOSE_SEED_DLG_H__
#define __FC_CHOOSE_SEED_DLG_H__

#include <UTIL_Dialog.h>

class QLineEdit;
class FC_ChooseSeedDlg : public UTIL_Dialog
{
    public:
        FC_ChooseSeedDlg(QWidget* parent = 0, const char* name = 0, WFlags f = 0 );
        ~FC_ChooseSeedDlg();

        int getSeed() const;
    private:
        void init();
        QLineEdit* edit;
};
#endif /* __FC_CHOOSE_SEED_DLG_H__ */


