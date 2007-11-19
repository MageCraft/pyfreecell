import psp2d
import vs_class
from vs_buttons import *

class tscreen(vs_class.tclass):
  button_events = None
  screen = None
  fclose = False

  def __init__(self):
    self.init_buttons()
    self.screen = psp2d.Screen()

  def init_buttons(self):
    self.button_events = tbutton_events()
    self.button_events.on_button_down = self.button_down
    self.button_events.on_button_up = self.button_up
    self.button_events.on_button_press = self.button_press

  def button_down(self, pbuttons):
    pass # Abstract method

  def button_up(self, pbuttons):
    pass # Abstract method

  def button_press(self, pbuttons):
    pass # Abstract method

  def update(self):
    self.screen.swap()

  def update_stacks(self):
    lselected = self.selected_item
    for lstack in self.stacks:
      lstack.update(self.screen, lselected, self.card_selection)

  def run(self):
    while True:
      self.button_events.do_events()
      if self.fclose:
        break
      self.update()
      
  def show(self):
    self.run()
    
  def close(self):
    self.fclose = True
