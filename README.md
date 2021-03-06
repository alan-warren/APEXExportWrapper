# APEXExportWrapper
The purpose of this project is to simplify the on-demand exporting
and splitting of Oracle Application Express (APEX) code to facillitate
granular version control. 

My fellow developers prefer to avoid the command line, and aren't familiar
with Java. This tool allows them to participate in our version control
from stock Windows and stock OSX platforms.

The download includes example configuration files,
but this repository is setup to ignore actual config files (to prevent accidentally 
pushing configuration to github). So, I reccommend versioning your config
files separately, and linking them.

## Oracle Provided Java Dependencies
The actual exporting and splitting of the application is handled by
Java classes provided by Oracle, as part of the APEX distribution,
with database connectivity via JDBC.

Since I don't believe I can legally re-distributte Oracle's files, you
must obtain those JARs yourself.

### From APEX
Download the APEX distribution from 
[OTN's APEX Download Page](http://www.oracle.com/technetwork/developer-tools/apex/downloads/index.html?ssSourceSiteId=otnru)

Once you've downloaded the .zip file, copy $zipbase/apex/utilities/oracle/apex/\*.class
to the ./APEX\_Export\_JARs/oracle/apex/ directory.

### From the Instant Client
You'll also need to download the 
[Oracle Instant Client](http://www.oracle.com/technetwork/database/features/instant-client/index-097480.html),
then locate ojdbc6.jar (likely in $zipbase/instant\_client_\*/ojdbc6.jar) and copy it to ./APEX\_Export\_JARs

##### Note
If you understand Java and classpaths, you can place these files wherever you'd like.  For example, if you
have the instant client already installed and on your CLASSPATH, you don't have to copy objdbc6.jar into
your install folder.  To skip envirnoment validation run with the -SkipEnvChk flag by modifying the 
included shortcut (Windows), or in the APEXExportWrapper.command file (OSX).

## Configuration Files
The configuration files use the CSV format which is easy to parse in both PowerShell and Python.  

You can use Excel (or any text editor) to modify the contents of the configuration files to match 
your environment, use the \*.conf.example.csv files as a starting off point.

I recommend storing and versioning your config files in your main repository, then linking
to it.

##### On Windows As Administrator (cmd.exe)
```cmd
mklink AEWHosts.conf.csv ..\eahr\AEWHosts.conf.csv
mklink AEWApps.conf.csv ..\eahr\AEWApps.conf.csv
```

#### On Windows As Administrator (powershell)
```cmd
New-Item -Path AEWHosts.conf.csv -ItemType SymbolicLink -Value ..\eahr\AEWHosts.conf.csv
New-Item -Path AEWApps.conf.csv -ItemType SymbolicLink -value ..\eahr\AEWApps.conf.csv
```

##### On OSX / *nix as Regular User
```bash
ln -s ../eahr/AEWHosts.conf.csv ./AEWHosts.conf.csv
ln -s ../eahr/AEWApps.conf.csv ./AEWApps.conf.csv
```

### AEWHosts.conf.csv

sid 	| connect\_string
:------ | -------------:
prod	| prodsystem.example.com:1521:prod
dev		| devsystem.example.com:1521:dev
test	| testsystem.example.com:1521:test
findev	| finance\_dev.example.com:1521:findev
finprod	| finance.example.com:1521:finprod

### AEWApps.conf.csv

NAME	| APP\_DIR	| APP\_ID	| OWNER	| dev	| test	| prod	| findev	| finprod	|
:-------|:----------|:---------:|:-----:|:-----:|:-----:|:-----:|:---------:|:---------:|
HR|~/code/HR/APEX/|100|HR\_USER|Y|Y|Y|N|N
FIN|~/code/FIN/APEX/|200|FIN\_USER|N|N|N|Y|Y

## Configuring PowerShell - Running on Windows
PowerShell is included in Windows 7 and 8.  Windows 8 comes with PowerShell 3.0, but these
scripts target 2.0 to minimize requirements.  The default security policy on Windows prevents
execution of PowerShell scripts.

You can enable execution with the
[Set-ExecutionPolicy Cmdlet](http://technet.microsoft.com/en-us/library/ee176961.aspx).

Running PowerShell as Administrator execute:
```powershell
	Set-ExecutionPolicy RemoteSigned
```

## Running on OSX
OSX has included Python since 10.8 "Mountain Lion" released July 2012. You can run the script directly
from the Finder by double clicking on the APEXExportWrapper.command file. You may need to run 
```bash
	chmod +x APEXExportWrapper.command
```

in the terminal to allow execution.

You can also run directly from the terminal in your favourite shell.
