#!/usr/bin/env python
# -*- coding: utf-8 -*-

DEBUG = True

def log(*arg_list):
    if DEBUG:
        print " ".join(map(str, arg_list))


class Rect:
    def __init__(self, left, top, width, height):
        self.left = left
        self.top = top
        self.width = width
        self.height = height
    def x(self): return self.left
    def y(self): return self.top
    def right(self): return self.left + self.width-1
    def bottom(self): return self.top + self.height-1
        
    

class Size:
    def __init__(self, width, height):
        self.width = width
        self.height = height

