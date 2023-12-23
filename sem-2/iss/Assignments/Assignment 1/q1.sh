#!/bin/bash

sed -i "/^$/d" quotes.txt
#sed does text transformations
#-i does it in file
#d is used to refer to the empty lines

cat quotes.txt
#concatenates file and prints on standard output

echo
echo

awk '!a[$0]++' quotes.txt | tee 'dvdv.txt'
#tee reads from the input(i.e modified awk) and writes it to file

rm quotes.txt

cat dvdv.txt >>quotes.txt

rm dvdv.txt
 