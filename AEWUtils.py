import os
import getpass
from distutils import spawn

depends = [
	"APEX_Export_JARs" + os.sep + "ojdbc6.jar",
	"APEX_Export_JARs" + os.sep + "oracle" + os.sep + "apex" + os.sep + "APEXExport.class", 
	"APEX_Export_JARs" + os.sep +"oracle" + os.sep + "apex" + os.sep + "APEXExportSplitter.class"
]

scriptPath = os.path.dirname(os.path.realpath(__file__))

def getJava():
	l_java = spawn.find_executable("java")
	if l_java is None:
		print "Cannot find java"
		raise
	return l_java

def verifyEnvironment():
	for d in depends:
		lookFer = scriptPath + os.sep + d
		print(lookFer)
		if not os.path.exists(lookFer):
			print "Cannot find dependency:" + d
			raise
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
