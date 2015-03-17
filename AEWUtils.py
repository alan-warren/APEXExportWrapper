import os
import platform
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
	"APEX_Export_JARs",
	"APEX_Export_JARs" + os.sep + "ojdbc6.jar",
	"APEX_Export_JARs" + os.sep + "oracle" + os.sep + "apex" + os.sep + "APEXExport.class", 
	"APEX_Export_JARs" + os.sep + "oracle" + os.sep + "apex" + os.sep + "APEXExportSplitter.class"
]

cpParts = [
	"APEX_Export_JARs" + os.sep + "ojdbc6.jar",
	"APEX_Export_JARs"
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
			print "Please consult README.md in the APEXExportWrapper base directory for dependency installation instructions"
			raise MissingDependency("Cannot find dependency:" + lookFer)
	getJava()


def executeAPEXExport(p_connstr, p_password, p_app):
	ipv4 = "-Djava.net.preferIPv4Stack=true"
	exportProg = "oracle.apex.APEXExport"
	splitProg = "oracle.apex.APEXExportSplitter"
	javaLoc = getJava()
	outDir = p_app["APP_DIR"]
	cpSep = ""

	if platform.system() == "Windows":
		#Can't use tilde on Windows (it's fine in powershell, but not through Python's system call)
		homeDir = os.environ.get("UserProfile")
		outDir = outDir.replace("/", "\\")
		cpSep = ";"
	else:
		homeDir = os.environ.get("HOME")
		outDir = outDir.replace("\\", "/")
		cpSep = ":"

	myClassPath = "." + cpSep + cpSep.join([scriptPath + os.sep + cp for cp in cpParts])
	envCP = os.environ.get("CLASSPATH")
	if envCP != None:
		print "Appending existing classpath"
		myClassPath += cpSep + envCP
	outDir = outDir.replace("~", homeDir)

	print outDir
	os.chdir(outDir)
	dumpCmd = javaLoc + " -cp " + myClassPath + " " + ipv4 + " " + exportProg + " -db " + p_connstr + " -user " + p_app['OWNER']
	dumpCmd += " -password " + p_password + " -applicationid " + str(p_app["APP_ID"]) + " -skipExportDate -expSavedReports"
	print "Executing:"
	print dumpCmd.replace(p_password, "<redacted>")
	sysRetVal = os.system(dumpCmd)

	if sysRetVal != 0:
		splitCmd = javaLoc + " -cp " + myClassPath + " " + splitProg + " f" + p_app["APP_ID"] + ".sql"
		print "Split Command:"
		print splitCmd
		os.system(splitCmd)
	else:
		print "Export returned non-zero, will not attempt split"

def loadCSV(filename, keyCol):
	csvFile = open(filename)
	csvReader = csv.DictReader(csvFile)
	hotKeys = []
	rArr = []

	for row in csvReader:
		key = row[keyCol]
		#Does it contain a hotkey def'n
		ampIdx = key.find("&")
		if ampIdx != -1:
			hkey = key[ampIdx + 1].upper()
			if hkey == 'Q':
				print "Q is a reserved hotkey, please use something else"
				quit()
			if hkey in hotKeys:
				print "Cannot use the same hotkey (" + hkey + ") twice"
				quit()
			display = key.replace("&", "")
		else:
			hkey = "?"
			display = key
		row["hotkey"] = hkey
		row["display"] = display
 		rArr.append(row)
 		hotKeys.append(hkey)
	return rArr

def loadApps():
	return loadCSV("AEWApps.conf.csv", "NAME")

def loadHosts():
	return loadCSV("AEWHosts.conf.csv", "sid")

def doMenu(prompt, opts):
	hkeys = []
	selIdx = -1
	while(selIdx == -1):
		for opt in opts:
			hkeys.append(opt["hotkey"])
			print "[" + opt["hotkey"] + "] " + opt["display"]
		print prompt
		inp = rosetta_keyboard.getch().upper()
		try:
			selIdx = hkeys.index(inp)
		except:	
			print "Invalid option..."
			if inp == "Q":
				quit()
			else:
				print "Press Q to quit"
			selIdx = -1
	return selIdx

def filterHosts(app, hosts):
	rArr = []
	for host in hosts:
		if app[host["display"]] == 'Y':
			rArr.append(host)
	if len(rArr) == 0:
		raise AttributeError("No hosts matching app")
	return rArr