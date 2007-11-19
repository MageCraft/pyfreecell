from card import *

class tgame_type:
  easy = 0
  medium = 1
  hard = 2
  
class tgame_state:
  deck = None
  stacks = None
  done = None
  selected_stack_index = None
  selected_index = None
  game_type = None
  
  def __init__(self):
    self.deck = tstack()
    self.done = tstack()
    self.stacks = []
    self.selected_stack_index = None
    self.selected_index = None
    self.game_type = tgame_type.easy
    
  def copy_to(self, pgame_state):
    self.deck.copy_to(pgame_state.deck)
    self.done.copy_to(pgame_state.done)

    pgame_state.stacks = []
    for lstack in self.stacks:
      lnew_stack = tstack()
      lstack.copy_to(lnew_stack)
      pgame_state.stacks.append(lnew_stack)
      
    pgame_state.selected_stack_index = self.selected_stack_index
    pgame_state.selected_index = self.selected_index
    pgame_state.game_type = self.game_type
    
  def duplicate(self):
    lresult = tgame_state()
    self.copy_to(lresult)
    return lresult
    
  def save_to_file(self, pfile_name):
    lfile = file(pfile_name, 'w')
    lfile.write(self.get_as_string())
    lfile.close
    
  def load_from_file(self, pfile_name):
    lfile = file(pfile_name, 'r')
    lstring = lfile.read()
    self.set_as_string(lstring)
    lfile.close
    
  def get_as_string(self):
    lresult = self.deck.get_as_string() + '\n' \
        + self.done.get_as_string()
    for lstack in self.stacks:
      lresult = lresult + '\n' + lstack.get_as_string()
    lresult = lresult + '\n' + `self.selected_stack_index` \
         + '\n' + `self.selected_index` \
         + '\n' + `self.game_type`
    return lresult

  def set_as_string(self, pstring):
    llines = pstring.split('\n')
    self.deck.set_as_string(llines.pop(0))
    self.done.set_as_string(llines.pop(0))

    for lstack in self.stacks:
      lstack.set_as_string(llines.pop(0))

    self.selected_stack_index = int(llines.pop(0))
    self.selected_index = int(llines.pop(0))
    self.game_type = int(llines.pop(0))
    

