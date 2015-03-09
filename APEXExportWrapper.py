import AEWUtils
import getpass
import csv
import pprint


AEWUtils.verifyEnvironment()
allHosts = AEWUtils.loadHosts()
allApps = AEWUtils.loadApps()
pp = pprint.PrettyPrinter(indent=4, width=120)

#appNames = [a[allApps["headers"].index("display")] for a in allApps["rows"]]

#hostNames = [a[allHosts["headers"].index("display")] for a in allHosts["rows"]]

appIdx = AEWUtils.doMenu("Which app would you like to export?", allApps)

selApp = allApps[appIdx]

#Only present hosts which have the app
filteredHosts = AEWUtils.filterHosts(selApp, allHosts)
hostIdx = AEWUtils.doMenu("Dump from which host?", filteredHosts)
selHost = filteredHosts[hostIdx]

print("Selected App")
pp.pprint(selApp)

print("Selected Host:")
pp.pprint(selHost)

print("Enter password for " + selApp["OWNER"] + "@" + selHost["connect_string"] + ":")
l_pass = getpass.getpass()
AEWUtils.executeAPEXExport(selHost["connect_string"], l_pass, selApp)
