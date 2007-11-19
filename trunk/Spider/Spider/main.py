import psp2d
import vs_screen
from card import *
from vs_buttons import *
from spider import *
import select

class tmain(vs_screen.tscreen):
  static_buffer = None
  background = None
  card_selection = None
  font = None
  draw_button = None
  game_state = None
  show_selection = True
  undo = []
  redo = []
  
  def get_super(self):
    return vs_screen.tscreen

  def __init__(self):
    self.super.__init__(self)
    self.static_buffer = psp2d.Image(480, 272)
    self.background_image = psp2d.Image('images/background.png')
    self.font = psp2d.Font('images/font_arial_10_white.png')
    self.draw_button = tdraw_button(self.static_buffer, self.font)
    self.game_state = tgame_state()
    self.card_selection = tcard_selection()
    self.init_stacks()

  def init_stacks(self):
    self.game_state.stacks = []
    lx = 7
    ly = 7
    for i in range(0, 10):
      lstack = tstack()
      lstack.x = lx
      lstack.y = ly
      self.game_state.stacks.append(lstack)
      lx = lx + 48

  def init_deck(self):
    self.game_state.deck.clear()
    
    if self.game_state.game_type == tgame_type.easy:
      lsuits = [suits.hearts, suits.hearts, suits.hearts, suits.hearts]
    elif self.game_state.game_type == tgame_type.medium:
      lsuits = [suits.spades, suits.spades, suits.hearts, suits.hearts]
    else:
      lsuits = [suits.spades, suits.clubs, suits.diamonds, suits.hearts]

    for lsuit in lsuits:
      for lvalue in range(0, 13):
        self.game_state.deck.add(lsuit, lvalue, False)
        self.game_state.deck.add(lsuit, lvalue, False)
        
    self.game_state.deck.shuffle()

  def init_deal(self):
    self.init_deck()
    self.game_state.done.clear()
    self.undo = []
    self.redo = []
    
    for lstack in self.game_state.stacks:
      lstack.items = []

    for i in range(0, 4):
      for lstack in self.game_state.stacks:
        lcard = self.game_state.deck.items.pop()
        lstack.add_existing(lcard)

    for i in range(0, 4):
        lcard = self.game_state.deck.items.pop()
        lstack = self.game_state.stacks[i]
        lstack.add_existing(lcard)

    for lstack in self.game_state.stacks:
        lcard = self.game_state.deck.items.pop()
        lcard.face_up = True
        lstack.add_existing(lcard)
        
    # Testing deal
    #self.test_deal()

    self.game_state.selected_stack_index = 0
    self.game_state.selected_index = len(self.selected_stack.items) - 1
    
    self.update_static()
    
  def test_deal(self):
    for lstack_index in range(0, 2):
      for lvalue_index in range(cards.ace, cards.king + 1):
        lvalue = cards.king - lvalue_index
        lcard = tcard()
        lcard.suit = suits.hearts
        lcard.value = lvalue
        lcard.face_up = True
        if lvalue != cards.ace:
          self.game_state.stacks[0 + lstack_index].items.append(lcard)
        else:
          self.game_state.stacks[3 + lstack_index].items.append(lcard)
    
  def deal(self):
    self.copy_undo()
    ldeck_count = round(len(self.game_state.deck.items) / 10)
    if ldeck_count > 0:
      self.show_selection = False
      try:
        limage = tcard_images.back
        lx = 440 - ((ldeck_count - 1) * 5)
        ly = 222
        lframes = 15
        for lstack in self.game_state.stacks:
          if len(self.game_state.deck.items) > 0:
            lcard = self.game_state.deck.items.pop()
            lcard.face_up = True
            if len(lstack.items) > 0:
              ldest_card = lstack.last_card()
              ldx = ldest_card.x
              if ldest_card.face_up:
                ldy = ldest_card.y + 10
              else:
                ldy = ldest_card.y + 5
            else:
              ldx = lstack.x
              ldy = lstack.y
            lxchange = ((ldx - lx) / float(lframes))
            lychange = ((ldy - ly) / float(lframes))
            for lframe_index in range(0, lframes + 1):
              lcard.x = lx + (lxchange * float(lframe_index))
              lcard.y = ly + (lychange * float(lframe_index))
              self.screen.blit(self.static_buffer)
              lcard.update(self.screen)
              self.screen.swap()
            lstack.items.append(lcard)
            lcard.update(self.static_buffer)
        self.check_stacks()
      finally:
        self.show_selection = True
        self.game_state.selected_index = len(self.selected_stack.items) - 1
        self.update_static()

  @property
  def selected_stack(self):
    return self.game_state.stacks[self.game_state.selected_stack_index]

  @property
  def selected_item(self):
    try:
      litem = self.selected_stack.items[self.game_state.selected_index]
    except:
      litem = None
    return litem

  def select_left(self):
    lselected_index = self.game_state.selected_stack_index
    while True:
      lselected_index = lselected_index - 1
      if lselected_index == 0:
        break
      elif len(self.game_state.stacks[lselected_index].items) > 0:
        break
    if lselected_index >= 0 and len(self.game_state.stacks[lselected_index ].items) > 0:
      self.game_state.selected_stack_index = lselected_index
      self.game_state.selected_index = len(self.selected_stack.items) - 1

  def select_right(self):
    lselected_index = self.game_state.selected_stack_index
    while True:
      lselected_index = lselected_index + 1
      if lselected_index == len(self.game_state.stacks):
        break
      elif len(self.game_state.stacks[lselected_index].items) > 0:
        break
    if lselected_index < len(self.game_state.stacks) and len(self.game_state.stacks[lselected_index ].items) > 0:
      self.game_state.selected_stack_index = lselected_index
      self.game_state.selected_index = len(self.selected_stack.items) - 1

  def select_up(self):
    lselected_index = self.game_state.selected_index - 1
    if lselected_index >= 0:
      lselected = self.selected_item
      lnew = self.selected_stack.items[lselected_index]
      if lnew.face_up and lnew.suit == lselected.suit and lnew.value == lselected.value + 1:
        self.game_state.selected_index = lselected_index;

  def select_down(self):
    lselected_index = self.game_state.selected_index + 1
    if lselected_index < len(self.selected_stack.items):
      self.game_state.selected_index = lselected_index;

  def move_left(self):
    lselected_index = self.game_state.selected_stack_index
    lnew_index = lselected_index
    while True:
      lnew_index = lnew_index - 1
      if lnew_index < 0:
        break
      else:
        lcard = self.game_state.stacks[lnew_index].last_card()
        if lcard == None or lcard.value == self.selected_item.value + 1:
          break
    if lnew_index >= 0:
      self.copy_undo()
      lnew_card_index = len(self.game_state.stacks[lnew_index].items)
      litems = self.game_state.stacks[lselected_index].items
      self.game_state.stacks[lselected_index].items = litems[0:self.game_state.selected_index]
      self.game_state.stacks[lnew_index].items = self.game_state.stacks[lnew_index].items + litems[self.game_state.selected_index:len(litems)]
      self.game_state.selected_stack_index = lnew_index
      self.game_state.selected_index = lnew_card_index
      self.check_stacks()
      self.update_static()

  def move_right(self):
    lselected_index = self.game_state.selected_stack_index
    lnew_index = lselected_index
    while True:
      lnew_index = lnew_index + 1
      if lnew_index >= len(self.game_state.stacks):
        break
      else:
        lcard = self.game_state.stacks[lnew_index].last_card()
        if lcard == None or lcard.value == self.selected_item.value + 1:
          break
    if lnew_index < len(self.game_state.stacks):
      self.copy_undo()
      lnew_card_index = len(self.game_state.stacks[lnew_index].items)
      litems = self.game_state.stacks[lselected_index].items
      self.game_state.stacks[lselected_index].items = litems[0:self.game_state.selected_index]
      self.game_state.stacks[lnew_index].items = self.game_state.stacks[lnew_index].items + litems[self.game_state.selected_index:len(litems)]
      self.game_state.selected_stack_index = lnew_index
      self.game_state.selected_index = lnew_card_index
      self.check_stacks()
      self.update_static()

  def check_stacks(self):
    for lstack in self.game_state.stacks:
      self.check_stack_complete(lstack)
      lcard = lstack.last_card()
      if lcard != None:
        lcard.face_up = True
    self.check_selection()
    self.check_game_complete()
        
  def check_stack_complete(self, pstack):
    llast_index = len(pstack.items) - 1
    if llast_index >= cards.king - 1:
      lok = True
      lsuit = pstack.items[llast_index].suit
      for lindex in range(cards.ace, cards.king + 1):
        lcard = pstack.items[llast_index - lindex]
        if not lcard.face_up or lcard.suit != lsuit or lcard.value != lindex:
          lok = False
          break
      if lok:
        self.complete_stack(pstack)
        
  def complete_stack(self, pstack):
    self.calculate_positions()
    llast_index = len(pstack.items) - 1
    lcard_done = pstack.items[llast_index - cards.king:llast_index + 1]
    pstack.items = pstack.items[0:llast_index - cards.king]
    self.update_static()
    self.show_selection = False
    try:
      ldx = 5 + (len(self.game_state.done.items) * 10)
      ldy = 222
      lframes = 8
      for lcard_index in range(0, len(lcard_done)):
        lcard = lcard_done.pop()
        lx = lcard.x
        ly = lcard.y
        lxchange = ((ldx - lx) / float(lframes))
        lychange = ((ldy - ly) / float(lframes))
        for lframe_index in range(0, lframes + 1):
          lcard.x = lx + (lxchange * float(lframe_index))
          lcard.y = ly + (lychange * float(lframe_index))
          self.screen.blit(self.static_buffer)
          for lcard2 in lcard_done:
            lcard2.update(self.screen)
          lcard.update(self.screen)
          self.screen.swap()
        if lcard.value == cards.ace:
          self.game_state.done.items.append(lcard)
        else:
          self.game_state.done.items[len(self.game_state.done.items) - 1] = lcard
        lcard.update(self.static_buffer)
    finally:
      self.show_selection = True

  def check_selection(self):
    if self.game_complete:
      self.game_state.selected_stack_index = -1
      self.game_state.selected_index = -1
    else:
      lstack = self.selected_stack
      lcount = len(lstack.items)
      if lcount > 0:
        if self.game_state.selected_index >= lcount:
          self.game_state.selected_index = lcount - 1
      else:
        lselected_index = self.game_state.selected_stack_index
        lchange = 0
        lstack_count = len(self.game_state.stacks)
        while True:
          lchange = lchange + 1
          lleft_index = lselected_index - lchange
          lright_index = lselected_index - lchange
          if lleft_index < 0 and lright_index >= lstack_count:
            break
          else:
            if lleft_index >= 0:
              lstack = self.game_state.stacks[lleft_index]
              lcount = len(lstack.items)
              if lcount > 0:
                self.game_state.selected_stack_index = lleft_index
                self.game_state.selected_index = lcount - 1
                break
            if lright_index < lstack_count:
              lstack = self.game_state.stacks[lright_index]
              lcount = len(lstack.items)
              if lcount > 0:
                self.game_state.selected_stack_index = lright_index
                self.game_state.selected_index = lcount - 1
                break
              
  def check_game_complete(self):
    if self.game_complete:
      self.show_select(False, True)
      
  @property
  def game_complete(self):
    lcomplete = True
    for lstack in self.game_state.stacks:
      if len(lstack.items) > 0:
        lcomplete = False
        break
    return lcomplete
        
  def button_down(self, pbuttons):
    if buttons.cross in pbuttons:
      if buttons.left in pbuttons:
        self.move_left()
      if buttons.right in pbuttons:
        self.move_right()
    elif buttons.left_trigger in pbuttons:
      self.do_undo()
    elif buttons.right_trigger in pbuttons:
      self.do_redo()
    elif buttons.triangle in pbuttons:
      self.deal()
    elif buttons.select in pbuttons:
      self.show_select(True, False)
    elif buttons.start in pbuttons:
      self.save_game()
    
  def button_up(self, pbuttons):
    pass

  def button_press(self, pbuttons):
    if not buttons.cross in pbuttons:
      if buttons.left in pbuttons:
        self.select_left()
      if buttons.right in pbuttons:
        self.select_right()
      if buttons.up in pbuttons:
        self.select_up()
      if buttons.down in pbuttons:
        self.select_down()
        
  def calculate_positions(self):
    for lstack in self.game_state.stacks:
      lstack.calculate_positions()

  def update_static(self):
    self.static_buffer.blit(self.background_image, 0, 0, -1, -1, 0, 0, False)
    self.update_stacks()
    self.update_deck()
    self.update_done()
    self.update_buttons()

  def update(self):
    self.screen.blit(self.static_buffer)
    self.update_animation()
    self.super.update(self)
    
  def update_deck(self):
    lcount = int(round(len(self.game_state.deck.items) / 10))
    if lcount > 0:
      limage = tcard_images.back
      lx = 440
      ly = 222
      lby = -5
      for i in range(0, lcount):
        self.static_buffer.blit(limage, 0, 0, -1, -1, lx, ly, True)
        lx = lx + lby
      self.draw_button.draw_button(lx + 13, ly + 14, buttons.triangle, '')
      
  def update_done(self):
    lx = 5
    ly = 222
    lby = 10
    for lcard in self.game_state.done.items:
      lcard.x = lx
      lcard.y = ly
      lcard.update(self.static_buffer)
      lx = lx + lby

  def update_stacks(self):
    for lstack in self.game_state.stacks:
      lstack.calculate_positions()
      lstack.update(self.static_buffer)

  def show_select(self, pallow_continue, pcompleted):
    lselect = select.tselect(self.game_state.game_type, pallow_continue, pcompleted)
    lselect.show()
    if pcompleted or lselect.restart:
      self.game_state.game_type = lselect.game_type
      self.init_deal()
      
  def update_buttons(self):
    lx = 160
    ly = 236
    self.draw_button.draw_button(lx, ly, buttons.cross, 'Drag')
    lx = lx + 60
    self.draw_button.draw_button(lx, ly, buttons.select, 'Menu')
    lx = lx + 60
    self.draw_button.draw_button(lx, ly, buttons.start, 'Save')
    
  def update_animation(self):
    if self.show_selection:
      lselected = self.selected_item
      try:
        self.card_selection.update(self.screen, lselected.x - 7, lselected.y - 8)
      except:
        pass

  def show(self):
    if self.load_game():
      self.show_select(True, False)
      self.update_static()
    else:
      self.show_select(False, False)
    self.super.show(self)
    
  def copy_undo(self):
    self.redo = []
    self.undo.append(self.game_state.duplicate())
    
  def copy_redo(self):
    self.redo.append(self.game_state.duplicate())
    
  def do_undo(self):
    if len(self.undo) > 0:
      self.copy_redo()
      self.game_state = self.undo.pop()
      self.update_static()
    
  def do_redo(self):
    if len(self.redo) > 0:
      self.undo.append(self.game_state.duplicate())
      self.game_state = self.redo.pop()
      self.update_static()

  def load_game(self):
    try:
      self.game_state.load_from_file('save_game.dat')
      return True
    except:
      return False
    
  def save_game(self):
    self.game_state.save_to_file('save_game.dat')
    
    
