#!/bin/bash

pushd `dirname $0` > /dev/null
myHome=`pwd`
popd > /dev/null

function AEWverifyEnvironment() {
	goodToGo=0
	#Check for java
	which java
	if [ $? -ne 0 ]; then
		echo "Java must be installed, and be present on the path"
		$goodToGo=1
	fi
	#check for installed libraries
	files=( "ojdbc6.jar" "oracle/apex/APEXExport.class" "oracle/apex/APEXExportSplitter.class" )
	for f in "${files[@]}" 
	do
		lib=$myHome/APEX_Export_JARs/$f
		if [ -s "$lib" ]; then
			echo "Found $lib"
		else
			echo "Cannot find $lib"
			goodToGo=1
		fi
	done
	return $goodToGo

}

function possibleSids() {
	filename=$1
	echo "Possible SIDs"
	awk -F"," '{print $1}' $filename
}

function pickApp() {
	filename=$1
	echo "Possible Apps"
	awk -F"," '{if (NR!=1) {printf "%s\n", $1}}' $filename
	echo -n "Pick App to export:"
	read myApp
	appLine=`grep "^$myApp" $filename`
	if [ $? -eq 0 ]; then
			echo "Valid app"
			echo $appLine
			return $appLine
	else
			echo "Not a valid app"
			exit
	fi
}
