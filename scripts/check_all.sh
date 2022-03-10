#!/bin/bash

# Run a check on a set of experiments
# ./check_all.sh <name> <from> <to> <steps>
# e.g. ./check_all.sh spin 30 41 ../files/step.json

expt=$1
from=$2
to=$3
steps=$4
outdir=$5

mkdir -p $outdir

for i in $(seq $from $to)
do
	 instance="${expt}${i}"
	 echo "Checking ${instance}"
	./check.sh "${instance}" $steps $outdir
done
