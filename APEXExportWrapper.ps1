Param (
	[switch]$NoEnvChk = $false
)
Write-Host "Starting APEXExportWrapper"
$scriptPath = Split-Path -parent $MyInvocation.MyCommand.Definition
Write-Host $scriptPath


. "$scriptPath\Select-Item.ps1"
. "$scriptPath\AEWUtils.ps1"

if ($NoEnvChk -eq $true) {
	Write-Host "Skipping environment check"
} elseif (Verify-Environment-For-Export){
	Write-Host "Environment configured properly"
} else {
	Write-Host "Environment not configured properly, consult the README"
	return
}

$hostsData = Get-Content $scriptPath\"AEWHosts.conf.csv" | Select -Skip 1 | ConvertFrom-Csv -Delimiter "," -Header "sid","connect_string"
$sidList = $hostsData | Select -Property "sid" -ExpandProperty "sid"

$appHeaders = "name","app_dir","app_id","owner" + $sidList
$apps = Get-Content $scriptPath\"AEWApps.conf.csv" | Select -Skip 1 | ConvertFrom-Csv -Delimiter "," -Header $appHeaders
$appList = $apps | Select -Property "name" -ExpandProperty "name"

$appNum = Select-Item -Caption "APEXExportWrapper" -Message "Choose an APP to export" -choiceList $appList
$theApp = $apps[$appNum]

#filter the hosts against the selected app
$sidChoices = @()
$hostsData | ForEach {
	$curSid = $_."sid"
	IF ($theApp."$curSid" -eq "Y") {
		$sidChoices = $sidChoices + "$curSid"
	}
}

$sidChoiceNum = Select-Item -Caption "APEXExportWrapper" -Message "Choose the SID to use" -choiceList $sidChoices

$theHost = $hostsData | Where {$_.sid -eq $sidChoices[$sidChoiceNum]}
$connect_string = $theHost.connect_string

$theHost.sid = $theHost.sid -replace "&"
$theApp.name = $theApp.name -replace "&"
$cred = Get-Credential -credential "$($theApp.owner)@$($theHost.sid)"

Execute-APEX-Export $connect_string $cred.GetNetworkCredential().Password $theApp