#!/usr/bin/env python

from common import *
import pdb

class Engine:
    def __init__(self, free, home, field, selection):
        self.free = free
        self.home = home
        self.field = field 
        self.selection = selection
        self.notify = None
        self.super_notify = None

    def set_notify(self, func):
        self.notify = func

    def set_super_move_notify(self, func):
        self.super_notify = func

    def get_free(self):
        empty_free=[]
        for i in range(len(self.free)):
            if is_empty(self.free[i]):
                empty_free.append(i)
        return empty_free

    def get_empty_field(self, dst_col):
        empty_field = []
        for i in range(len(self.field)):
            if is_empty(self.field[i]) and i is not dst_col:
                empty_field.append(i)
        return empty_field

    def get_super_move_availcount(self, empty_free, empty_field):
        m = len(empty_free)
        n = len(empty_field)
        return (n+1)*(2*m+n)/2 + 1

    def field2free(self, src_col, dst_col):
        assert( is_empty(self.free[dst_col]) )
        assert( not_empty(self.field[src_col]) )
        self.free[dst_col] = self.field[src_col][-1]
        self.field[src_col].pop()

    def free2field(self, src_col, dst_col):
        assert(self.free[src_col] != EMPTY)
        assert(fit_field(self.field[dst_col][-1], self.free[src_col]))
        self.field[dst_col].append(self.free[src_col])
        self.free[src_col] = EMPTY

    def field2field(self, src_col, dst_col):
        self.field[dst_col].append(self.field[src_col].pop())

    def dump(self):
        print self.free, self.home
        print self.field

    def super_move_pack(self, empty_free, empty_field, src_col, v, stack):
        #pdb.set_trace()
        done = lambda: is_empty(self.field[src_col]) or self.field[src_col][-1] == v
        if done(): return
        #move cards to empty_free first
        for col in empty_free:
            self.field2free(src_col, col)
            self.dump()
            stack.insert(0, (FIELD, src_col, FREE, col))
            if done(): return

        #move cards to empty_field from left to right
        for col in empty_field:
            self.field2field(src_col, col)
            self.dump()
            stack.insert(0, (FIELD, src_col, FIELD, col))
            if done(): return

        #move cards from (n-2),(n-3),...,0 to n-1 col
        l = empty_field[:-1]
        l.reverse()
        for col in l:
            self.field2field(col, empty_field[-1])
            self.dump()
            stack.insert(0, (FIELD, col, FIELD, empty_field[-1]) )

        #move card from free 2 field, from right to left
        l = empty_free[:]
        l.reverse()
        for col in l:
            self.free2field(col, empty_field[-1])
            self.dump()
            stack.insert(0, (FREE, col, FIELD, empty_field[-1]) )

        empty_field.pop()
        #call me again
        self.super_move_pack(empty_free, empty_field, src_col, v, stack)

    def super_move_unpack(self, stack, old_src_col, new_src_col):
        #pdb.set_trace()
        opt_map = { (FREE,FIELD):self.free2field, 
                    (FIELD,FIELD):self.field2field, 
                    (FIELD,FREE):self.field2free 
                  }
        for step in stack:
            src_area, src_col, dst_area, dst_col = step
            if src_area == FIELD and src_col == old_src_col:
                src_col = new_src_col
            #unpack, reverse step, move from dst to src
            opt = opt_map[(dst_area,src_area)]
            opt(dst_col, src_col)
            self.dump()

    def super_move(self, src_col, dst_col):
        #pdb.set_trace()
        assert( len(self.field[src_col]) != 0 )
        empty_free = self.get_free()
        empty_field = self.get_empty_field(dst_col)
        avail_count = self.get_super_move_availcount(empty_free, empty_field)
        series = []
        src = self.field[src_col]
        dst = self.field[dst_col]
        dst_v = EMPTY
        if not_empty(dst):
            dst_v = dst[-1]

        for row in range(len(src)-1, -1, -1):
            row1 = row
            series.insert(0, src[row])
            #series.append(src[row])
            row1 -= 1
            if row1 < 0 or \
               not fit_field(src[row1], src[row]) or \
               (dst_v != EMPTY and fit_field(dst_v, src[row])) or \
               len(series) is avail_count :
                   break;
        src_v = series[0]
        if not fit_field(dst_v, src_v):
            return False
        #begin super move
        self.idle()
        stack=[]
        self.super_move_pack(empty_free, empty_field, src_col, src_v, stack)
        #move show card to dst_col
        assert( self.field[src_col][-1] == src_v )
        self.field2field(src_col, dst_col)
        self.super_move_unpack(stack, src_col, dst_col)
        return True

    def select(self, area, col):
        opt_map = { 
                    FREE: self.on_select_free,
                    HOME: self.on_select_home,
                    FIELD: self.on_select_field
                  }
        opt_map[area](col)

    def is_safe_autoplay(self, v):
        if value(v) == 0 or value(v) == 1:
            return True #ace or 2
        home = self.home
        cout = 0
        for i in home:
            if is_black(i) ^ is_black(v) and value(i) >= value(v)-1:
                cout += 1
        if cout == 2:
            return True
        else: 
            return False
        
    def auto_play(self):
        free, home, field = self.free, self.home, self.field
        auto = False
        #freecell
        for k in range(len(free)):
            for v in range(len(home)):
                if fit_home(home[v],free[k]) and self.is_safe_autoplay(free[k]):
                    home[v] = free[k]
                    free[k] = EMPTY
                    auto = True
        #field
        for col in field:
            if is_empty(col): continue
            for i in range(len(home)):
                if fit_home(home[i], col[-1]) and self.is_safe_autoplay(col[-1]):
                    home[i] = col.pop()
                    auto = True

        if auto: self.auto_play() #call me again, until can't autoplay

    def idle(self):
        self.selection['area'] = IDLE

    def on_select_free(self, col):
        notify, auto = False, False
        src_col = self.selection['col']
        sel = self.selection
        if sel['area'] is IDLE:
            print 'free, idle'
            if self.free[col] is EMPTY: return
            sel['area'] = FREE
            sel['col'] = col
            notify = True
        elif sel['area'] is FREE:
            print 'free 2 free'
            if self.free[col] is not EMPTY:
                if src_col is col: # select again
                    pass #self.idle()
                else: 
                    print 'can not move'
                    return
            else:
                self.free[col] = self.free[src_col]
                self.free[src_col] = EMPTY
            self.idle()
            notify, auto = True, False
        elif sel['area'] is HOME:
            print 'home 2 free, impossible, undo later'
            pass 
            return
        elif sel['area'] is FIELD:
            print 'field 2 free'
            if self.free[col] is not EMPTY: return
            dst_v = self.field[src_col][-1]
            self.free[col] = dst_v
            self.field[src_col].pop()
            self.idle()
            notify, auto = True, True
            #auto_play()
        else:
            assert(False)

        if auto: self.auto_play()
        if notify: self.notify()

    def on_select_home(self, col):
        #pdb.set_trace()
        notify, auto = False, False
        src_col = self.selection['col']
        dst_v = self.home[col]
        if self.selection['area'] is IDLE:
            print 'point home'
            pass
            return
        elif self.selection['area'] is FREE:
            print 'free 2 home'
            src_v = self.free[src_col]
            if fit_home(dst_v, src_v):
                self.home[col] = src_v
                self.free[src_col] = EMPTY
                self.idle()
                notify, auto = True, True
            else:
                print 'can not move'
                pass
                return
        elif self.selection['area'] is HOME:
            print 'home 2 home, impossible'
            pass
            return
        elif self.selection['area'] is FIELD:
            print 'field 2 home'
            src_v = self.field[src_col][-1]
            if fit_home(dst_v, src_v):
                self.home[col] = src_v
                self.field[src_col].pop()
                self.idle()
                notify, auto = True, True
            else:
                print 'can not move'
                pass
                return
        else:
            assert(False)

        if auto: self.auto_play()
        if notify: self.notify()
                
    def on_select_field(self, col):
        #pdb.set_trace()
        field = self.field
        sel = self.selection
        src_col = sel['col']
        notify, auto = False, False
        if sel['area'] is IDLE:
            print 'field, idle'
            assert( not_empty(field[col]) )
            sel['area'] = FIELD
            sel['col'] = col
            notify, auto = True, False
        elif sel['area'] is FREE:
            print 'free 2 field'
            assert( not_empty(field[col]) )
            if fit_field(field[col][-1], self.free[src_col]):
                field[col].append(self.free[src_col])
                self.free[src_col] = EMPTY
                self.idle()
                notify, auto = True, True
            else:
                print 'can not move'
                pass
                return
        elif sel['area'] is FIELD:
            print 'field 2 field'
            if src_col is col:
                pass #select again, need tell row later
                auto = False
            else:
                if self.super_move(src_col, col):
                    pass
                    auto = True
                else:
                    print 'can not move'
                    return
            self.idle()
            notify = True
        else:
            assert( False )

        if auto: self.auto_play()
        if notify: self.notify()


