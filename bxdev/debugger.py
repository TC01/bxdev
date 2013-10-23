import serial
import sys

#Import winreg either from _winreg or winereg
if (sys.platform == "win32" or sys.platform == "cygwin"):
	import _winreg as winreg
	WineError = None
else:
	import winereg as winreg
	from winereg import WineError
	from winereg import WindowsError

def parsePortSettings(portString):
	"""Function to parse a registry port string into an array"""
	portSettings = ""
	try:
		portSettings = portString.split(',')
		for i in range(len(portSettings) - 1):
			portSettings[i] = portSettings[i].lstrip().rstrip()
	except:
		# This should really be handled by winereg, since apparently winreg does that.
		# Until I make winereg less sucky, we'll just do it here.
		raise WindowsError
	return portSettings

def getBasicXPort(key):
	"""Retrieves the debugging port information from the registry in the form of a string"""
	bxPort, garbageType = winreg.QueryValueEx(key, "BX24port_Number")
	return bxPort
	
def setBasicXPort(key, portline):
	"""Sets the BasicX serial port information in the registry using the portline string"""
	if len(portline.split(',')) != 5:
		print "  Error: Invalid port settings configure string entered"
		success = False
	try:
		winreg.SetValueEx(key, "BX24port_Number", 0, winreg.REG_SZ, portline)
		print "  Port values updated"
	except WineError:
		print "  Error: Wine cannot be running while performing registry operations"
		print "  Please kill any active instances of wine and try again"
		success = False
	return success
	
def createMonitorPort(portSettings):
	"""Creates a monitor port object using pyserial with specified port settings"""
	monitorPort = serial.Serial()
	try:
		monitorPort.port = int(portSettings[0]) - 1
		monitorPort.baudrate = int(portSettings[1])
		monitorPort.parity = str(portSettings[2])
		monitorPort.bytesize = int(portSettings[3])
		monitorPort.stopbits = int(portSettings[4][0])
	except:
		return serial.Serial()
	return monitorPort
