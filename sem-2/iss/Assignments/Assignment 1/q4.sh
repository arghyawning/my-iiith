#!/bin/bash

#arr=(21 22 34 1 7 90 101 2 4 8 45)
#n=11
IFS=","
read -a arr

n=${#arr[@]}
#echo $n
echo
echo "Array input:"
echo ${arr[*]}
echo

for ((i = 0; i < n; i++)); do

	for ((j = 0; j < n - i - 1; j++)); do

		if [ ${arr[j]} -gt ${arr[$((j + 1))]} ]; then
			temp=${arr[j]}
			arr[$j]=${arr[$((j + 1))]}
			arr[$((j + 1))]=$temp
		fi
	done
done

echo "Sorted array:"
echo ${arr[*]}
