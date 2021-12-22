#!/bin/bash

# Author : CABOS Matthieu
# Date : 01/10/2021

# To use like : ./Script_sheduler.sh 10.14.0.49 200 
# It will get 200 point values and update Round Robin Archive and associated graph

ip=$1
n_input=$2

i=1
while [ $i -lt $n_input ]
do
	python3 Switch_info_getter.py $ip 
	i=$(( i + 1 ))
done

# ./Get10GSockets.sh $ip $n_input

rrdtool  graph rrdtool_RX_traffic.png -w 800 -h 160 -a PNG --start -60 --end now --title "Transfert (Ko)" DEF:RX=traffic.rrd:RX:AVERAGE LINE2:RX#FF0000

rrdtool  graph rrdtool_Error_traffic.png -w 800 -h 160 -a PNG --start -60 --end now --title "Error (Counter)" DEF:RX=traffic.rrd:Error:AVERAGE LINE2:RX#FF0000