#!/bin/bash

if [[ $# -eq 2 ]]
then
        expr $1 \* $2
else
        echo "there must be exactly 2 arguments"
fi