#pspsnd.py
#pygame-wrapper to fake pspsnd module as found on http://fraca7.free.fr/pspwiki/doku.php?id=pspsnd
#meant merely to allow pypsp games to be made on a computer

#This is under a BSD License, copyright Kousu <kousue@gmail.com> 2006

import pygame

pygame.mixer.init()

sndFxVolume = 255 #volume of Sound class
musicVolume = 255 #volume of Music class

def setSndFxVolume(volume):
	if 0<=volume<=255:
		global sndFxVolume
		sndFxVolume = volume

def setMusicVolume(volume):
	if 0<=volume<=255:
		global musicVolume
		musicVolume = volume

class Sound:
	loops = 0
	def __init__(self, filename):
		self.snd = pygame.mixer.Sound(filename)
		self.snd.set_volume(sndFxVolume)
	
	def start(self):
		self.snd.play(self.loops)

class Music(Sound):
	"""For now Music is just another Sound, because I have no idea what
	fraca is trying to do by having two classes that do the same thing,
	and even though I could read the source I'm lazy
	(sorry for saying it was closed source though, Fraca)"""
	
	def __init__(self, filename, maxchan = 128, loop = False):
		"""maxchan is I have no clue, loop makes it loop"""
		Sound.__init__(self, filename)
		if loop: self.loops = -1 #play indefinitely
		else: self.loops = 0 #no looping
		self.snd.set_volume(musicVolume)
	
	def stop(self):
		self.snd.stop()
