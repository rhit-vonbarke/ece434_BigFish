#!/bin/bash

#arg 1 is the video id
#arg 2 is the refresh rate

if [ "$2" == "-d" ]; then
    #echo 'downloaded'
    echo 'Downloading file...'
    ./download.sh "$1"
    echo 'Download complete.'
    sleep 1
fi

ts=`date +%s%N`
./runparralel.sh "./delayplay.sh ${1} ${ts}" "sudo python3 wavprocessor.py ${1} ${ts} ${2:60}"
