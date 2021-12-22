#!/bin/bash

# Author : CABOS Matthieu
# Date : 01/12/2021

nb_in=$1

i=1
while [ $i -lt $nb_in ]
do
	python3 Origin_Users.py
	i=$(( i + 1  ))
	sleep 60
done