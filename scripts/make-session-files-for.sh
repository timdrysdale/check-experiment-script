#!/bin/sh
mkdir -p ../autogenerated
cd ../autogenerated

echo "making files for experiments in range ${1} - ${2} experiments with topic base-code ${3}"


for i in $(seq $1 $2)
do
    num=$(printf "%02d" $i)
	name="${3}${num}"
	echo $name
	echo "https://relay-access.practable.io/session/${name}-data" > "data.access.${name}"  
	echo "https://relay-access.practable.io/session/${name}-log" > "log.access.${name}"	
	echo "https://relay-access.practable.io/session/${name}-video" > "video.access.${name}"

done