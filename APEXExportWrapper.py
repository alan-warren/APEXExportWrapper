import AEWUtils
import getpass
import csv


AEWUtils.verifyEnvironment()
allHosts = AEWUtils.loadHosts()
allApps = AEWUtils.loadApps()

#appNames = [a[allApps["headers"].index("display")] for a in allApps["rows"]]

#hostNames = [a[allHosts["headers"].index("display")] for a in allHosts["rows"]]

appIdx = AEWUtils.doMenu("Which app would you like to export?", allApps)

selApp = allApps["rows"][appIdx]

print(selApp)
print allApps["headers"]

print allHosts

#l_pass = getpass.getpass()

