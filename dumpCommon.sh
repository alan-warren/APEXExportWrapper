#!/bin/bash
if [ "$(uname)" == "Darwin" ]; then
	curOS="OSX"
elif [ "$(expr substr $(uname -s) 1 5)" == "Linux" ]; then
	curOS="LINUX"
elif [ "$(expr substr $(uname -s) 1 10)" == "MINGW32_NT" ]; then
	curOS="MINGW32"
elif [ "$(expr substr $(uname -s) 1 6)" == "CYGWIN" ]; then
	curOS="CYGWIN"
fi

oldCP=$CLASSPATH
pushd `dirname $0` > /dev/null
basePath=`pwd`
popd > /dev/null
CLASSPATH=$basePath
CLASSPATH=$basePath:$basePath/APEX_Export_JARs/
CLASSPATH=$CLASSPATH:$basePath/APEX_Export_JARs/ojdbc6.jar

if [[ $curOS == "CYGWIN" ]]; then
	echo "Running on Cygwin"
	#MINGW32 automatically converts paths, for Cygwin we need to use the cygpath tool
	#This assumes the java executable under Cygwin is the Windows binary, and not one
	#installed by Cygwin
	WinClassPath=`cygpath -d $basePath`
	tmp=`cygpath -d $basePath/APEX_Export_JARs/`
	WinClassPath="$WinClassPath;$tmp"
	tmp=`cygpath -d $basePath/APEX_Export_JARs/ojdbc6.jar`
	WinClassPath="$WinClassPath;$tmp"
	CLASSPATH=$WinClassPath
fi

echo $CLASSPATH
javaexe=java #require java to be on the path

ipv4="-Djava.net.preferIPv4STack=true"
prog="oracle.apex.APEXExport"

echo -n "DB SID:"
read db
db=`echo $db | tr '[:upper:]' '[:lower:]'`

hostdesc=`grep ^$db  dumpCommon.conf | sed "s/^\$db[	 ]*//"`

if [ -z "$app" ]; then
	echo -n "Application #:"
	read app
fi

if [ -z "$username" ]; then
	echo -n "Username:"
	read username
fi

echo -n "Password for $username@$hostdesc:"
read -s passwd
echo

pushd $APEXBase
cmdStr="$javaexe -cp $CLASSPATH $prog"
cmdStr="$cmdStr -db $hostdesc -user $username"
cmdStr="$cmdStr -applicationid $app"
cmdStr="$cmdStr -skipExportDate -expSavedReports -password"

echo "$cmdStr redacted"
$cmdStr $passwd

mv f$app.sql $alias
cd $alias
cmdStr="$javaexe -cp $CLASSPATH oracle.apex.APEXExportSplitter f$app.sql"
$cmdStr
CLASSPATH=$oldCP
popd
