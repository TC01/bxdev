#/usr/bin/env python

import os
import shutil
import sys

from distutils.core import setup

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
	version = "0.4",
	description = "BasicX development libraries",
	long_description = "Software to debug BasicX projects using serial communications (www.basicx.com)",
	author = "Ben Rosser",
	license = "MIT",
	author_email = "rosser.bjr@gmail.com",
	url = "http://venus.arosser.com/projects/basicx",
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
