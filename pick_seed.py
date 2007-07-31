#show a dialog to pick a seed


import gtk
import sys

def pick_seed(value=1, min=1, max=sys.maxint, parent=None):
    picker = SeedPicker(value, min, max, parent)
    seed = picker.run()
    return seed

class SeedPicker:
    def __init__(self, value, min, max, parent=None):
        self.dlg = gtk.Dialog("Choose a game", parent, 0,
                ('_OK', gtk.RESPONSE_OK,
                 '_Cancel', gtk.RESPONSE_CANCEL))
        self.label = gtk.Label('Input seed(1-32000)')
        self.dlg.vbox.pack_start(self.label, padding=10)
        adj = gtk.Adjustment(value, min, max, 1)
        self.entry = gtk.SpinButton(adj)
        self.entry.set_numeric(True)
        self.dlg.vbox.pack_start(self.entry, padding=5)
        self.dlg.show_all()

    def run(self):
        response = self.dlg.run()
        #destroy dialog, must
        self.dlg.destroy()
        if response == gtk.RESPONSE_OK:
            return self.entry.get_value()
        else:
            return None





if __name__ == '__main__':
    pick_seed(max=32000)
    



