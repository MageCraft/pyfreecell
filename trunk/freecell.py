#!/usr/bin/env python

import pygtk
pygtk.require('2.0')

import gtk
import gtk.gdk
import random
import time
import sys
import pick_seed
import gc

from util import *
from common import *
from engine import *

CARDS_PATH = 'cards.bmp'
FLAG_PATH = 'flag1.bmp'
FLAG_MASK_RGB = (0,127,0)
CARD_W = 71
CARD_H = 96
SPLIT_H = 15
SPLIT_W = 8
SPLIT_W2 = 5 #for scrollwindow
SPLIT_FREE_FEILDS = 11
SCREEN_BACK_COLOR = gtk.gdk.Color(0,65535/2,0)

MAX_SEED = 32000
MAXCOL = 8
MAXPOS = 21

TITLE_STATIC = 'pyfreecell'
TITLE_DYNAMIC= 'pyfreecell -- %d#'

def print_cards(cards):
    for row in range(7):
        for col in range(MAXCOL):
            if row*8 + col < DECK_SIZE :
                print '%02d' % (cards[col][row]),
        print


class pyFreecell:
    ui = '''<ui>
    <menubar name="MenuBar">
      <menu name="Game" action="Game">
        <menuitem action="New game"/>
        <menuitem action="Choose game"/>
        <menuitem action="Restart game"/>
        <separator/>
        <menuitem action="Statistics"/>
        <menuitem action="Preference"/>
        <separator/>
        <menuitem action="Undo"/>
        <separator/>
        <menuitem action="Quit"/>
      </menu>
      <menu name="Help" action="Help">
        <menuitem action="About"/>
      </menu>
    </menubar>
    </ui>'''

    def __init__(self, is_testing=False):
        self.__load_pixbuf()
        self.rt_free = Rect(0, 0, CARD_W*4, CARD_H)
        self.rt_flag = Rect(self.rt_free.right()+1, 0, CARD_W, CARD_H)
        self.rt_home = Rect(self.rt_flag.right()+1, 0, CARD_W*4, CARD_H) 
        self.rt_field = Rect(SPLIT_W, self.rt_free.bottom()+SPLIT_FREE_FEILDS, (CARD_W+SPLIT_W)*8, 0)
        self.pixmap = None
        self.deck = None
        self.seed = None
        self.field = None
        self.free = None
        self.home = None
        self.selection = None
        self.playing = False
        self.testing = is_testing

        #create widgets
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.set_title(TITLE_STATIC)
        self.window.connect("destroy", self.destroy)
        self.window.connect("delete_event", self.delete_event)

        self.vb = gtk.VBox()
        self.create_menus();
        self.mb = self.uimanager.get_widget('/MenuBar')
        self.vb.pack_start(self.mb, False)

        self.area = gtk.DrawingArea()
        self.area.connect('expose_event', self.area_expose)
        self.area.connect('configure_event', self.area_config)
        self.area.connect('button_press_event', self.on_btn_press)
        self.area.connect('button_release_event', self.on_btn_release)
        self.area.set_events(gtk.gdk.BUTTON_PRESS_MASK | 
                             gtk.gdk.BUTTON_RELEASE_MASK )
        self.sw = gtk.ScrolledWindow()
        self.sw.set_shadow_type(gtk.SHADOW_NONE)
        self.sw.set_policy(gtk.POLICY_NEVER, gtk.POLICY_AUTOMATIC)
        self.sw.add_with_viewport(self.area)
        #self.sw.add(self.area)
        self.vb.pack_start(self.sw)

        self.window.add(self.vb)
        self.window.set_default_size(640,480)
        self.window.set_geometry_hints(self.window, min_height=480, min_width=640)
        self.window.show_all()

    def create_menus(self):
        self.uimanager = gtk.UIManager()
        self.main_actions = gtk.ActionGroup('MainActions')
        self.main_actions.add_actions([
                ('Game', None, '_Game'),
                ('New game', None, '_New game', 
                 '<Control>n', 'Play new game', self.new_game),
                ('Choose game', None, '_Choose game',
                 '<Control>c', 'Choose a game with seed', self.choose_game),
                ('Restart game', None, '_Restart game',
                 '<Control>r', 'Restart current playing game', self.restart_game),
                ('Statistics', None, '_Statistics', 
                 '<Control>s', 'Show history game statistics', self.game_history),
                ('Preference', None, '_Preference', 
                 '<Control>p', 'Set your preference', self.preference),
                ('Undo', None, '_Undo', 
                 '<Control>u', 'Undo your last action', self.undo),
                ('Quit', None, '_Quit',
                 '<Control>q', 'Quit', self.destroy),
                ('Help', None, '_Help'),
                ('About', None, '_About', None, None, self.about)
                ])
        self.window.add_accel_group(self.uimanager.get_accel_group())
        self.uimanager.insert_action_group(self.main_actions,0)
        self.uimanager.add_ui_from_string(self.ui)


    def __shuffle(self):
        self.deck = range(DECK_SIZE)
        random.seed(self.seed)
        random.shuffle(self.deck)
        max_row = lambda col: (DECK_SIZE-1-col)/MAXCOL + 1
        for col in range(MAXCOL):
            self.field.append([])
            for row in range(max_row(col)):
                self.field[col].append(self.deck[MAXCOL*row+col])

    def __create_game(self, seed):
        if self.testing:
            import test
            self.free, self.home, self.field = test.select_test_sample(self.window)
        else:
            self.seed = seed
            self.free = [EMPTY] * 4
            self.home = [EMPTY] * 4
            self.field = []
            self.__shuffle()
        self.playing = True
        self.selection = {'area':IDLE, 'col':-1}
        self.engine = Engine(self.free, self.home, self.field, self.selection)
        self.engine.set_notify(self.area.queue_draw)
        #set title
        self.window.set_title( TITLE_DYNAMIC % (self.seed,))
        #refresh
        self.area.queue_draw()

    def new_game(self, *args):
        random.seed(time.time())
        seed = random.randint(0, MAX_SEED)
        #seed = 11982
        self.__create_game(seed)

    def choose_game(self, *args):
        seed = pick_seed.pick_seed(max=MAX_SEED, parent=self.window)
        if seed is not None:
            print 'pick seed is %d' %(seed,)
            self.__create_game(seed)

    def restart_game(self, *args):
        #notify user that if want to finish current game, later
        self.__create_game(self.seed) #use the current seed
        
    def game_history(self, *args):
        pass
    def preference(self, *args):
        pass
    def undo(self, *args):
        pass
    def about(self, *args):
        pass
        

    def __load_pixbuf(self):
        self.pbuf_cards = gtk.gdk.pixbuf_new_from_file(CARDS_PATH)
        self.pbuf_flag1 = gtk.gdk.pixbuf_new_from_file(FLAG_PATH)

        r,g,b = to_chr(FLAG_MASK_RGB)
        for pixbuf in (self.pbuf_flag1,):
            pixbuf.add_alpha(True, r,g,b)

    def __set_highlight_gc(self, gc, value):
        func = None
        if is_black(value):
            func = gtk.gdk.INVERT
        else:
            func = gtk.gdk.XOR
        gc.set_function(func)
        gc.set_rgb_fg_color(gtk.gdk.color_parse('white'))

    def __draw_card(self, drawable, gc, area, col, row=-1, value=EMPTY, highlight=False):
        if not self.playing:
            return
        dest_x, dest_y = 0, 0
        if area == FREE:
            value = self.free[col]
            if value is EMPTY:
                return
            dest_x = self.rt_free.x +  CARD_W*col
            dest_y = self.rt_free.y
        elif area == HOME:
            value = self.home[col]
            if value is EMPTY:
                return
            dest_x = self.rt_home.x +  CARD_W*col
            dest_y = self.rt_home.y
        elif area == FIELD:
            if row == -1:
                row = len(self.field[col])-1
            value = self.field[col][row]
            dest_x = self.rt_field.x  + (CARD_W + SPLIT_W) * col
            dest_y = self.rt_field.y  + (SPLIT_H) * row

        assert(value != EMPTY)
        src_x = (value / 4 ) * CARD_W
        src_y = (value%4) * CARD_H

        if not highlight:
            drawable.draw_pixbuf(gc, self.pbuf_cards, src_x, src_y, dest_x, dest_y, CARD_W, CARD_H)
        else:
            self.__set_highlight_gc(self.hl_gc, value)
            drawable.draw_rectangle(self.hl_gc, True, dest_x, dest_y, CARD_W, CARD_H)

        #draw 12 points later
        x1,y1 = dest_x, dest_y
        x2,y2 = dest_x, dest_y+CARD_H-1
        x3,y3 = dest_x+CARD_W-1,dest_y+CARD_H-1
        x4,y4 = dest_x+CARD_W-1, dest_y
        points=[(x1,y1), (x1+1,y1), (x1,y1+1),
                (x2,y2), (x2+1,y2), (x2,y2-1),
                (x3,y3), (x3-1,y3), (x3,y3-1),
                (x4,y4), (x4-1,y4), (x4,y4+1)]
        self.gc.set_rgb_fg_color(SCREEN_BACK_COLOR)
        drawable.draw_points(self.gc,points)
        
    def __do_paint(self, drawable):
        print '__do_paint'

        #draw background
        self.gc.set_rgb_fg_color(SCREEN_BACK_COLOR)
        drawable.draw_rectangle(self.gc, True, 0, 0, -1,-1)
        cell = Rect(0, self.rt_free.y, CARD_W,CARD_H)
        
        #draw freecell 
        color1 = gtk.gdk.color_parse('black')
        color2 = gtk.gdk.color_parse('green')
        for i in range(4):
            cell.x = self.rt_free.x + CARD_W * i
            draw3DRect(drawable, self.gc, cell, color1, color2)
            self.__draw_card(drawable, self.gc, FREE, i)
            
        #draw flag
        w,h = (38,38)
        frame_rt = Rect(self.rt_flag.x + (self.rt_flag.width - w)/2, 
                self.rt_flag.y + (self.rt_flag.height - h)/2, w, h)
        draw3DRect(drawable, self.gc, frame_rt, color2, color1) 
        x = frame_rt.x + (frame_rt.width - self.pbuf_flag1.get_width()) /2
        y = frame_rt.y + (frame_rt.height - self.pbuf_flag1.get_height()) /2
        drawable.draw_pixbuf(self.gc, self.pbuf_flag1, 0, 0, x, y)

        #draw  home
        for i in range(4):
            cell.x = self.rt_home.x + CARD_W * i
            draw3DRect( drawable, self.gc, cell, color1, color2)
            self.__draw_card(drawable, self.gc, HOME, i)

        #draw fields
        if self.field is not None:
            for col in range(len(self.field)):
                for row in range(len(self.field[col])):
                    self.__draw_card(drawable, self.gc, FIELD, col, row)
        #draw hightlight
        if self.playing and self.selection['area'] is not IDLE:
            self.__draw_card(drawable, self.gc, self.selection['area'], self.selection['col'], highlight=True)
            
    def delete_event(self, widget, event, data=None):
        print 'delete_event'
        return False

    def destroy(self, widget, data=None):
        gtk.main_quit()

    def area_expose(self, area, event):
        print 'area_expose'
        x, y, width, height = event.area
        self.__do_paint(self.pixmap)
        self.area.window.draw_drawable(self.gc, self.pixmap, x, y, x, y, width, height)
        return True

    def area_config(self, area, event):
        x, y, width, height = self.area.get_allocation()
        print 'area_config,(%d,%d)' % (width, height)
        if self.pixmap is None:
            self.gc = self.area.window.new_gc()
            self.hl_gc = self.area.window.new_gc() #gc for drawing highlight
        else:
            del self.pixmap
            gc.collect()
            self.pixmap = None
        self.pixmap = gtk.gdk.Pixmap(area.window, width, height)
        self.rt_field.height = height - self.rt_field.y
        return True


    def on_btn_press(self, widget, event):
        print 'no_btn_press', event.type, event.button, event.x, event.y 
        if not self.playing:
            print 'not playing'
            return True
        pos = Point(int(event.x), int(event.y))
        sel = {} 
        if self.rt_free.contains(pos):
            print 'point in freecell'
            rpos = pos - self.rt_free.top_left()
            sel['area'] = FREE
            sel['col'] = rpos.x / CARD_W
        elif self.rt_home.contains(pos):
            print 'point in home'
            rpos = pos - self.rt_home.top_left()
            sel['area'] = HOME
            sel['col'] = rpos.x / CARD_W
        elif self.rt_field.contains(pos):
            print 'point in field'
            rpos = pos - self.rt_field.top_left()
            if rpos.x % (CARD_W+SPLIT_W) > CARD_W:
                print 'select split space'
                pass
            else:
                col = rpos.x / (CARD_W+SPLIT_W)
                sz = len(self.field[col])
                if sz > 0 and rpos.y > CARD_H + SPLIT_H*(sz-1):
                    print 'beyond the range of col:%d'%(col)
                    pass
                else:
                    sel['area'] = FIELD
                    sel['col'] = col
        else:
            print 'point other places'
            pass

        print sel
        if len(sel) != 0:
            self.engine.select(sel['area'], sel['col'])


    def get_last_card_rect(self, col):
        t = len(self.field[col]) - 1
        pt = self.rt_field.top_left() + Point(col*(CARD_W+SPLIT_W), t*SPLIT_H)
        return pt.x, pt.y, CARD_W, CARD_H


            
    def on_btn_release(self, widget, event):
        print 'no_btn_release', event.type, event.button, event.x, event.y 
        return True

def main():
    gtk.main()
    return 0

if __name__ == '__main__':    
    test = False
    if len(sys.argv) == 2:
        if sys.argv[1] == '-test' or sys.argv[1] == '-t':
            test = True
    #test = True
    pyFreecell(test)
    main()




