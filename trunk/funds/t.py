#!/usr/bin/env python
# -*- coding: utf-8 -*-

(align_left, align_right, align_middle) = range(3)

#header must have following format:
#(text, length, align, data_align)

class PrintTable:
    def __init__(self, headers=None, rows=None):
        self.headers = headers
        if rows is None:
            self.rows = []
        else:
            self.rows = rows

    def set_headers(self, headers):
        self.headers = headers

    def append_row(self, row):
        self.rows.append(row)

    def line_str(self):
        return '-' * ( sum([h[1] for h in headers])  + len(headers) + 1 ) + '\n'


    def output(self):
        s = ''
        s += self.line_str()
        s += self.header_str() 
        s += self.line_str()
        s += self.rows_str()
        s += self.line_str()
        print s
        
    def header_str(self):
        s = ''
        s += '|'
        for header in headers:
            text, length, align = header[:-1]
            s += self.cell_str(text, length, align)
            s += '|'
        return s + '\n'

    def rows_str(self):
        s = ''
        for row in self.rows:
            s += '|'
            for col in range(len(row)):
                header = headers[col]
                text, length, align = row[col], header[1], header[-1]
                s += self.cell_str(text, length, align) 
                s += '|'
            s += '\n'
        return s

    def cell_str(self, text, length, align):
        L = len(text)
        assert( L <= length )
        s = None
        ch = ' '
        if align == align_right:
            s = ch* (length-L) + text
        elif align == align_left:
            s = text + ch* (length-L)
        else:
            l1 = (length-L) / 2 
            l2 = length-l1-L
            s = ch*l1 + text + ch*l2
        return s 


if __name__ == '__main__':
    headers = []
    headers.append( ('代码', 10, align_middle, align_middle) )
    headers.append( ('名称', 10, align_middle, align_middle) )
    headers.append( ('份额', 10, align_middle, align_middle) )
    headers.append( ('本金', 10, align_middle, align_middle) )
    headers.append( ('净值', 8, align_middle, align_middle) )
    headers.append( ('涨跌', 8, align_middle, align_middle) )
    headers.append( ('当前金额', 10, align_middle, align_middle) )
    t = PrintTable(headers)
    #t.output_cell('你好', 8, align_left)
    #t.output_cell('你好', 8, align_middle)
    #t.output_cell('你好', 9, align_middle)
    row = ('400003', '东方精选', '20000.00', '20000.00', '1.009', '1.27%', '21500.00')
    t.append_row( row )
    t.append_row( row )
    t.output()

