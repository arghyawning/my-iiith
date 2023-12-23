#!/bin/bash

echo "Input: "
read s

echo
reverse=$(echo "$s" | rev)
echo "Reverse: $reverse"

revmod=$(echo "$reverse" | tr "0-9a-zA-Z" "1-9a-zA-Z")
echo "Reversed and replaced: $revmod"

length=${#reverse}
l=$(($length / 2))
#echo $l

#for(( i=0; i<$l; i++));
#do

half="${s:0:$l}"
revhalf=$(echo "$half" | rev)
normhalf="${s:$l:$length}"
final="${revhalf}${normhalf}"
echo "Half reversed: $final"

#line 20,22,23: basically substring
