#!/bin/bash

# levels to cache
levels=(5 10 25 50 100)

# cli arguements
dataFile=$1
cacheDir=$2
thres=$3

# ensure cache directory
mkdir $cacheDir 2>/dev/null

# start contours
for i in "${levels[@]}"
do
    (
        echo "Caching level: $i"
        python3 genCache.py -e $dataFile $cacheDir/$i.json $i $thres >/dev/null
        echo "Finished level: $i"
    ) &
done
sleep 0.01
echo

# ending message
wait
echo
echo "Finished caching levels:"
echo "${levels[@]}"
