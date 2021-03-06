#!/bin/bash

# usage: ./connect.sh <expt> <stream>
# tokens and access files are assumed to be in ../autogenerated
# with naming convention:
# access file: <stream>.access.<expt>
# token file: <stream>.token.<expt>
#
# an example commmand: ./connect.sh spin30 log 20
# this puts incoming data to spin30-log-<timestamp>.json for 20 seconds
#
# timothy.d.drysdale@gmail.com
# 17 Jan 2022

dir=../autogenerated

# parse arguments
expt=${1}  #e.g. spin30
stream=${2} #e.g. log
duration=${3} #in bash time (support only seconds, minutes, hours, days)
outdir=${4}


# retrieve access
access=$(cat $dir/$stream.access.$expt)

# retrieve token
token=$(cat $dir/$stream.token.$expt)

# generate output filename with timestamp
suffix="json"

if [[ "$stream" == "video" ]]
then
	suffix="ts"
fi

out=$outdir/$expt-$stream-$(date +%s).$suffix

response=$(curl -X POST -H "Authorization: ${token}" $access --silent)

websocket=$(echo $response | jq -r '.uri')

if [[ "$websocket" == "null" ]] 
then
	echo "Error connecting to:" ${access}
	echo $response
	echo "token:" $token
	exit 1
fi

format="binary"

if [[ "$stream" == "video" ]]
then
	format="binary"
fi

#set -x # DEBUG ON

# Things that seem to only get a single message ...
# websocat --$format $websocket - > $out &
#{ websocat --$format $websocket - > $out; } &

# convert duration into seconds
# https://stackoverflow.com/questions/50433578/how-to-convert-time-period-string-in-sleep-format-to-seconds-in-bash
t2s() {
   sed 's/d/*24*3600 +/g; s/h/*3600 +/g; s/m/*60 +/g; s/s/\+/g; s/+[ ]*$//g' <<< "$1" | bc
}

seconds=$(t2s $duration)

#Use timeout script to avoid websocat only writing a single message to file when backgrounded

if [ -n "${5}" ]
then
	#test sh-c on command line websocat - sh-c:"./play.sh ../files/step.json"

	./timeout.sh -t $seconds websocat --$format $websocket sh-c:"./play.sh ${5} ${6}" #do not pipe to file (it will be empty)
	
else
    ./timeout.sh -t $seconds websocat --$format $websocket - > $out
fi

#set +x #DEBUG OFF
