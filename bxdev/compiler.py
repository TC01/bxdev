import os
import shutil
import sys

#Import winreg either from _winreg or winereg
if (sys.platform == "win32" or sys.platform == "cygwin"):
	import _winreg as winreg
	WineError = None
else:
	import winereg as winreg
	from winereg import WineError

def pathToNix(pathName):
	"""Convert a Wine style path to a Unix style path"""
	winePath = os.path.expanduser("~/.wine/")
	pathName = pathName.replace(r'\\', "/")
	pathName = pathName.replace("Z:", "")
	pathName = pathName.replace("C:", winePath + "drive_c/")
	return pathName

def pathToWine(pathName):
	"""Convert a nix style path to a Wine style path"""
	winePath = os.path.expanduser("~/.wine/drive_C/")
	if winePath in pathName:
		pathName = "C:" + pathName
	else:
		pathName = "Z:" + pathName
	pathName = pathName.replace("/", r'\\')
	return pathName
	
def getProjectData(fullProject):
	"""Return a tuple of project name, file, and directory from the full path of a project file"""
	filename = fullProject[fullProject.rfind("/") + 1:]
	project, b, c = filename.partition(".")
	directory = fullProject[:fullProject.rfind("/") + 1]
	directory = os.path.abspath(directory)
	return project, filename, directory
	
def setRegistryData(key, directory, target):
	"""Will set the target and directory in the windows/wine registries"""
	success = True
	try:
		winreg.SetValueEx(key, "Work_Dir", 0, winreg.REG_SZ, directory)
		winreg.SetValueEx(key, "Chip_Type", 0, winreg.REG_SZ, target)
	except WineError:
		print "  Error: Wine cannot be running while performing registry operations"
		print "  Please kill any active instances of wine and try again"
		success = False
	return success
	
def getBasicXPath(key):
	"""Retrieves the install directory of the BasicX compiler from the registry"""
	bxPath, garbageType = winreg.QueryValueEx(key, "Install_Directory")
	return bxPath
	
def getCompilerCommand(bxPath, project, download):
	"""Creates a compiler command to build the given BasicX project"""
	command = ""
	bxPath += "\\BasicX.exe"
	if (sys.platform != "win32" and sys.platform != "cygwin"): 
		command = "wine "
		bxPath = pathToNix(bxPath)
	bxPath = '"' + bxPath + '" '
	command += bxPath + project + " /C"
	if download:
		command += " /D"
	return command
	
def runCompilerCommand(command, directory):
	"""Run a given BasicX compiler command and print the output"""
	os.system(command)
	try:
		outputFile = directory + "/BasicX.err"
		output = open(outputFile, 'rt')
		print output.read()
		output.close()
		os.remove(outputFile)
	except:
		print "No compiler output generated"
