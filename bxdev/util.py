"""Utility functions for bxdev

"""

import sys

#Import winreg either from _winreg or winereg
if (sys.platform == "win32" or sys.platform == "cygwin"):
	import _winreg as winreg
	WineException = None
else:
	from bxdev import winereg as winreg
	from winreg import WineException

def getBuildTarget(target):
	"""Parse command line input for the build target to one of the three target values"""
	if target == None or (target != "BX01" and target != "BX24" and target != "BX35"):
		target = "BX24"
	return target
	
def openBasicXKey():
	"""Returns an "opened" BasicX registry key"""
	key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r'Software\VB and VBA Program Settings\BasicX\Config', 0, winreg.KEY_ALL_ACCESS)
	return key