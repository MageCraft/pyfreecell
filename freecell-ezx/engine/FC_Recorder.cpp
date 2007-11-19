#include "FC_Recorder.h"
#include <qtl.h>

FC_Recorder::FC_Recorder()
{

}

FC_Recorder::~FC_Recorder()
{

}

void FC_Recorder::add(const MOVE_ACTION& action)
{
    actions.push(action);
}

void FC_Recorder::add(MOVE_POS src, int src_col, MOVE_POS dst, int dst_col, MOVE_TYPE type)
{
    MOVE_ACTION action;
    action.src = src;
    action.src_col = src_col;
    action.dst = dst;
    action.dst_col = dst_col;
    action.type = type;

    add(action);
}
        
void FC_Recorder::add_free2free(int src_col, int dst_col, MOVE_TYPE type)
{
    MOVE_ACTION action;
    action.src = freecell;
    action.src_col = src_col;
    action.dst = freecell;
    action.dst_col = dst_col;
    action.type = type;
    
    add(action);
}

void FC_Recorder::add_free2fields(int src_col, int dst_col, MOVE_TYPE type)
{
    MOVE_ACTION action;
    action.src = freecell;
    action.src_col = src_col;
    action.dst = fields;
    action.dst_col = dst_col;
    action.type = type;
    
    add(action);

}

void FC_Recorder::add_free2home(int src_col, int dst_col, MOVE_TYPE type)
{
    MOVE_ACTION action;
    action.src = freecell;
    action.src_col = src_col;
    action.dst = homecell;
    action.dst_col = dst_col;
    action.type = type;

    add(action);

}

void FC_Recorder::add_fields2free(int src_col, int dst_col, MOVE_TYPE type)
{
    MOVE_ACTION action;
    action.src = fields;
    action.src_col = src_col;
    action.dst = freecell;
    action.dst_col = dst_col;
    action.type = type;
    
    add(action);

}

void FC_Recorder::add_fields2home(int src_col, int dst_col, MOVE_TYPE type)
{
    MOVE_ACTION action;
    action.src = fields;
    action.src_col = src_col;
    action.dst = homecell;
    action.dst_col = dst_col;
    action.type = type;
    
    add(action);
}

void FC_Recorder::add_fields2fields(int src_col, int dst_col, MOVE_TYPE type)
{
    MOVE_ACTION action;
    action.src = fields;
    action.src_col = src_col;
    action.dst = fields;
    action.dst_col = dst_col;
    action.type = type;
    
    add(action);
}

void FC_Recorder::undo(MoveActions& actions)
{
    if( this->actions.isEmpty() )
        return;

    MOVE_ACTION& a = this->actions.top();
    if( a.type == normal )
    {
        actions.push( a.reverse() );
        this->actions.pop();
        return;
    }
    else if( a.type == supermove )
    {
        actions.push( a.reverse() );
        this->actions.pop();
        undo(actions);
    }
    else if( a.type == safe_autoplay )
    {
        actions.push( a.reverse() );
        this->actions.pop();
        undo(actions);
    }
    else 
    {
        ASSERT(FALSE);
    }
}

FC_Recorder::MOVE_ACTION& FC_Recorder::MOVE_ACTION::reverse()
{
    qSwap(src, dst);
    qSwap(src_col, dst_col);
    return *this;
}
