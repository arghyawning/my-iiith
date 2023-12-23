#!/bin/bash

echo "Input file name: "
read file

a=$(wc -c <"$file")
b=$(wc -l <"$file")
c=$(wc -w <"$file")

echo "Size of the file: $a bytes"
echo "Total number of lines in the file: $b"
echo "Total number of words in the file: $c"
echo

n=1
while IFS= read -r line; do #linewise reading
	echo "$line" >>"temp.txt" #line stored in temp text file
	w=$(wc -w <"temp.txt") #number of words in line
	echo "Line No: $n - Count of Words: $w" 
	((n = n + 1)) 
	rm "temp.txt"
done <"$file"

echo

grep -wo "[[:alnum:]]\+" "$file" | sort | uniq -c >>"temp.txt" 

while IFS= read -r line; do
	echo "$line" >>"tmp.txt"
	ct=$(echo "$line" | awk '{print $1}')
	word=$(echo "$line" | awk '{print $NF}')
	if [[ "$ct" -ne 1 ]]; then
		echo "Word: $word - Count of Repetition: $ct"
	fi
	rm "tmp.txt"
done <"temp.txt"

rm "temp.txt"

#-wo means -w and -o
#1 is 2nd arg
#2 awk nf gives now per line