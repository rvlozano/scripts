#!/bin/bash 
# Written by: rlozano@streamsets.com
# Description:
# BASH Script to periodicly check available files that are available using ulimit..
# Good Reference to troubleshooting these types of issue.
# http://www.mastertheboss.com/java/hot-to-solve-the-too-many-open-files-error-in-java-applications/


function printusage {
    echo "Usage: ./filesopend.sh [ -p STREAMSETSPID ] [ -t tics ]  -f filenameURI ]"
    Checks a Single Time the number of files that are available using ulimit.
    echo "    /tmp/filesopend.sh -p 95609 -t 1 -f /tmp/output"
    Continually checks number of files that are available using ulimit.
    echo "    /tmp/filesopend.sh -p 95609 -t all -f /tmp/output"
}

while getopts p:t:f:h: flag
do
    case "${flag}" in
        p) pid=${OPTARG};;
        t) tics=${OPTARG};;
        f) file=${OPTARG};;
        :) printusage;;
        *) printusage;;
    esac
done

# stops your script if any simple command fails. 
set -e

# function to collect data
function collect {
    lssouput=$(lsof -p $pid)
    echo "$lssouput" > $file"_lsof"
    ulcurr=$(cat $file"_lsof" | wc -l | xargs)
    ulconf=$(ulimit -n)
    let ulatm=ulconf-ulcurr
    echo $(date +"%Y-%m-%d %T") $ulatm >> $file
}

echo "tics: " $tics

if [[ $tics != "all" ]]
then
        collect || echo "Error occured"
else

	while [ TRUE ]; do 
		sleep 60
		collect || echo "Error occured"
	done
fi
