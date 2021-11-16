#!/bin/bash

timegoal=`expr $2 + 10000000000`
x=`date +%s%N`
while [ $x -lt $timegoal ]
do
x=`date +%s%N`
done

aplay audiodownloads/${1}.wav
