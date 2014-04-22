"""Preliminary Python support for the Wine registry

winereg is an attempt to provide a module similar, but not identical, to the
existing _winreg (or winreg) on Windows for accessing registry keys.

It is only similar because it works very differently from _winreg, opening the
hive files directly and using standard string editing to manipulate them.

Since it works very differently, attempts have been made to provide some
functions which at least appear to act the same as their _winreg counterparts,
but in fact do not (and exist only so an application can use both).

winereg was written as part of the bxbuild project, and so it may or may not be
expanded further to provide full registry editing access. It only provides
a handful of the functions provided by _winreg.

"""

import os

winePath = os.path.expanduser("~/.wine")
HKEY_CURRENT_USER = "user.reg"
HKEY_LOCAL_MACHINE = "system.reg"
HKEY_USERS = "userdef.reg"

#Some useless _winreg constants that we need to emulate (they don't do anything in winereg (yet))
KEY_ALL_ACCESS = 0
KEY_READ = 1
REG_SZ = 2

class RegistryKey:
	"""Class for winereg, this is NOT anything to do with winreg! And therefore behaves more sanely than some wrappers."""
	def __init__(self, hiveFile, keyName):
		self.hiveFile = hiveFile
		self.keyName = keyName
		
	def __str__(self):
		return self.keyName + " in " + self.hiveFile
		
	def __repr__(self):
		return self.keyName + " in " + self.hiveFile
		
	def getHiveName(self):
		"""Return the full path and name of the hive file"""
		global winePath
		return winePath + "/" + self.hiveFile
		
	def getHive(self, mode):
		"""Open the hive file and return a copy in whatever mode is passed"""
		try:
			hive = open(self.getHiveName(), mode)
			return hive
		except IOError:
			return None

# A dummy error message for problems relating to Wine, may add stuff here later.
class WineError(Exception):
	pass

# This is defined by Python, but only on Windows, so we need it for non-win32...
class WindowsError(Exception):
	pass

def isWineRunning():
	"""Check to see if wine is running... we can't edit the registry if it is"""
	# There has *got* to be a better way to do this. This uses os.system and ps, it's awful.
	try:
		os.system("ps -ef | grep wine > ps.out")
		output = open("ps.out", 'rt')
		outText = output.read()
		output.close()
		os.remove("ps.out")
		if "wineserver" in outText:
			return True
		return False
	except:
		return False

def OpenKey(key, subKey, res=None, sam=None):
	"""Opens the specified key. 'key' MUST be a HKEY constant, unlike _winreg."""
	global winePath
	global HKEY_CURRENT_USER
	global HKEY_LOCAL_MACHINE
	
	#_winreg is too complicated for it's own good... fix later
	if (key != HKEY_CURRENT_USER and key != HKEY_LOCAL_MACHINE):
		print "winereg implementation error: 'key' must be a HKEY constant"
		return None
		
	#Fix the double backslash
	subKey = subKey.replace('\\' , '\\\\')
	
	#Try to open, if we find something, return a RegistryKey class
	hiveName = winePath + "/" + key
	try:
		hive = open(hiveName, 'rt')
		hiveData = hive.read()
		if subKey in hiveData:
			regKey = RegistryKey(key, subKey)
			return regKey
		else:
			return None
	except:
		return None

def QueryValue(key, valueName):
	"""Retrieves the data for a specified value name associated with an open registry key"""
	#Verify that this is a valid key
	if key == None:
		return None
	
	#Open the hive file in read mode
	hive = key.getHive('rt')
	hiveText = hive.read()
	hive.close()
	
	#Find the subkey name that we're looking for
	hiveText = hiveText[hiveText.find(key.keyName):]
	hiveText = hiveText[:hiveText.find("\n\n") + 1]
	value = hiveText[hiveText.find(valueName) + len(valueName) + 3:]
	value = value[:value.find("\n") - 1]
	return value
	
def QueryValueEx(key, valueName):
	"""Retrieves the data and datatype for a specified value name associated with an open registry key"""
	#I'm too lazy to implement this
	value = QueryValue(key, valueName)
	return value, 0
	
def SetValue(key, subKey, type, value):
	"""Stores data in the value field of an open registry key."""
	global HKEY_CURRENT_USER
	global HKEY_LOCAL_MACHINE
	
	#The key can't be none
	if key == None:
		return False
		
	#Wine can't be running when we try this operation
	if isWineRunning():
		raise WineError
		
	#_winreg is too complicated for it's own good... fix later
	try:
		if (key == HKEY_CURRENT_USER or key == HKEY_LOCAL_MACHINE):
			print "winereg implementation error: 'key' must NOT be a HKEY constant"
			return False
	except:
		return False
		
	#Now, make a new hive file with the new key (this is an awful way to do it... but whatever)
	hive = key.getHive('rt')
	newHive = ""
	valid = True
	for line in hive:
		#Verify that we haven't found the key yet
		if key.keyName in line:
			valid = False
		
		#If we have not found the key, keep adding lines to the new file; if we have, and we've gotten to the end, resume adding lines normally
		if valid:
			newHive += line
		elif line == "\n":
			valid = False
			
		#If we've found the key check if we've found the right property; if we HAVE, change it
		if not valid:
			if subKey in line:
				line = line[:line.find(subKey) + len(subKey) + 3]
				line += value
				line += '"\n'
			newHive += line
			
	#Write the new hive file
	hive.close()
	hive = key.getHive('wt')
	hive.write(newHive)
	hive.close()
	return True
	
def SetValueEx(key, subKey, datum, type, value):
	"""Retrieves the data and datatype for a specified value name associated with an open registry key"""
	#I'm too lazy to implement this
	value = SetValue(key, subKey, type, value)
	return value, 0
