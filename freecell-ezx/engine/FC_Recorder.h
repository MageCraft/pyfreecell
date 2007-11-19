#ifndef __FC_RECORDER_H__
#define __FC_RECORDER_H__

#include <qvaluestack.h>

class FC_Recorder
{
    public:
        FC_Recorder();
        ~FC_Recorder();

        enum MOVE_POS { freecell, homecell, fields };
        enum MOVE_TYPE { normal, supermove, safe_autoplay };

        struct MOVE_ACTION {
            MOVE_POS src;
            int src_col;
            MOVE_POS dst;
            int dst_col;
            MOVE_TYPE type;

            MOVE_ACTION& reverse();
        };
        typedef QValueStack<MOVE_ACTION> MoveActions;

        void add(const MOVE_ACTION& action);
        void add(MOVE_POS src, int src_col, MOVE_POS dst, int dst_col, MOVE_TYPE type=normal);
        
        void add_free2free(int src_col, int dst_col, MOVE_TYPE type=normal);
        void add_free2home(int src_col, int dst_col, MOVE_TYPE type=normal);
        void add_free2fields(int src_col, int dst_col, MOVE_TYPE type=normal);
        void add_fields2free(int src_col, int dst_col, MOVE_TYPE type=normal);
        void add_fields2home(int src_col, int dst_col, MOVE_TYPE type=normal);
        void add_fields2fields(int src_col, int dst_col, MOVE_TYPE type=normal);

        void undo(MoveActions& actions);

    private:
        MoveActions actions;
};


#endif /*__FC_RECORDER_H__*/

