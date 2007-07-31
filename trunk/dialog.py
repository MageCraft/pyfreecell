#/usr/bin/env python
import pygtk
pygtk.require('2.0')
import gtk

IDLE, FREE, HOME, FIELD = range(4)
EMPTY = -1
DEBUG = True

ACE=0

def fit_home(dst,src):
	if dst == EMPTY:
		return value(src) == ACE
	return suit(src) == suit(dst) and value(src) == value(dst)+1

def fit_field(dst,src):
	if dst == EMPTY:
		return True;
	return value(src) == value(dst) - 1 and (is_black(src) and is_red(dst))

def log(info):
	if DEBUG:
		print info
	

class Engine:
	def __init__(self, free, home, fields, selection):
		self.free = free
		self.home = home
		self.fields = fields 
		self.selection = selection

	def set_notify(self, func):
		self.notify = func

	def set_super_move_notify(self, func):
		self.super_notify = func

	def select(self, area, col):
		if area == FREE:
			self.on_select_free(col)
		elif area == HOME:
			self.on_select_home(col)
		elif area == FIELD:
			self.on_select_field(col)
		else:
			print 'error area:', area
			 
	def auto_play(self):
		pass

	def on_select_free(self, col):
		if self.free[col] != EMPTY:
			return
		notify = False
		src_col = self.selection['col']
		if self.selection["area"] == IDLE:
			print 'free, idle'
			self.selection['area'] = FREE
			self.selection['col'] = col
		elif self.selection['area'] == FREE:
			print 'free 2 free'
			self.free[col] = self.free[src_col]
			self.free[src_col] = EMPTY
			notify = True
		elif self.selection['area'] == HOME:
			print 'home 2 free, impossible, undo later'
		elif self.selection['area'] == FIELD:
			row = len(self.fields[src_col])-1
			dst_v = self.fields[src_col][row]
			self.free[col] = dst_v
			self.fields[src_col].pop()
			notify = True
			#auto_play()
		else:
			assert(False)

		if notify:
			self.notify()

	def on_select_home(self, col):
		notify = False
		src_col = self.selection['col']
		dst_v = self.home[col]
		if self.selection['area'] == IDLE:
			print 'point home'
		elif self.selection['area'] == FREE:
			print 'free 2 home'
			src_v = self.free[src_col]
			if fit_home(dst_v, src_v):
				self.home[col] = src_v
				self.free[src_col] = EMPTY
				notify = True
			else:
				print 'can not move'
		elif self.selection['area'] == HOME:
			print 'home 2 home, impossible'
		elif self.selection['area'] == FIELD:
			print 'field 2 home'
			src_v = self.field[src_col]
			if fit_field(dst_v, src_v):
				self.home[col] = src_v
				self.field[src_col].pop()
				notify = True
			else:
				print 'can not move'
		else:
			assert(False)
				
	def on_select_field(self, col):
		pass



class ScrollWindowTest:

    def __init__(self):
        self.press_count = 0
        self.area_width, self.area_height = 0, 0
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.area = gtk.DrawingArea()
        self.sw = gtk.ScrolledWindow()
        self.sw.add_with_viewport(self.area)
        self.sw.set_policy(gtk.POLICY_NEVER, gtk.POLICY_AUTOMATIC)
        self.sw.connect('size-allocate', self.on_size_allocate)
        self.window.add(self.sw)
        self.window.set_default_size(640,480)
        self.window.set_geometry_hints(self.window, min_height=480, min_width=640)
        self.window.connect('destroy', lambda w: gtk.main_quit())
        self.window.connect("button-press-event", self.on_button_press)
        self.window.set_events(gtk.gdk.BUTTON_PRESS_MASK)
        self.window.show_all()

    def on_button_press(self, widget, event):
        x, y, width, height = self.area.get_allocation()
        print width, height
        if self.press_count == 0:
            self.area_width, self.area_height = width, height
        self.press_count += 1
        if self.press_count % 2 == 0:
            self.area.set_size_request(self.area_width, self.area_height)
        else:
            self.area.set_size_request(self.area_width, self.area_height+20)



    def on_size_allocate(self, widget, allocation):
        x,y,width,height = allocation
        print width,height


    def run(self):
        gtk.main()
        return True




class DialogTest:
	def __init__(self):
		self.w = gtk.Window(gtk.WINDOW_TOPLEVEL)
		self.w.set_title("Dialog Test, click your mouse!")
		self.w.connect("destroy", lambda w: gtk.main_quit())
		self.w.set_default_size(400,300)
		self.w.connect("button-press-event", self.on_button_press)
		self.w.set_events(gtk.gdk.BUTTON_PRESS_MASK)
		self.w.show()

	def create_dlg(self):
		self.dlg = gtk.Dialog("input number dialog", self.w, 0,
				("_OK", gtk.RESPONSE_OK, 
			     "_Cancel", gtk.RESPONSE_CANCEL))
		label = gtk.Label("input seed(0-32000):")
		self.dlg.vbox.pack_start(label)
		entry = gtk.SpinButton()
		#entry.set_range(0,32000)
		self.dlg.vbox.pack_start(entry)
		self.dlg.show_all()
		

	def on_button_press(self, widgt, event):
		print 'button press', event.x, event.y
		self.create_dlg()
		self.dlg.run()
		self.dlg.destroy()
		

	def run(self):
		gtk.main()
		return True


if __name__ == '__main__':
	#DialogTest().run()
    ScrollWindowTest().run()






