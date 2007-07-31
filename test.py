#!/usr/bin/env python

import gtk
from common import *

sort_line = ['C2','D3','C4','D5','C6','D7','C8','D9','CA','DB','CC','DD']
sort_line.reverse()

def get_card(symbol):
    if symbol == EMPTY:
        return EMPTY
    assert( len(symbol) == 2)
    map_suit={'C':Club, 'D':Diamond, 'H':Heart, 'S':Spade}
    suit = symbol[0]
    value = symbol[1]
    return map_suit[suit] + 4 * (int(value,16)-1)

def get_super_move_availcount(m,n):
    return (n+1)*(2*m+n)/2 + 1

def standard(sample):
    free = [get_card(s) for s in sample['FREE']]
    home = [get_card(s) for s in sample['HOME']]
    field=[]
    for col in sample['FIELD']:
        field.append([ get_card(s) for s in col])
    return free, home, field

#sample 1, EMPTY_FREE:2, EMPTY_FIELD:2
sample_1_limit = get_super_move_availcount(2,2)
sample_1 = {'FREE':[EMPTY,EMPTY,'H5','H6'], 'HOME':[EMPTY,EMPTY,EMPTY,EMPTY],
'FIELD':[ [],[], sort_line, ['H3'], ['SC'], ['H7'], ['SA'], ['C7'],['C3']] }

#column
(
  COLUMN_NAME,
  COLUMN_DESCRIPTION,
  COLUMN_OBJECT
) = range(3)

class TestSample:
    def __init__(self, sample, name, desc, limit):
        self.name = name
        self.sample = sample
        self.desc = desc
        self.limit = limit



def select_test_sample(parent=None):
    samples=[]
    sample1 = TestSample(sample_1, 'sample 1', 'test super move', sample_1_limit)
    samples.append(sample1)
    picker = SamplePicker(samples, parent)
    ret = None
    if picker.run() == gtk.RESPONSE_OK:
        ret = standard(picker.sel_sample)
    picker.destroy()
    return ret

        
    



class SamplePicker(gtk.Dialog):
    def __init__(self, samples, parent=None):
        self.data = samples
        self.sel_sample = None
        gtk.Dialog.__init__(self, 'pick a sample to test', parent, 0,
                ('_OK', gtk.RESPONSE_OK,
                 '_Cancel', gtk.RESPONSE_CANCEL))
        self.__create_model()
        self.__create_treeview()
        self.__fill_treeview()
        self.set_default_size(300,200)
        self.show_all()

    def __append_column(self, title, col_id):
        col = gtk.TreeViewColumn(title, gtk.CellRendererText(), text=col_id)
        col.set_resizable(True)
        self.treeview.append_column(col)

    def __create_model(self):
        self.model = gtk.ListStore(str,str, object)

    def __create_treeview(self):
        sw = gtk.ScrolledWindow()
        sw.set_shadow_type(gtk.SHADOW_ETCHED_IN)
        sw.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        self.vbox.pack_start(sw)
        self.treeview = gtk.TreeView(self.model)
        self.__append_column('Name', COLUMN_NAME)
        self.__append_column('Description', COLUMN_DESCRIPTION)
        #self.treeview.set_headers_visible(False)
        selection = self.treeview.get_selection()
        selection.set_mode(gtk.SELECTION_SINGLE)
        selection.connect('changed', self.sel_changed_cb)
        sw.add(self.treeview)

    def __fill_treeview(self):
        for sample in self.data:
            it = self.model.append()
            self.model.set(it, COLUMN_NAME, sample.name,
                    COLUMN_DESCRIPTION, sample.desc,
                    COLUMN_OBJECT, sample.sample)
            
    def sel_changed_cb(self, selection):
        model, iter = selection.get_selected()
        if iter is not None:
            sel = model[iter]
            self.sel_sample = sel[COLUMN_OBJECT]
            



if __name__ == '__main__':
    select_test_sample(None)








