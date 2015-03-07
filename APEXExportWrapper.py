import AEWUtils
import getpass
import csv


AEWUtils.verifyEnvironment()
allHosts = AEWUtils.loadHosts()
allApps = AEWUtils.loadApps()

appNames = [a[allApps[allApps["headers"].indx("NAME")] for a in allApps]

hostNames = [a[allhosts["headers"].index("sid")] for a in allHosts]
print "Which app would you like to export?"


for app in allApps:
	print app[appsHeaders.index("NAME")]



#l_pass = getpass.getpass()

