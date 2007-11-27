#!/usr/bin/env python
# -*- coding: utf-8 -*-


EMPTY = -1
GRAY  = -2


class Unit: 
    def __init__(self, value=EMPTY):
        self.value = value

class Pos:
    def __init__(self, x=Empty, y=Empty):
        self.x = x
        self.y = y

    def left(self, dx=1): return Pos(self.x-dx, self.y)
    def right(self, dx=1): return Pos(self.x+dx, self.y)
    def above(self, dy=1): return Pos(self.x, self.y-dy)
    def below(self, dy=1): return Pos(self.x, self.y+dy)
    def move(self,dx,dy):
        self.x += dx
        self.y += dy
        return self

class RS_Column:
    def __init__(self, size, init):
        self.init = init
        self.data = [ self._get_init(i) for i in range(size)]

    def _get_init(self, index):
        if callable(self.init):
            return self.init(index)
        return self.init

    def __getitem__(self, index):
        return self.data[index]
    def __setitem__(self, index, value):
        self.data[index] = value
    def __delitem__(self, index):
        del self.data[index]
        self.data.append(self._get_init(len(self.data)))
    def __repr__(self):
        return self.data.__repr__()
    def __len__(self):
        return self.data.__len__()

class UnitWorld:
    def __init__(self, max_col, max_row, min_col=0, min_row=0):
        self.units = []
        self.full_lines = []
        self.max_col = max_col
        self.max_row = max_row

        #matrix
        for i in range(max_col):
            self.units.append(RS_Column(self.max_row, Unit(EMPTY)))

    def init(self):
        pass

    def clear(self):
        for col in self.units:
            for u in col:
                u.value = EMPTY

    def dump(self):
        for col in self.units:
            func = lambda v: v!=EMPTY and "1" or "0"
            print "\t".join(map(func, col))

    def dump_with_color(self):
        for col in self.units:
            print "\t".join(map(str, col))

    def __repr__(self):
        self.dump()

    def set_empty(self, x,y): 
        self.units[x][y].value = EMPTY

    def is_empty(self, x,y): 
        return self.units[x][y].value == EMPTY

    def value(self, x,y): 
        return self.units[x][y].value

    def set_value(self, x,y, value): 
        self.units[x][y].value = value

    def check_full_lines(self):
        assert( self.full_lines.__len__() == 0 )
        for r in range(self.max_row-1, -1, -1):
            row = self.get_row(r)
            count = len( filter(lambda v: v == EMPTY, row) )
            if count == self.max_col: 
                break;
            if count == 0:
                self.full_lines.append(r)

    def get_row(self, row):
        return map(lambda col: col[row], self.units)

    def get_full_line_count(self): 
        return len(self.full_lines)

    def flag_full_lines(self):
        for row in self.full_lines:
            self._gray_line(row)

    def remove_full_lines(self):
        for l in self.full_lines:
            self._remove_row(l)
        self.full_lines = []
            
    #private
    def _gray_line(self,row):
        for col in self.units:
            col[row] = GRAY

    def _remove_row(self, row):
        for col in self.units:
            del col[row]
