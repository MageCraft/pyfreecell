import psp2d
import _random
import vs_class

class tsuits:
  spades = 0
  clubs = 1
  diamonds = 2
  hearts = 3

  names = ['S', 'C', 'D', 'H']

  def suit(self, pname):
    lresult = None
    lindex = 0
    for lname in self.names:
      if lname == pname:
        lresult = lindex
        break
      lindex = lindex + 1
    return lresult

suits = tsuits()

class tcards:
  ace = 0
  two = 1
  three = 2
  four = 3
  five = 4
  six = 5
  seven = 6
  eight = 7
  nine = 8
  ten = 9
  jack = 10
  queen = 11
  king = 12
  
  names = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '0', 'J', 'Q', 'K']
  
  def card(self, pname):
    lresult = None
    lindex = 0
    for lname in self.names:
      if lname == pname:
        lresult = lindex
        break
      lindex = lindex + 1
    return lresult
    
cards = tcards()

class tcard_images:
  front = psp2d.Image('images/card.png')
  back = psp2d.Image('images/card_back.png')

class tsuit_large_images:
  items = [psp2d.Image('images/spade_large.png')
      , psp2d.Image('images/club_large.png')
      , psp2d.Image('images/diamond_large.png')
      , psp2d.Image('images/heart_large.png')]

class tsuit_small_images:
  items = [psp2d.Image('images/spade_small.png')
      , psp2d.Image('images/club_small.png')
      , psp2d.Image('images/diamond_small.png')
      , psp2d.Image('images/heart_small.png')]

class tvalue_images:
  items = [psp2d.Image('images/A.png')
      , psp2d.Image('images/2.png')
      , psp2d.Image('images/3.png')
      , psp2d.Image('images/4.png')
      , psp2d.Image('images/5.png')
      , psp2d.Image('images/6.png')
      , psp2d.Image('images/7.png')
      , psp2d.Image('images/8.png')
      , psp2d.Image('images/9.png')
      , psp2d.Image('images/10.png')
      , psp2d.Image('images/J.png')
      , psp2d.Image('images/Q.png')
      , psp2d.Image('images/K.png')]
      
class tcard(vs_class.tclass):
  x = 0
  y = 0
  suit = suits.clubs
  value = cards.ace
  face_up = False

  def update(self, pscreen):
    if self.face_up:
      pscreen.blit(tcard_images.front, 0, 0, -1, -1, self.x, self.y, True)

      limage = tsuit_small_images.items[self.suit]
      pscreen.blit(limage, 0, 0, -1, -1, self.x + 3, self.y + 4, True)

      limage = tsuit_large_images.items[self.suit]
      pscreen.blit(limage, 0, 0, -1, -1, self.x + 9, self.y + 15, True)

      limage = tvalue_images.items[self.value]
      pscreen.blit(limage, 0, 0, -1, -1, self.x + 13, self.y + 4, True)
    else:
      pscreen.blit(tcard_images.back, 0, 0, -1, -1, self.x, self.y, True)
      
  def copy_to(self, pcard):
    pcard.x = self.x
    pcard.y = self.y
    pcard.suit = self.suit
    pcard.value = self.value
    pcard.face_up = self.face_up
    
  def get_as_string(self):
    lresult = cards.names[self.value] + suits.names[self.suit]
    if self.face_up:
      lresult = lresult + 'U'
    else:
      lresult = lresult + 'D'
    lresult = lresult + '%(x)03d%(y)03d' % {'x': self.x, 'y': self.y}
    return lresult
    
  def set_as_string(self, pstring):
    lvalue = pstring[0: 1]
    lsuit = pstring[1: 2]
    lface_up = pstring[2: 3]
    lx = pstring[3: 6]
    ly = pstring[6: 9]
    
    self.value = cards.card(lvalue)
    self.suit = suits.suit(lsuit)
    self.face_up = lface_up == 'U'
    self.x = int(lx)
    self.y = int(ly)
      
class tstack(vs_class.tclass):
  x = 0
  y = 0
  items = []
  
  def __init__(self):
    self.items = []

  def add_existing(self, pcard):
    self.items.append(pcard)
    
  def add(self, psuit, pvalue, pface_up):
    lcard = tcard()
    
    lcard.suit = psuit
    lcard.value = pvalue
    lcard.face_up = pface_up
    
    self.add_existing(lcard)
    
  def clear(self):
    self.items = []
    
  def shuffle(self):
    lrandom = _random.Random()
    lrandom.seed()
    
    lcount = len(self.items)

    for i in range(0, lcount):
      lnew_index = int(round(lrandom.random() * (lcount - 1)))
      lcard = self.items[i]
      lother_card = self.items[lnew_index]
      self.items[i] = lother_card
      self.items[lnew_index] = lcard
  
  def calculate_positions(self):
    lx = self.x
    ly = self.y
    for lcard in self.items:
      lcard.x = lx
      lcard.y = ly
      if lcard.face_up:
        ly = ly + 10
      else:
        ly = ly + 5
  
  def update(self, pscreen):
    for lcard in self.items:
      lcard.update(pscreen)

  def last_card(self):
    if len(self.items) == 0:
      return None
    else:
      return self.items[len(self.items) - 1]
      
  def copy_to(self, pstack):
    pstack.x = self.x
    pstack.y = self.y
    pstack.clear()
    for lcard in self.items:
      lnew_card = tcard()
      lcard.copy_to(lnew_card)
      pstack.items.append(lnew_card)
      
  def get_as_string(self):
    lresult = ''
    for lcard in self.items:
      lresult = lresult + lcard.get_as_string()
    return lresult

  def set_as_string(self, pstring):
    self.clear()
    lstring = pstring
    while len(lstring) >= 9:
      lcard_string = lstring[0: 9]
      lstring = lstring[9: len(lstring)]
      
      lcard = tcard()
      lcard.set_as_string(lcard_string)
      self.items.append(lcard)
    
class tcard_selection(vs_class.tclass):
  images = [psp2d.Image('images/selection_01.png')
      , psp2d.Image('images/selection_02.png')
      , psp2d.Image('images/selection_03.png')
      , psp2d.Image('images/selection_04.png')
      , psp2d.Image('images/selection_05.png')]
  image_index = 0
  image_index_by = 1
  frame_delay = 5
  frame_delay_index = 0

  def update(self, pscreen, px, py):
    limage = self.images[self.image_index]
    pscreen.blit(limage, 0, 0, -1, -1, px, py, True)
    self.update_image_index()
    
  def update_image_index(self):
    self.frame_delay_index = self.frame_delay_index + 1
    if self.frame_delay_index == self.frame_delay:
      self.frame_delay_index = 1

      if self.image_index == 4:
        self.image_index_by = -1
      elif self.image_index == 0:
        self.image_index_by = 1

      self.image_index = self.image_index + self.image_index_by

