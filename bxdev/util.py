"""Utility functions for bxdev

"""

import sys

#Import winreg either from _winreg or winereg
if (sys.platform == "win32" or sys.platform == "cygwin"):
	import _winreg as winreg
	WineError = None
else:
	import winereg as winreg
	from winereg import WineError

def getBuildTarget(target):
	"""Parse command line input for the build target to one of the three target values"""
	if target is None or (target != "BX01" and target != "BX24" and target != "BX35"):
		target = "BX24"
	return target
	
def openBasicXKey():
	"""Returns an "opened" BasicX registry key"""
	key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r'Software\VB and VBA Program Settings\BasicX\Config', 0, winreg.KEY_ALL_ACCESS)
	return key
