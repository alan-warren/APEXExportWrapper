from __future__ import print_function
import AEWUtils
import getpass
import csv
import pprint
import sys

if len(sys.argv) == 2 and sys.argv[1] == "-SkipEnvChk":
	print("Skipping environment check")
else:
	AEWUtils.verifyEnvironment()

allHosts = AEWUtils.loadHosts()
allApps = AEWUtils.loadApps()
pp = pprint.PrettyPrinter(indent=4, width=120)

appIdx = AEWUtils.doMenu("Which app would you like to export?", allApps)

selApp = allApps[appIdx]

print("\n\nSelected App:%s\n" % selApp["display"])
#Only present hosts which have the app
filteredHosts = AEWUtils.filterHosts(selApp, allHosts)
hostIdx = AEWUtils.doMenu("Dump from which host?", filteredHosts)
selHost = filteredHosts[hostIdx]

#print("Selected App")
#pp.pprint(selApp)

#print("Selected Host:")
#pp.pprint(selHost)

print("Enter password for %s@%s" % (selApp["OWNER"], selHost["connect_string"]))
l_pass = getpass.getpass()
AEWUtils.executeAPEXExport(selHost["connect_string"], l_pass, selApp)
