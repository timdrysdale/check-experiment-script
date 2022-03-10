#!/bin/bash

# Read lines from a file, and echo them after delay specified on each line, in the format
# <delay> <line to echo>
# e.g. file contents should look like this
# 0.1s {"set":"mode","to":"position"}
# 0.1s {"set":"parameters","kp":1,"ki":0,"kd":0}
# 0.1s {"set":"position","to":6}
# 3s { "set": "mode", "to": "wait" }
#
#
# Add optional delay on the end of the file (for keeping the pipe open until the timeout stops websocat

regex="([0-9]*)(\.[0-9]*)?[a-zA-Z]" #Check format of delay ok

while IFS='' read -r line || [[ -n "${line}" ]]; do

	delay=$(echo "${line}" | sed 's/ .*//') #get first word on line

	if [[ $delay =~ $regex ]]
	then
		command=$(echo "$line" | sed 's/[^ ]* //' ) #remove first word on line
		sleep $delay && echo "${command}"
	else
		echo "${line}"
	fi

done < "$1"

# do the optional sleep if a valid delay
if [ -n ${2} ]
then
	if [[ ${2} =~ $regex ]]
	then
		sleep ${2}
	fi
fi

	
