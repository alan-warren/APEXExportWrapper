import os
import getpass
import csv
from distutils import spawn

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

def loadHosts():
	hostsFile = open("AEWHosts.conf.csv")
	hostsReader = csv.reader(hostsFile)
	hostsHeaders = hostsReader.next()
	rDict = {}

	rDict["headers"] = hostsHeaders
	rDict["rows"] = []
	for i in hostsReader:
		rDict["rows"].append(i)
	return rDict

def loadApps():
	appsFile = open("AEWApps.conf.csv")
	appsReader = csv.reader(appsFile)
	appsHeaders = appsReader.next()
	rArr = []

	for i in appsReader:
		rArr.append(i)
	return rArr

def doMenu(opts):
	for opt in opts:
		print opt