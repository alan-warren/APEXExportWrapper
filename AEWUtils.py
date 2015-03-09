import os
import getpass
import csv
from distutils import spawn
import rosetta_keyboard

class MissingDependency(Exception):
	def __init__(self, msg):
		self.msg = msg

	def __str__(self):
		return msg

depends = [
	"APEX_Export_JARs" + os.sep + "ojdbc6.jar",
	"APEX_Export_JARs" + os.sep + "oracle" + os.sep + "apex" + os.sep + "APEXExport.class", 
	"APEX_Export_JARs" + os.sep +"oracle" + os.sep + "apex" + os.sep + "APEXExportSplitter.class"
]

scriptPath = os.path.dirname(os.path.realpath(__file__))

def getJava():
	l_java = spawn.find_executable("java")
	if l_java is None:
		raise MissingDependency("Cannot find java")
	return l_java

def verifyEnvironment():
	for d in depends:
		lookFer = scriptPath + os.sep + d
		if not os.path.exists(lookFer):
			raise MissingDependency("Cannot find dependency:" + lookFer)
	getJava()


def executeAPEXExport(p_connstr, p_password, p_app):
	myClassPath = ";".join([scriptPath + os.sep + d for d in depends])
	ipv4 = "-Djava.net.preferIPv4Stack=true"
	exportProg = "oracle.apex.APEXExport"
	splitProg = "oracle.apex.APEXExportSplitter"
	javaLoc = getJava()

	cmd = javaLoc + " -cp " + myClassPath + " " + ipv4 + " " + exportProg + " -db " + p_connstr + " -user " + p_app['user']
	cmd += " -password " + p_password + " -applicationid " + str(p_app["app_id"]) + " -skipExportDate -expSavedReports"
	print "Command:"
	print cmd

def loadCSV(filename, keyCol):
	csvFile = open(filename)
	csvReader = csv.reader(csvFile)
	csvHeaders = csvReader.next()
	rDict = {}

	csvHeaders.append("hotkey")
	csvHeaders.append("display")
	rDict["headers"] = csvHeaders
	rDict["rows"] = []

	for row in csvReader:
		key = row[csvHeaders.index(keyCol)]
		#Does it contain a hotkey def'n
		ampIdx = key.find("&")
		row.append("hotkey")
		row.append("display")
		if ampIdx != -1:
			hkey = key[ampIdx + 1].upper()
			display = key.replace("&", "")
		else:
			hkey = "?"
			display = key
		row[csvHeaders.index("hotkey")] = hkey
		row[csvHeaders.index("display")] = display
 		rDict["rows"].append(row)
	return rDict

def loadApps():
	return loadCSV("AEWApps.conf.csv", "NAME")

def loadHosts():
	return loadCSV("AEWHosts.conf.csv", "sid")

def doMenu(prompt, opts):
	hkeys = []
	selIdx = -1
	while(selIdx == -1):
		for opt in opts["rows"]:
			hkeys.append(opt[opts["headers"].index("hotkey")])
			print "[" + opt[opts["headers"].index("hotkey")] + "] " + opt[opts["headers"].index("display")]
		print prompt
		inp = rosetta_keyboard.getch().upper()
		try:
			selIdx = hkeys.index(inp)
		except:	
			print "Invalid option..."
			if inp == "Q":
				quit()
			selIdx = -1
	return selIdx