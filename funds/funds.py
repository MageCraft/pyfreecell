#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib2
import BeautifulSoup
import gtk
from threading import Thread
import gobject as go
import sys, os

if not os.environ.has_key('http_proxy'):
    os.environ['http_proxy'] = 'http://e2533c:Frank78524#@wwwgate0-ch.mot.com:1080'

data_src = 'http://funds.eastmoney.com/'
funds = [ ['400003', '东方精选', 19417.4700],
          ['050009', '博时新兴', 9852.4900],
	  ['020005', '金马稳健', 19753.6300] ]

def format(e):
    if type(e) == float:
        return "%8.2f" % e
    else:
        return str(e)

def fetch_data_from_web():
    res = urllib2.urlopen( data_src )
    soup = BeautifulSoup.BeautifulSoup(res) 
    print 'fetch done'
    rows = soup.findAll('tr', height="20")
    total_all=0
    th, e = rows[0].findAll('td'), rows[2].findAll('td') 
    price_col, date_info = 3, th[3].nobr.string
    if e[3].string == '---':
        price_col, date_info = 5, th[4].nobr.string
    #print price_col, date_info
    for row in rows[2:]:
        cols = row.findAll('td')
        id, price = cols[1].string, cols[price_col].string
        for fund, i in zip(funds, range(len(funds)) ):
            if fund[0] == id:
                #print id, price
                total = fund[-1] * float(price)
                funds[i].append( float(price) )
                funds[i].append( total )
                total_all += total
    funds.append(['总计:', total_all, '', '', '']) 
    funds.append(['日期:', date_info, '', '', '']) 


(COL_ID, COL_NAME, COL_QUANTITY, COL_PRICE, COL_SUM ) = range(5) 

class FundsInfoDlg(gtk.Dialog):
    def __init__(self, data):
        self.data = data
        gtk.Dialog.__init__(self, '基金信息', None, 0, ('_OK', gtk.RESPONSE_OK))
        self.__create_model()
        self.__create_treeview()
        self.set_default_size(400, 200)
        self.sID = go.idle_add(self.start_thread)
        self.show_all()

    def start_thread(self):
        print 'start_thread...'
        self.set_title( "基金信息(正在读取数据...)" )
        self.thread = Thread(target=self.thread_func)
        self.thread.start()
        print 'start_thread done'

    def thread_func(self):
        print 'run...'
        fetch_data_from_web()
        go.source_remove(self.sID)
        self.sID = go.idle_add( self.idle_fill )
        print 'run done'

    def __append_column(self, title, col_id):
        col = gtk.TreeViewColumn(title, gtk.CellRendererText(), text=col_id)
        col.set_resizable(True)
        self.treeview.append_column(col)

    def __create_model(self):
        self.model = gtk.ListStore(str, str, str, str, str)

    def __create_treeview(self):
        sw = gtk.ScrolledWindow()
        sw.set_shadow_type(gtk.SHADOW_ETCHED_IN)
        sw.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        self.vbox.pack_start(sw)
        self.treeview = gtk.TreeView(self.model)
        self.__append_column('代码', COL_ID)
        self.__append_column('名称', COL_NAME)
        self.__append_column('数量', COL_QUANTITY)
        self.__append_column('净值', COL_PRICE)
        self.__append_column('金额', COL_SUM)
        selection = self.treeview.get_selection()
        selection.set_mode(gtk.SELECTION_SINGLE)
        sw.add(self.treeview)

    def fill_data(self):
        for row in self.data:
            it = self.model.append()
            params = []
            for i in range(5):
                params.append(i)
                params.append( format(row[i]) )
            self.model.set(it, *params)

    def idle_fill(self):
        self.set_title("基金信息")
        self.fill_data()
        go.source_remove(self.sID)

def test_engine():
    fetch_data_from_web()
    print 'Date: %s' % date_info
    for fund in funds:
        print "\t".join([format(i) for i in fund])

def main():
    gtk.gdk.threads_init() #must call this function to use multithread
    dlg = FundsInfoDlg(funds)
    dlg.run()
    dlg.destroy()

if __name__ == '__main__':
    test_engine()
    #main()
    sys.exit()
