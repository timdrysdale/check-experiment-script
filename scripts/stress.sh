#!/bin/bash

# Run check all, process the files, and produce latest comparison graphs
# e.g. ./stress.sh spin 30 41 ../files/step.json ../log 10 ../log/summary 6
expt=$1
from=$2
to=$3
steps=$4
out=$5
reps=$6
summary=$7
step=$8 #step in radians in steps file

main=$(date +%Y-%m-%d)


for i in $(seq 0 $reps)
do

	main=$(date +%Y-%m-%d)
	leaf=$(date +%H%M)
    dir="${out}/${main}/${leaf}"
	mkdir -p $dir

	./check_all.sh $expt $from $to $steps $dir

	./process_all.sh $dir

done

mkdir -p $summary
./compare_all.py --root $out --out $summary $step


