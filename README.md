# APEXExportWrapper
The purpose of this project is to simplify the on-demand exporting 
and splitting of Oracle Application Express (APEX) code to facillitate
granular version control.

## Oracle Dependencies
The actual exporting and splitting of the application is handled by
Java classes provided by Oracle, as part of the APEX / APEX Listener
distributions, with database connectivity via JDBC.

Since I don't believe I can legally re-distributte Oracle's files, you
must obtain those JARs yourself, from [OTN's APEX Download Page](http://www.oracle.com/technetwork/developer-tools/apex/downloads/index.html?ssSourceSiteId=otnru)

Once you've downloaded the .zip file, copy $zipbase/apex/utilities/oracle/apex/\*.class 
to the ./APEX_Export_JARs directory/oracle/apex/

You'll also need to download the [Oracle Instant Client](http://www.oracle.com/technetwork/database/features/instant-client/index-097480.html),
then locate ojdbc6.jar (likely in $zipbase/instant_client_\*/ojdbc6.jar)



## Configuration Files

### APEXExportWrapperHosts.conf

### APEXExportWrapperApps.conf

## Configuring PowerShell - Running on Windows

## Running on *nix/OSX


