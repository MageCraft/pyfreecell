#!/usr/bin/env python
# -*- coding: utf-8 -*-
from psp2d import Color, Image, Screen, Font, Controller, Timer


class Main(Timer):
    def __init__(self, fps=50):
        Timer.__init__(self, 1000/fps)
        self.fps = fps
        self.scr = Screen()
        self.img = Image(480, 272)
        self.img.clear(Color(0, 0, 0))
        draw_background(self.img, Color(127,127,127))

    def fire(self):
        pad = Controller()
        if pad.circle:
            return Fasle #quit
        elif pad.square:
            log('pad.squre')
        elif pad.triangle:
            log('pad.triangle')
        elif pad.circle:
            log('pad.circle')
        elif pad.cross:
            log('pad.cross')
        elif pad.up:
            log('pad.up')
        elif pad.down:
            log('pad.down')
        elif pad.left:
            log('pad.left')
        elif pad.right:
            log('pad.right') 
        else:
            pass
        self.scr.blit(self.img)
        self.scr.swap()
        return True



#font_path = 'images/font_arial_10_white.png'




SCREEN_SIZE = Size(480, 272)

MAX_ROW = 20
MAX_COL = 10
BLOCK_H = SCREEN_SIZE.height / MAX_ROW 
BLOCK_W = BLOCK_H

#draw horizontal or vertical line with width >= 1
def draw_line(surface, x0, y0, x1, y1, color, width=1):
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
    Main().run()

if __name__ == '__main__':
    main()
