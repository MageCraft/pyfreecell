#!/usr/bin/env python

import pygtk
pygtk.require('2.0')
import gtk

#column
(
    COLUMN_ID,
    COLUMN_NAME
) = range(2)

#data




class ListSample:
    def __init__(self):
        self.dlg = gtk.Dialog('list sample', None, 0,
                ('_Cancel', gtk.RESPONSE_CANCEL,
                 '_OK', gtk.RESPONSE_OK))
        self.__create_treeview()
        self.__fill_treeview()
        self.dlg.set_default_size(300,400)
        self.dlg.connect('destroy', lambda *w: gtk.main_quit())
        self.dlg.connect('response', self.response_cb)
        self.dlg.show_all()

    def response_cb(self, dialog, reponse_id):
        if reponse_id == gtk.RESPONSE_OK:
            print 'ok'
        elif reponse_id == gtk.RESPONSE_CANCEL:
            print 'cancel'
        self.dlg.destroy()

    def __create_model(self):
        ls = gtk.ListStore(int, str)
        return ls

    def __fill_treeview(self):
        #fill data
        selection = self.treeview.get_selection()
        ls = self.model
        for item in range(10):
            it = ls.append()
            ls.set(it, 
                   COLUMN_ID, item,
                   COLUMN_NAME, 'item %d'%(item)
                   )
            if item == 0:
                selection.select_iter(it)

    def __append_row(self, title, col_id):
        col = gtk.TreeViewColumn(title, gtk.CellRendererText(),
                text=col_id)
        col.set_resizable(True)
        col.set_sort_column_id(col_id)
        self.treeview.append_column(col)

    def __create_treeview(self):
        sw = gtk.ScrolledWindow()
        sw.set_shadow_type(gtk.SHADOW_ETCHED_IN)
        sw.set_policy(gtk.POLICY_NEVER, gtk.POLICY_AUTOMATIC)
        self.dlg.vbox.pack_start(sw)
        
        self.model = self.__create_model()
        self.treeview = gtk.TreeView(self.model)
        selection = self.treeview.get_selection()
        selection.set_mode(gtk.SELECTION_SINGLE)
        selection.connect('changed', self.sel_changed_cb)
        #self.__append_row('ID', COLUMN_ID)
        self.__append_row('Name', COLUMN_NAME)
        self.treeview.set_headers_visible(False)
        sw.add(self.treeview)

    def sel_changed_cb(self, selection):
        model, iter = selection.get_selected()
        row = model[iter]
        print row[COLUMN_ID], row[COLUMN_NAME]
        
def main():
    obj = ListSample()
    gtk.main()

if __name__ == '__main__':
    main()


        

