Write-Host "Starting APEXExportWrapper"
$scriptPath = Split-Path -parent $MyInvocation.MyCommand.Definition

. "$scriptPath\Select-Item.ps1"
. "$scriptPath\AEWUtils.ps1"

if (Verify-Environment-For-Export){
	Write-Host "Environment configured properly"
} else {
	Write-Host "Environment not configured properly, consult the README"
	return
}

$hostsData = Get-Content $scriptPath\"APEXExportWrapperHosts.conf" | Select -Skip 1 | ConvertFrom-Csv -Delimiter "," -Header "sid","connect_string"
$sidList = $hostsData | Select -Property "sid" -ExpandProperty "sid"

$appHeaders = "name","app_id","owner" + $sidList
$apps = Get-Content $scriptPath\"APEXExportWrapperApps.conf" | Select -Skip 1 | ConvertFrom-Csv -Delimiter "," -Header $appHeaders
$appList = $apps | Select -Property "name" -ExpandProperty "name"

$appNum = Select-Item -Caption "APEXExportWrapper" -Message "Choose an APP to export" -choiceList $appList
$theApp = $apps[$appNum]

#filter the hosts against the selected app
$sidChoices = @()
$hostsData | ForEach {
	$curSid = $_."sid"
	echo $theApp."$curSid"
	IF ($theApp."$curSid" -eq "Y") {
		$sidChoices = $sidChoices + "$curSid"
	}
}

$sidChoiceNum = Select-Item -Caption "APEXExportWrapper" -Message "Choose the SID to use" -choiceList $sidChoices

$theHost = $hostsData | Where {$_.sid -eq $sidChoices[$sidChoiceNum]}
$connect_string = $theHost.connect_string
Write-Host $connect_string

$cred = Get-Credential -credential "$($theApp.owner)@$($theHost.sid)"
#$plainText = $cred.GetNetworkCredential().Password

Execute-APEX-Export $connect_string $cred.GetNetworkCredential().Password $theApp
