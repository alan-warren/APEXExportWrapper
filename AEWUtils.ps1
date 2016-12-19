Function Verify-Environment-For-Export
{
	Param(
		[String]$APEXVersion
	)
	$goodToGo = 1
	$depends = "APEX_Export_JARs/ojdbc6.jar","APEX_Export_JARs/apex$APEXVersion/oracle/apex/APEXExport.class", "APEX_Export_JARs/apex$APEXVersion/oracle/apex/APEXExportSplitter.class"
	Write-Host "Running in:$scriptPath"
	try {
		$javaExists = Get-Command "java" -ErrorAction Stop
	} catch {
		Write-Host "Can't find Java, make sure it's installed and on your %PATH%"
		$goodToGo = 0
	}

	foreach ( $depend in $depends ) {
		if ( !(Test-Path "$scriptPath/$depend") ) {
			$goodToGo = 0
			Write-Host "Cannot find dependency:"
			Write-Host "	$scriptPath/$depend" -ForegroundColor Red
		}
	}
	return $goodToGo
}

Function Execute-APEX-Export

{
	Param(
		[Object]$myHost,
		[String]$my_password,
		[Object]$myApp
	)
	if($IsWindows){
		$myClassPath = "$scriptPath\APEX_Export_JARs\apex$($myHost.APEX_Version);$scriptPath\APEX_Export_JARs\ojdbc6.jar"
	} else {
		$myClassPath = "$scriptPath/APEX_Export_JARs/apex$($myHost.APEX_Version):$scriptPath/APEX_Export_JARs/ojdbc6.jar"
	}
	$ipv4 = "-Djava.net.preferIPv4Stack=true" # Was having issues with Java defaulting to IPv6
	$exportProgName = "oracle.apex.APEXExport"
	$splitProgName = "oracle.apex.APEXExportSplitter"
	echo $myApp."owner"

	cd ($myApp.app_dir)
	Write-Host "Using classpath:$myClassPath"
	Write-Host "Switched to app directory: $($myApp.app_dir)"
	Write-Host "Connecting as $($myApp.owner)@$($myHost.connect_string) for application $($myApp.app_id)"
	$javaLoc = Get-Command java | Select-Object -first 1
	$javaJobOutput = & $javaLoc.Definition -cp ($myClassPath) ($ipv4) ($exportProgName) -db ($myHost.connect_string) -user ($myApp.owner) -password ($my_password) -applicationid ($myApp.app_id) -skipExportDate -expSavedReports
	Write-Host $javaJobOutput
	$javaJobOutput = & $javaLoc.Definition -cp ($myClassPath) ($splitProgName) ("f$($myApp.app_id).sql")
	Write-Host $javaJobOutput
}
