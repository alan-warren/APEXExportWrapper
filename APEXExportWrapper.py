import AEWUtils
import getpass
import csv

AEWUtils.verifyEnvironment()

hostsFile = open("AEWHosts.conf.csv")
hostsReader = csv.reader(hostsFile)
hostsHeaders = hostsReader.next()
allHosts = []

appsFile = open("AEWApps.conf.csv")
appsReader = csv.reader(appsFile)
appsHeaders = appsReader.next()

print "Which app would you like to export?"

for app in appsReader:
	print app.



#l_pass = getpass.getpass()

