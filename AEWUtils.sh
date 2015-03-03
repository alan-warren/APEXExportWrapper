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
	appHeaders=`head -n1 $filename`
	echo "Possible Apps"
	awk -F"," '{if (NR!=1) {printf "%s\n", $1}}' $filename
	echo -n "Pick App to export:"
	read myApp
	appLine=`grep -i "^$myApp," $filename`
	if [ $? -eq 0 ]; then
			outp=$appLine
			return 0
	else
			echo "Not a valid app"
			return 1
	fi
}

function fieldFromCSV() {
	$headers=$1
	$line=$2
	$fieldName=$3
	echo $headers |awk ' 
	BEGIN { count=0; quote=0}
    { for (i=1;i<=length($0);i++)
      {
      	  if(substr($0,i,1)=="\"") { quote=!quote; continue};
          if(substr($0,i,1)=="," && quote==0) {count++;}
      }
    }
    END {print count}'
}
