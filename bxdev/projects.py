"""

"""

import os
import shutil

from distutils.sysconfig import get_python_lib

def getPRFDir():
	"""Use distutils to find the location of the template .prf files"""
	prfdir = os.path.join(get_python_lib(), "bxdev")
	return prfdir
	
def createProjectDir(directory):
	"""Create a new project directory, return True if successful, False if not"""
	success = True
	if os.path.exists(directory):
		print "  Warning: project directory already exists."
	else:
		try:
			os.mkdir(directory)
			print "  Created project folder " + directory
		except:
			print "  Error: unable to create project directory."
			success = False
	return success
	
def createBXPFile(project, directory):
	"""Create a new BXP (BasicX Project File), return True if successful, False if not"""
	success = True
	try:
		bxp = open(directory + "/" + project + ".bxp", "wt")
		bxp.write(project + ".bas")
		bxp.close()
		print "  Created BasicX Project File " + project + ".bxp"
	except:
		print "  Error: Unable to create BasicX Project File " + project + ".bxp"
		success = False
	return success
		
def createBASFile(project, directory):
	"""Create a new BAS (BasicX source code file), return True if succesful, False if not"""
	success = True
	try:
		bas = open(directory + "/" + project + ".bas", "wt")
		bas.write("Option Explicit\r\r")
		bas.write("Public Sub Main()\r\r")
		bas.write("End Sub")
		bas.close()
		print "  Created BasicX Source Code File " + project + ".bas"
	except:
		print "  Error: Unable to create BasicX Source Code File " + project + ".bas"
		success = False
	return success

def createPRFFile(project, directory, prf):
	"""Copy the specified PRF (BasicX Chip Preferences file) into the project directory, return True if succesful, False if not"""
	success = True
	try:
		prfdest = os.path.join(directory, project + ".prf")
		shutil.copyfile(prf, prfdest)
		print "  Copied BasicX Chip Preferences file into project directory"
	except:
		print "  Error: Unable to copy BasicX Chip Preferences file (.prf)"
		success = False
	return success
