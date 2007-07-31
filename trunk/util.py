#!/usr/bin/env python
import gtk

class Point:
	def __init__(self,x=0,y=0):
		self.x=x
		self.y=y
	def __add__(self, other):
		return Point(self.x+other.x, self.y+other.y)
	def __sub__(self, other):
		return Point(self.x-other.x, self.y-other.y)


class Rect(gtk.gdk.Rectangle):
	def __init__(self, x=0, y=0, width=0, height=0):
			gtk.gdk.Rectangle.__init__(self, x,y,width,height)

	def right(self): return self.x + self.width-1
	def left(self): return self.x
	def top(self): return self.y
	def bottom(self): return self.y + self.height-1

	def top_left(self): return Point(self.x, self.y)
	def bottom_right(self): return Point(self.right(), self.bottom())

	def contains(self, pt):
		return pt.x in range(self.x, self.right()+1) and pt.y in range(self.y, self.bottom()+1) 

def matrix(col, row, value=None):
	colomn = [ value for i in range(row) ]
	matrix = [ colomn[:] for i in range(col) ]
	return matrix

def to_chr(list):
	return [chr(v) for v in list]

    
def draw3DRect( drawable, gc, rect, color1, color2):
    gc.set_rgb_fg_color(color1)
    drawable.draw_line(gc, rect.x, rect.y, rect.x+rect.width-2, rect.y)
    drawable.draw_line(gc, rect.x, rect.y, rect.x, rect.y+rect.height-2)
    gc.set_rgb_fg_color(color2)
    drawable.draw_line(gc, rect.x+rect.width-1, rect.y+1, rect.x+rect.width-1, rect.y+rect.height-1)
    drawable.draw_line(gc, rect.x+1, rect.y+rect.height-1, rect.x+rect.width-1, rect.y+rect.height-1)


