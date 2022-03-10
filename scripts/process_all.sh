#!/bin/bash

filename='./(\w*)-data-(\w*).json'
processed='.*processed.json'

dir=${1}

for i in ${dir}/*.json; do
	if  ( [[ $i =~ $filename ]] && ! [[ $i =~ $processed ]] )
	then
	        ./process.py --file ${i}
fi
									 
done

	
