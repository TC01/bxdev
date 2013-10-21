#!/usr/bin/env python

# Note that serial is not shipped with Python on Windows, need to get it manually
# (pip install pyserial, easy_install pyserial, etc)

import argparse
import os
import serial
import sys

from bxdev import debugger
from bxdev import util

#Import winreg either from _winreg or winereg
if (sys.platform == "win32" or sys.platform == "cygwin"):
	import _winreg as winreg
	WineException = None
else:
	import winereg as winreg
	from winereg import WineException
	
def main():
	"""Main function of the program"""
	parser = argparse.ArgumentParser(description="Read messages from a BasicX processor (http://www.basicx.com) sent over RS232 serial communication")
	parser.add_argument("-c", "--configure", dest="portline", help="Configure the port to read from, formatted like ' 3 ,19200,N,8,1'")
	parser.add_argument("-o", "--output", dest="output", help="Output file to write the debugging messages to, defaults to standard output")
	parser.add_argument("-t", "--terminator", dest="terminator", default="\\0", help="Terminating character from processor to indicate end of transmission")
	parser.add_argument("--port", dest= "port", help="Number of the port to monitor, will override but not write to the registry")
	parser.add_argument("--baud", dest="baud", help="Baud rate of the port to monitor, will override but not write to the registry", default="18000")
	parser.add_argument("--stopbits", dest="stopbits", help="Number of stop bits, will override but not write to the registry", default="1")
	parser.add_argument("--parity", dest="parity", help="Parity of the port to monitor, will override but not write to the registry", default="N")
	parser.add_argument("--bytesize", dest="bytesize", help="Size of bytes to read, will override but not write to the registry", default="8")
	args = parser.parse_args()
	
	#Access the registry to get port settings, if configure mode we're setting
	try:
		key = util.openBasicXKey()
		if args.portline != None:
			success = debugger.setBasicXPort(key, args.portline)
			if not success:
				print "Exiting..."
				return
		bxPort = debugger.getBasicXPort(key)
		
		#Now assign these values to the port object
		portSettings = debugger.parsePortSettings(bxPort)
		monitorPort = debugger.createMonitorPort(portSettings)
		if monitorPort == serial.Serial():
			print "Error: malformed port settings in registry"
			return
			
	#If we have a "windows error", the port settings are not in the registry
	except WindowsError:
		print "Error: BasicX port settings not in registry (BasicX may not be installed)"
		print "Attempting to use command line overrides..."
	
	#If overrides were specified using the command line, use them
	try:
		if args.port != None:
			monitorPort.port = int(args.port) - 1
		if args.baud != None:
			monitorPort.baudrate = int(args.baud)
		if args.parity != None:
			monitorPort.parity = args.parity
		if args.bytesize != None:
			monitorPort.bytesize = int(args.bytesize)
		if args.stopbits != None:
			monitorPort.stopbits = int(args.stopbits)
	except:
		print "Error: invalid port options specified on the command line."

	#If an output file is specified, open it now for writing
	outputFile = None
	if args.output != None:
		try:
			fullOutput = os.path.abspath(args.output)
			outputFile = open(fullOutput, 'ab')
		except:
			print "Error: Unable to open specified output file"
			sys.exit(1)
		
	#Try to open the monitor port using pyserial
	try:
		monitorPort.open()
		print "BasicX monitor port opened successfully"
	except:
		print "Error: unable to open monitor port, check connection and settings"
		sys.exit(1)
		
	#Receive debugging messages until either a terminator is received or the port closes
	badExit = False
	while monitorPort.isOpen():
		try:
			debug = monitorPort.readline()
			debug = debug[:-1]
			if debug.lstrip().rstrip() == args.terminator:
				break
			if args.output == None:
				print debug
			elif outputFile != None:
				outputFile.write(debug + "\n")
		except:
			badExit = True
			break
	
	#Close the port, output file (if there was one), and return 1 if bad exit
	monitorPort.close()
	print "Closed BasicX monitor port"
	if outputFile != None:
		outputFile.close()
	if badExit:
		sys.exit(1)

if __name__ == "__main__":
	main()