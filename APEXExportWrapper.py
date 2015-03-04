import AEWUtils
import getpass
import csv

AEWUtils.verifyEnvironment()

hostsFile = open("AEWHosts.conf.csv")
hostsReader = csv.reader(hostsFile)
hostsHeaders = hostsReader.next()
allHosts = []

for i in hostsReader:
	allHosts.append(i)


appsFile = open("AEWApps.conf.csv")
appsReader = csv.reader(appsFile)
appsHeaders = appsReader.next()
allApps = []

for i in appsReader:
	allApps.append(i)

print "Which app would you like to export?"

for app in allApps:
	print app[appsHeaders.index("NAME")]



#l_pass = getpass.getpass()

