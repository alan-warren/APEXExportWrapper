from __future__ import print_function
import AEWUtils
import getpass
import csv
import pprint
import sys



allHosts = AEWUtils.loadHosts()
allApps = AEWUtils.loadApps()
pp = pprint.PrettyPrinter(indent=4, width=120)

appIdx = AEWUtils.doMenu("Which app would you like to export?", allApps)

selApp = allApps[appIdx]
pp.pprint(selApp)
print("\n\nSelected App:%s\n" % selApp["display"])
#Only present hosts which have the app
filteredHosts = AEWUtils.filterHosts(selApp, allHosts)
hostIdx = AEWUtils.doMenu("Dump from which host?", filteredHosts)
selHost = filteredHosts[hostIdx]

#print("Selected App")
#pp.pprint(selApp)

#print("Selected Host:")
#pp.pprint(selHost)
if len(sys.argv) == 2 and sys.argv[1] == "-SkipEnvChk":
	print("Skipping environment check")
else:
	AEWUtils.verifyEnvironment(selHost['APEX_Version'])

print("Enter password for %s@%s" % (selApp["OWNER"], selHost["connect_string"]))
l_pass = getpass.getpass()
AEWUtils.executeAPEXExport(selHost, l_pass, selApp)
