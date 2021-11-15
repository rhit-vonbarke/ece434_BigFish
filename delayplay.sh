#!/bin/bash

#x=`date +%s%N`
#echo $x
#y=`expr $x / 1000000000`
#echo $y

#accurate* sleep protocol from common time start
timegoal=`expr $2 + 5000000000`
#echo $2
#echo $timegoal
x=`date +%s%N`
while [ $x -lt $timegoal ]
do
x=`date +%s%N`
done

aplay audiodownloads/${1}.wav
