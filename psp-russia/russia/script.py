import psp2d
import sys
import pygame
pygame.init()
import sys

font_path = 'images/font_arial_10_white.png'

MAX_ROW = 10
MAX_COL = 20

def main_1():
    scr = psp2d.Screen()
    fnt = psp2d.Font(font_path)
    img = psp2d.Image(480, 272)
    img.clear(psp2d.Color(0, 0, 0))
    img.drawText(0, 0, 'Hello, world', psp2d.Color(255,0,0))
    #fnt.drawText(img, 0, 0, 'Hello, world')
    #img.drawLine(100, 100, 150, 150, psp2d.Color(255,0,0))
    pygame.draw.line(img.surface, (255,0,0,255), (100,100), (150,150), 2)
    scr.blit(img)
    scr.swap()

    while True:
        for e in pygame.event.get():
            if e.type == pygame.QUIT: sys.exit()


def main():
    scr = psp2d.Screen()
    fnt = psp2d.Font(font_path)
    img = psp2d.Image(480, 272)
    img.clear(psp2d.Color(0, 0, 0))
    fnt.drawText(img, 0, 0, 'Hello, world')
    img.drawLine(100, 100, 150, 150, psp2d.Color(255,0,0))
    scr.blit(img)
    scr.swap()
    while True:
        pad = psp2d.Controller()
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
    main_1()
