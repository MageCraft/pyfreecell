import psp2d

class buttons:
  left = 0
  right = 1
  up = 2
  down = 3
  cross = 4
  circle = 5
  square = 6
  triangle = 7
  left_trigger = 8
  right_trigger = 9
  home = 10
  select = 11
  start = 12

class tbutton_events:
  button_press_skip = 8
  button_press_index = 0
  on_button_down = None
  on_button_up = None
  on_button_press = None
  buttons = []
  last_buttons =[]
  
  def get_buttons(self):
    self.last_buttons = self.buttons
    lcontroller = psp2d.Controller()
    lbuttons = []
    if lcontroller.left:
      lbuttons = lbuttons + [buttons.left]
    if lcontroller.right:
      lbuttons = lbuttons + [buttons.right]
    if lcontroller.up:
      lbuttons = lbuttons + [buttons.up]
    if lcontroller.down:
      lbuttons = lbuttons + [buttons.down]
    if lcontroller.cross:
      lbuttons = lbuttons + [buttons.cross]
    if lcontroller.circle:
      lbuttons = lbuttons + [buttons.circle]
    if lcontroller.square:
      lbuttons = lbuttons + [buttons.square]
    if lcontroller.triangle:
      lbuttons = lbuttons + [buttons.triangle]
    if lcontroller.l:
      lbuttons = lbuttons + [buttons.left_trigger]
    if lcontroller.r:
      lbuttons = lbuttons + [buttons.right_trigger]
    if lcontroller.select:
      lbuttons = lbuttons + [buttons.select]
    if lcontroller.start:
      lbuttons = lbuttons + [buttons.start]
    self.buttons = lbuttons
    
  @property
  def buttons_different(self):
    lresult = False
    for lbutton in range(buttons.left, buttons.start + 1):
      lin_buttons = lbutton in self.buttons
      lin_last_buttons = lbutton in self.last_buttons
      if lin_buttons != lin_last_buttons:
        lresult = True
        break
    return lresult
  
  def do_events(self):
    self.get_buttons()
    if len(self.buttons) > 0:
      if self.buttons_different:
        self.do_on_button_down()
        self.do_on_button_press(True)
      else:
        self.do_on_button_press(False)
              
  def do_on_button_down(self):
    if self.on_button_down != None:
      self.on_button_down(self.buttons)
              
  def do_on_button_press(self, pforce):
    if self.on_button_press != None:
      self.button_press_index = self.button_press_index + 1
      if pforce or self.button_press_index == self.button_press_skip:
        self.button_press_index = 0
        self.on_button_press(self.buttons)
        
class tdraw_button:
  image = None
  font = None
  button_images = []
  
  def __init__(self, pimage, pfont):
    self.image = pimage
    self.font = pfont
    
    self.button_images = [None
        , None
        , None
        , None
        , psp2d.Image('images/cross.png')
        , psp2d.Image('images/circle.png')
        , psp2d.Image('images/square.png')
        , psp2d.Image('images/triangle.png')
        , None
        , None
        , psp2d.Image('images/home.png')
        , psp2d.Image('images/select.png')
        , psp2d.Image('images/start.png')]
  
  def draw_button(self, px, py, pbutton, pcaption):
    limage = self.button_images[pbutton]
    self.image.blit(limage, 0, 0, -1, -1, px, py, True)
    self.font.drawText(self.image, px + 20, py + 2, pcaption)
  
  


