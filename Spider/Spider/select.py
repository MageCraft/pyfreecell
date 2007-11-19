import psp2d
import vs_screen
from card import *
from vs_buttons import *
from spider import *
import math

class tgame_type_update:
  card = None
  caption = ''
  x = 0
  y = 0
  
  def __init__(self):
    self.card = tcard()
    self.card.face_up = True
    
class tselect(vs_screen.tscreen):
  allow_continue = False
  completed = False
  game_type = tgame_type.medium
  restart = False
  font = None
  card_selection = None
  game_types = []
  draw_button = None
  spider = []
  spider_angle = 0.0

  def get_super(self):
    return vs_screen.tscreen

  def __init__(self, pgame_type, pallow_continue, pcompleted):
    self.super.__init__(self)
    self.allow_continue = pallow_continue
    self.completed = pcompleted
    self.game_type = pgame_type
    self.background_image = psp2d.Image('images/background.png')
    self.card_selection = tcard_selection()
    self.font = psp2d.Font('images/font_arial_10_white.png')
    self.draw_button = tdraw_button(self.screen, self.font)
    self.card_selection = tcard_selection()
    self.card_selection.frame_delay = 5
    self.init_game_types()
    self.init_spider()
    
  def init_game_types(self):
    lx = 90
    ly = 150
    lby = 120

    # Easy
    lgame_type = tgame_type_update()
    lgame_type.card.x = lx
    lgame_type.card.y = ly
    lgame_type.card.suit = tsuits.clubs
    lgame_type.card.value = tcards.jack
    lgame_type.caption = 'Easy'
    self.game_types.append(lgame_type)
    
    lx = lx + lby
    
    # Medium
    lgame_type = tgame_type_update()
    lgame_type.card.x = lx
    lgame_type.card.y = ly
    lgame_type.card.suit = tsuits.diamonds
    lgame_type.card.value = tcards.queen
    lgame_type.caption = 'Medium'
    self.game_types.append(lgame_type)
    
    lx = lx + lby
    
    # Hard
    lgame_type = tgame_type_update()
    lgame_type.card.x = lx
    lgame_type.card.y = ly
    lgame_type.card.suit = tsuits.hearts
    lgame_type.card.value = tcards.king
    lgame_type.caption = 'Hard'
    self.game_types.append(lgame_type)
    
  def init_spider(self):
    self.spider = [psp2d.Image('images/spider_s.png')
        , psp2d.Image('images/spider_p.png')
        , psp2d.Image('images/spider_i.png')
        , psp2d.Image('images/spider_d.png')
        , psp2d.Image('images/spider_e.png')
        , psp2d.Image('images/spider_r.png')]
    
  def button_down(self, pbuttons):
    if buttons.cross in pbuttons:
      self.do_select()
    elif buttons.left in pbuttons:
      if self.game_type > tgame_type.easy:
        self.game_type = self.game_type - 1
    elif buttons.right in pbuttons:
      if self.game_type < tgame_type.hard:
        self.game_type = self.game_type + 1
    elif buttons.circle in pbuttons:
      if self.allow_continue:
        self.do_continue()

  def update_spider(self):
    lx = 115
    ly = 60
    lindex = 0
    for limage in self.spider:
      lya = ly + (10 * math.sin(self.spider_angle + (0.5 * lindex)))
      self.screen.blit(limage, 0, 0, -1, -1, lx, lya, True)
      lx = lx + limage.width + 20
      lindex = lindex + 1
      
    self.spider_angle = self.spider_angle + 0.1
        
  def update_game_options(self):
    for lgame_type_index in range(tgame_type.easy, tgame_type.hard + 1):
      lgame_type = self.game_types[lgame_type_index]
      lgame_type.card.update(self.screen)
      if lgame_type_index == self.game_type:
        self.card_selection.update(self.screen, lgame_type.card.x - 7, lgame_type.card.y - 8)
      self.font.drawText(self.screen, lgame_type.card.x + 45, lgame_type.card.y + 15, lgame_type.caption)
      
  def update_buttons(self):
    lx = 380
    ly = 250
    self.draw_button.draw_button(lx, ly, buttons.cross, 'New Game')
    if self.allow_continue:
      lx = lx - 130
      self.draw_button.draw_button(lx, ly, buttons.circle, 'Continue Game')
      
  def update_completed(self):
    lx = 90
    ly = 225
    lindex = 0.0
    for lchar in ['C', 'o', 'n', 'g', 'r', 'a', 't', 'u', 'l', 'a', 't', 'i', 'o', 'n', 's', '.'
        , ' ', 'Y', 'o', 'u', ' ', 'W', 'o', 'n', '!']:
      lya = ly + (5 * math.sin(self.spider_angle + (0.5 * lindex)))
      self.font.drawText(self.screen, lx, lya, lchar)
      if lchar == 'W':
        lx = lx + 18
      elif lchar == 'l' or lchar == 'i':
        lx = lx + 8
      else:
        lx = lx + 12
      lindex = lindex + 0.25

  def update(self):
    self.screen.blit(self.background_image)
    self.update_spider()
    self.update_game_options()
    if self.completed:
      self.update_completed()
    self.update_buttons()
    self.super.update(self)
    
  def do_select(self):
    self.restart = True
    self.close()
    
  def do_continue(self):
    self.restart = False
    self.close()
    
  def show(self):
    self.super.show(self)
    
