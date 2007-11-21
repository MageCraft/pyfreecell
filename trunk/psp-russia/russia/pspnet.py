#pspnet.py
"""pygame-wrapper to fake pspnet module as found on http://fraca7.free.fr/pspwiki/doku.php?id=pspnet
meant merely to allow pypsp games to be made on a computer

This is under a BSD License, copyright Kousu <kousue@gmail.com> 2006

This doesn't really work right, for example you will still be able to use sockets even when you're disconnected.
There's not much to be done about that.

"""


__author__ = 'Kousu <kousue@gmail.com>'
__copyright__ = 'BSD License, 2006'

from socket import gethostbyname, gethostname

def connectToAPCTL(n = 1, callback = None):
	pass
def disconnectAPCTL():
	pass
def getIP():
	return gethostbyname(gethostname())
