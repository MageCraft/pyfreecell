#!/usr/bin/env python
# -*- coding: utf-8 -*-

from itertools import imap


def Matrix(col, row, initial=None):
    matrix = []
    for x in range(col): 
        col = []
        for y in range(row):
            if callable(initial): 
                col.append(initial(x,y))
            else:
                col.append(initial)
        matrix.append(col)
    return matrix

def dump_matrix(matrix):
    for col in matrix:
        print "\t".join(imap(str, col))


if __name__ == '__main__':
    matrix1 = Matrix(10,20, lambda x,y: x+y)
    matrix2 = Matrix(20,10, None)
    for m in (matrix1, matrix2):
        dump_matrix(m)

