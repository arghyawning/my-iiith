#!/bin/bash

#var=`wc -l < quotes.txt`
#echo $var

if test -f "speech.txt"; then
	rm "speech.txt"
fi

while IFS= read -r line; do #line extraction
	#echo "$line"
	#cut -d "~" -line- <<< "$s1"
	s1=${line#*~}#name
	s2=${line%~*}#quote
	s="$s1 once said, \"$s2\""
	echo "$s" >>"speech.txt"
done <"quotes.txt"

cat "speech.txt"
