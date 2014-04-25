#/usr/bin/env python

import os
import shutil
import sys

from distutils.core import setup

long_desc = """BasicX is a programming language for a series of microcontrollers designed and
built by NetMedia, Inc. These microcontrollers, the BX01, the BX24, and BX35, 
are little more than a modified AVR with a bootloader. However, the presence of
the bootloader means that we can only program them using the BasicX language.

This language is feature-complete with VB 6, and can only be compiled by an IDE 
nearly ten-years old.

These tools are written to change that.

There are three scripts, bxbuild, bxdebug, and bxproj, and a suite of shared
libraries they all depend upon. bxproj will create new BasicX projects, bxbuild
will compile them and download them to target devices, and bxdebug will read
debugging messages being transmitted over RS232 serial communication.

For more information about BasicX, see http://www.basicx.com/
BasicX is a programming language for a series of microcontrollers designed and
built by NetMedia, Inc. These microcontrollers, the BX01, the BX24, and BX35, 
are little more than a modified AVR with a bootloader. However, the presence of
the bootloader means that we can only program them using the BasicX language.

This language is feature-complete with VB 6, and can only be compiled by an IDE 
nearly ten-years old.

These tools are written to change that.

There are three scripts, bxbuild, bxdebug, and bxproj, and a suite of shared
libraries they all depend upon. bxproj will create new BasicX projects, bxbuild
will compile them and download them to target devices, and bxdebug will read
debugging messages being transmitted over RS232 serial communication.

For more information about BasicX, see http://www.basicx.com/"""

scripts = ["bxbuild", "bxdebug", "bxproj"]
if sys.platform == "win32":
	newScripts = []
	# Creating scripts as *.py, because Windows...
	for script in scripts:
		try:
			newScript = script + ".py"
			print "Creating script " + script + " as " + newScript
			shutil.copy(script, newScript)
			newScripts.append(newScript)
		except:
			pass
	if len(newScripts) == len(scripts):
		scripts = newScripts

setup(  name = "bxdev",
	version = "0.5",
	description = "BasicX development libraries",
	long_description = long_desc,
	author = "Ben Rosser",
	license = "MIT",
	author_email = "rosser.bjr@gmail.com",
	url = "http://venus.arosser.com/projects/basicx.html",
	packages = ["bxdev"],
	py_modules = ["winereg"],
	scripts = scripts,
	package_data={'bxdev': ['BX01.prf', 'BX24.prf', 'BX35.prf']} )

try:
	if sys.platform == "win32":
		for newScript in newScripts:
			os.remove(newScript)
except:
	pass
