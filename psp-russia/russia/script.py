#!/usr/bin/env python
# -*- coding: utf-8 -*-
from psp2d import Color, Image, Screen, Font, Controller

font_path = 'images/font_arial_10_white.png'
BLOCK_NORMAL_CLR_TABLES = (
    Color(191,0,0),
    Color(0,191,0),
    Color(0,0,191),
    Color(191,191,0),
    Color(191,0,191),
    Color(0,191,191)
)

lighter = lambda c: (255,0)[not c>0]
darker = lambda c: (128,0)[not c>0]

def get_block_colors(unit_value):
    clr = BLOCK_NORMAL_CLR_TABLES[unit_value]
    l = [clr.red, clr.green, clr.blue]
    return clr, Color(*map(lighter, l)), Color(*map(darker,l))


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

SCREEN_SIZE = Size(480, 272)

MAX_ROW = 20
MAX_COL = 10
BLOCK_H = SCREEN_SIZE.height / MAX_ROW 
BLOCK_W = BLOCK_H

#draw horizontal or vertical line with width >= 1
def draw_line_x(surface, x0, y0, x1, y1, color, width=1):
    if width == 1: 
        surface.drawLine(x0,y0,x1,y1,color)
    else:
        #fill rect
        assert( x0 == x1 or y0 == y1 )
        assert( x0 != x1 or y0 != y1 ) #paint a point
        x,y,w,h = x0, y0, width, width 
        if x0 > x1: x = x1
        if y0 > y1: y = y1
        if x0 == x1: 
            h = abs(y1-y0)
        else:
            w = abs(x1-x0)
        surface.fillRect(x, y, w, h, color)

def draw_background(surface, color):
    game_area_width = BLOCK_W*MAX_COL
    frame_width = BLOCK_W
    left, top = (SCREEN_SIZE.width - game_area_width - frame_width*2)/2, 0
    draw_line_x(surface, left, top, left, SCREEN_SIZE.height, color, frame_width)
    draw_line_x(surface, left+game_area_width+frame_width, top, left+game_area_width+frame_width, SCREEN_SIZE.height, color, frame_width)
    #surface.drawLine(left, top + SCREEN_SIZE.height-1, left+game_area_width, top+SCREEN_SIZE.height-1, color)

def draw3dRect(surface, rect, clr1, clr2):
    surface.drawLine( rect.x(), rect.y(), rect.right()-1, rect.y(), clr1 );
    surface.drawLine( rect.x(), rect.y(), rect.x(), rect.bottom()-1, clr1 );
    surface.drawLine( rect.right(), rect.y()+1, rect.right(), rect.bottom(), clr2 );
    surface.drawLine( rect.x()+1, rect.bottom(), rect.right(), rect.bottom(), clr2 );

def drawBlock(surface, rect, bkClr, clr1, clr2):
    surface.fillRect(rect.left, rect.top, rect.width, rect.height, bkClr)
    draw3dRect(surface, rect, clr1, clr2)

def main():
    scr = Screen()
    fnt = Font(font_path)
    img = Image(480, 272)
    img.clear(Color(0, 0, 0))
    draw_background(img, Color(127,127,127))
    unit_value = 3
    drawBlock(img, Rect(10, 10, BLOCK_W, BLOCK_H), *get_block_colors(unit_value))
    scr.blit(img)
    scr.swap()
    while True:
        pad = Controller()
        if pad.circle:
            break #quit
        elif pad.square:
            print 'pad.squre'
        elif pad.triangle:
            print 'pad.triangle'
        elif pad.circle:
            print 'pad.circle'
        elif pad.cross:
            print 'pad.cross'
        elif pad.up:
            print 'pad.up'
        elif pad.down:
            print 'pad.down' 
        elif pad.left:
            print 'pad.left' 
        elif pad.right:
            print 'pad.right' 
        else:
            pass

if __name__ == '__main__':
    main()
