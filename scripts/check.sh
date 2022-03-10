#!/bin/bash

# Check the data and video of an experiment for a given command set
# timothy.d.drysdale@gmail.com 17 Jan 2022

expt=${1}  #e.g. spin30
steps=${2} #e.g. ../files/step.json
outdir=${3} #e.g. ../log/today

# convert duration into seconds
# https://stackoverflow.com/questions/50433578/how-to-convert-time-period-string-in-sleep-format-to-seconds-in-bash
t2s() {
   sed 's/d/*24*3600 +/g; s/h/*3600 +/g; s/m/*60 +/g; s/s/\+/g; s/+[ ]*$//g' <<< "$1" | bc
}

#Check how long the steps take to run - runtime is in units of seconds 
runtime=0

while IFS='' read -r line || [[ -n "${line}" ]]; do

	delay=$(echo "${line}" | sed 's/ .*//') #get first word on line

	regex="([0-9]*)(\.[0-9]*)?[a-z]" #Check format of delay is in bash format

	if [[ $delay =~ $regex ]]
	then
		duration=$(t2s $delay) 
	    runtime=$(echo "${runtime} + ${duration}" | bc -l)
	fi

done < "$steps"

# Calculate our timeout by rounding to next largest integer (detect . in the runtime)

decimal="([0-9]*)(\.[0-9]*)"
if [[ $runtime =~ $decimal ]]
then
	timeout=$(echo "${BASH_REMATCH[1]} + 1" | bc -l)
else
	timeout=$runtime
fi

overrun=1s

#We cannot collect the data and the video at the same time, because the "collecting" websocat instance does
# not collect more than a single message when run in the background

# Run the file once to get the data

echo "Collecting data for ${timeout}s"

./connect.sh $expt data ${timeout}s ${outdir} ${steps} ${overrun} & #This CAN run in background.

./connect.sh $expt data ${timeout}s ${outdir} #This cannot be run in background, else it just collects one message

# Repeat to collect video

echo "Collecting video for ${timeout}s"

./connect.sh $expt data ${timeout}s ${outdir} ${steps} ${overrun} & #This CAN run in background.

./connect.sh $expt video ${timeout}s ${outdir} #This cannot be run in background, else it just collects one message



								  
								  
								  






