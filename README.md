bxdev 0.4 - BasicX Development Libraries
========================================

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

For more information about BasicX, see http://www.basicx.com/

Installation:
----

Clone the project with git:

`$ git clone https://github.com/TC01/bxdev/`

Then cd into the project, build, and install it with setup.py:

```
$ cd bxdev
$ python setup.py build
$ python setup.py install
```

Usage:
----

Begin by creating a new project with bxproj. The -s flag will create a 
subfolder for the project in your current working directory.

`$ bxproj.py -s [ProjectName]`

This will quickly setup a project for you, and allow you to start coding by
editing `[ProjectName].bas.`

When you want to compile code, use bxbuild with the -d flag to download the
code to the microcontroller:

```
$ cd [ProjectName]
$ bxbuild.py -d [ProjectName].bxp
```

The compiler window will appear on the screen for a few seconds during which
the code compiles. Any errors will appear on the terminal window.

Then, should you wish to read debugging messages (Debug.Print) from the device,
run bxdebug with the --port flag to specify what serial port the device is
connected.

`$ bxdebug.py --port PortNumber`

Unplugging the device from the serial port will stop bxdebug.py.

Legality:
----

This program is made by Ben Rosser and distributed under the MIT license (refer
to LICENSE.txt for the full documentation).

It is not made or endorsed by NetMedia, Inc., and uses no code from them. The
only thing it uses is the command line options for the BasicX compiler, which
are well-documented in the compiler's docs.
