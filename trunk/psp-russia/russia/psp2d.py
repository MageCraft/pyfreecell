#psp2d.py
#pygame-wrapper to fake psp2d module as found on http://fraca7.free.fr/pspwiki/doku.php?id=psp2d
#meant merely to allow pypsp games to be made on a computer

#This is under a BSD License, copyright Kousu <kousue@gmail.com> 2006

from __future__ import division

__author__ = 'Kousu <kousue@gmail.com>'
__copyright__ = 'BSD License, 2006'

#Note to fraca: psp2d is not especially pythonic yet. This is sad. In particular, Controller should 

"""
Todo:
Dump dir() on this module and all classes in the real module and such and implement everything exactly like it should be
Fixup controller mappings to be easier to work with
Protect the display from being reinitialized somehow?
make it wipe the mouse trail every time instead of relying on the user code to wipe the screen. Would have to cache stuff.
"""


import sys
import pygame, SFont
from pygame.locals import *

pygame.init()
pygame.key.set_repeat(500,30)
DEF_FONT = pygame.font.SysFont('Arial', 12)


class Controller:
	"""This class gives access to the state of the pad and buttons. The state is read upon instantiation and is accessible through read-only properties.
                self.start      => K_F1
                self.select     => K_F2
                self.square     => K_i 
                self.triangle   => K_j
                self.circle     => K_l
                self.cross      => K_k 
                self.up         => K_UP or K_a
                self.down       => K_DOWN or K_a
                self.left       => K_LEFT or K_s
                self.right      => K_RIGHT or K_d
                self.l          => K_LSHIFT
                self.r          => K_RSHIFT
	"""
	
	def __init__(self):
		"""Read the current state of the 'controller'.
		This should be read-only to follow fraca's idiot way, but oh well.
		See the code for what each PSP control is mapped to
		
		While the controller has a mousepos property the mouse is being dragged which is mapped to the joystick being moved. mousepos is used to calculate a distance to pretend the joystick is moving.
		"""
		
		#The mouse motion in the X direction, hard limited and normalized to the range -127 and 128.
		#normalize and hardlimit:
		#we'll say 100px = 127 (i.e. the highest is 127)
		#px = 1.27j
		#Npx = n*1.27j
		
		#self.analogX, self.analogY = [1.27*c for c in pygame.mouse.get_rel()]
		self.analogX, self.analogY = 0,0
		if hasattr(self, 'mousepos'):
			newpos = pygame.mouse.get_pos()
			pygame.draw.line(pygame.display.get_surface(), (0,0,0), self.mousepos, newpos)
			pygame.display.flip()
			self.analogX, self.analogY = (b-a for a,b in zip(self.mousepos, newpos))
			#if __debug__: print self.analogX, self.analogY
			if -127>self.analogX: self.analogX=-127
			elif self.analogX>128: self.analogX=128
			if -127>self.analogY: self.analogY=-127 #XXX stupid ugly shit code
			elif self.analogY>128: self.analogY=128
		
		#if __debug__: print (self.analogX, self.analogY)
		#pygame.event.pump() #update the in-memory keystate
		#keys = pygame.key.get_pressed()
                self.start = False
                self.select = False
                self.triangle = False
                self.square = False
                self.circle = False
                self.cross = False
                self.up = False
                self.left = False
                self.down = False
                self.right = False
                self.l = False
                self.r = False
		
		
		
		for e in pygame.event.get():
			if e.type == QUIT: sys.exit(0) #this is a little hook to make the program nice to the rest of the system. Under the assumption that the app will often be querying the controller, this here serves to kill the app if the user clicks close or something
                        if e.type == KEYDOWN:
                            keys = [e.key]
                            #if __debug__ and keys: print keys
                            self.start = K_F1 in keys
                            self.select = K_F2 in keys
                            self.triangle = K_i in keys
                            self.square = K_j in keys
                            self.circle = K_l in keys
                            self.cross = K_k in keys
                            self.up = K_w in keys or K_UP in keys
                            self.left = K_a in keys or K_LEFT in keys
                            self.down = K_s in keys or K_DOWN in keys
                            self.right = K_d in keys or K_RIGHT in keys
                            self.l = K_LSHIFT in keys
                            self.r = K_RSHIFT in keys
			if e.type == MOUSEBUTTONDOWN:
				Controller.mousepos = e.pos #cache the position, used in calculating how much to give to the joystick

			if e.type == MOUSEBUTTONUP:
				del Controller.mousepos




		
#GRAPHICS
class Color:
	"""
	Represents a colour.
	In pygame, this would be:
	(r,g,b) or (r,g,b,a)
	"""
	def __init__(self, r, g, b, a = 255):
		self.red = r
		self.green = g
		self.blue = b
		self.alpha = a
	def tuple(self):
		"""Turns this colour into a pygame-style tuple
		this is a non-standard extension. NOT PART OS PYPSP!"""
		return (self.red, self.green, self.blue, self.alpha)
		#XXX should this skip the alpha in certain cases? e.g. if the alpha is fully opqaue?
	
#A pygame wart is that there is no docs on colours!!! I never knew you could write (r,g,b,a) I thought it was always (r,g,b)


#XXX Look up what these are in the real implementation
IMG_PNG = 0
IMG_JPEG = 1

class Image:
	#self.surface is the pygame surface we are wrapping
	#we don't subclass pygame.Surface to avoid people accidentally calling on pygame methods without realizing it
	def __init__(self, *args):
		"""
		3 different constructors:
		__init__(self, filename)
		__init__(self, w, h)
		__init__(self, img)
		"""
		
		if len(args)==1:
			arg = args[0]
			if type(arg)==type(""): #filename
				self.surface = pygame.image.load(arg)
			elif type(arg)==type(self): #copy an image
				#self.surface = pygame.Surface((surf.get_width(), surf.get_height()), 0, surf)
				self.surface = arg.surface.copy()
			#XXX todo: for compatibility, allow passing in pygame surfaces directly to this
		elif len(args)==2: #
			self.surface = pygame.Surface(args, pygame.SRCALPHA, 32) #args is a double (width, height), just like Surface() wants
		else: raise TypeError("__init__() takes either 1 or 2 arguments (%d given)" % len(args))
	
	def clear(self, color):
		self.surface.fill(color.tuple())
	
	def blit(self, source, sx=0, sy=0, w=-1, h=-1, dx=0, dy=0, blend=False, dw=-1, dh=-1):
		#appearantly this function will resize the surface while blitting
		#XXX this completely ignores alphas. Don't know what to do about that.
		if w == -1: w = source.width
		if h == -1: h = source.height
		
		if dw == -1: dw = source.width
		if dh == -1: dh = source.height
		
		r = source.surface.subsurface((sx,sy,w,h))
		r = pygame.transform.scale(r, (dw,dh))
		
		self.surface.blit(r, (dx,dy))	
	
	def fillRect(self, x, y, w, h, color):
		self.surface.fill((x,y,w,h), color.tuple())
	
	def saveToFile(self, filename, type=IMG_PNG):
		#This isn't exactly right, fraca's implementation (is broken because it lets you pick the extension and the filetype separately) does PNG and JPEG, whereas pygame (just pulls format info direct from the filename) only does BMP and TGA
		pygame.image.save(self.surface, filename)

	def putPixel(self, x, y, color):
		self.surface.set_at((x,y), color.tuple())
	
	def getPixel(self, x, y):
		color = self.surface.get_at((x,y))
		return Color(*color)	
	width = property(lambda self: self.surface.get_width())
	height = property(lambda self: self.surface.get_height())

        def drawLine(self, x0, y0, x1, y1, color):
            pygame.draw.line(self.surface, color.tuple(), (x0,y0), (x1,y1));

        def drawText(self, x, y, text, color):
            t = DEF_FONT.render(text, True, color.tuple())
            self.surface.blit(t, (x, y))


class Screen(Image):
	surface = pygame.display.set_mode((480,272)) #this makes the surface get cached when the module is imported. This isn't always what you want, of course, but it works for the mock up. PSP screen res is 480x272.
	#XXX not quite like fraca. He randomly makes the two classes distinct instead of making one inherit from the other. Oh well.
	
	def __init__(self):
		"""Override the constructor to kill it so
			i) you don't get to pick the info. HAH.
			ii) Screen.surface isn't overriden by self.surface.
		"""
		pass
	def swap(self):
		pygame.display.flip()


class Font(SFont.Font):
	"""Wrap an SFont to make it look like PSP Python fonts"""
	def textWidth(self, text):
		return self.size(text)[0]
	def textHeight(self, text):
		return self.size(text)[1]
	def drawText(self, image, x, y, text):
		self.write(image.surface, (x,y), text)
		#image.surface.blit(self.render(text), (x,y)) #XXX should this be touching the internals of the image like this??)

class BlitBatch:
	def __init__(self): raise NotImplementedError("This class allows the user to batch several blitting operations. It was written for optimization purposes but it doesn\u2019t seem to really make a difference.")


#MISCELLANEOUS
class Mask:
	def __init__(self, img, x, y, w, h, threshold):
		raise NotImplementedError
	def collide(self, msk):
		pass
	def union(self, msk): pass
	def isIn(self, x, y): pass

#XXX Check these
TR_PLUS = 0
TR_MULT = 1
class Transform:
	def __init__(self, *args):
		"""
		__init__(self, type, param)
		__init__(self, cb)
		"""
		if len(args)==2:
			pass
		elif len(args)==1:
			pass
		else: raise TypeError("__init__() takes either 1 or 2 arguments (%d given)" % len(args))

	def apply(self, img):
		pass

class Timer:
	"""Fraca says: 'A timer class that doesn\u2019t run in its own thread (unlike the standard threading.Timer class).'
	Since I really really really don't know how to manage that I'm just going to use threading.Timer
	This timer dies after one run, if you want it to go again you should, as the last thing in fire(), make a new one
	and start it. I think. Hopefully that will still allow the old thread to die.
	"""
	def __init__(self, timeout): #timeout is in milliseconds
		self.t=threading.Timer(timeout/1000, self.fire)
	
	def fire(self): raise NotImplementedError("Timer.fire() must be overridden to be any use, idiot")
	
	def run(self):
		self.t.start()
