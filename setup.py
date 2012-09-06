#/usr/bin/env python

from distutils.core import setup

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
	scripts = ["bxbuild.py", "bxdebug.py", "bxproj.py"],
	package_data={'bxdev': ['BX01.prf', 'BX24.prf', 'BX35.prf']} )
