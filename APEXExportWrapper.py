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
hostIdx = doMenu("Dump from which host?", filteredHosts)
selHost = allHosts[hostIdx]

pp.pprint(selApp)


#l_pass = getpass.getpass()

