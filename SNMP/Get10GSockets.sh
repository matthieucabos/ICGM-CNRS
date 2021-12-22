#!/bin/bash

# Author : CABOS Matthieu
# Date : 08/10/2021

Ip_switch=$1
n_input=$2
i=1

tmp_value=0
value=0
snmpwalk -v 1 -c comaccess $Ip_switch:161 1.3.6.1.2.1.2.2.1.2 | grep "TenGigabitEthernet" > tmp
nb_lines=`wc -l tmp | cut -d " " -f1` 
count=1
res=''
if [ ! -e traffic10G.rrd ]
then
	rrdtool create traffic10G.rrd --step 1 DS:RX:COUNTER:60:U:U RRA:AVERAGE:0.5:1:60
	chmod 777 traffic10G.rrd
fi
while [ $i -lt $n_input ]
do
	while [ $count -le $nb_lines ]
	do
		num_10G+=`cat tmp | head -$count | tail -1 | cut -d '.' -f2 | cut -d " " -f1`
		# test+=`cat tmp | head -$count | tail -1 | grep -Po '\K[0-9]/[0-9]/[0-9]*'`
		num_10G+=" "
		# test+=" "
		count=$(( count + 1 ))
	done

	tmp_value=0
	for item in $num_10G
	do
		# Commande info SNMP Octets sortants
		tmp_value=`snmpget -v 1 -c comaccess 10.14.0.49:161 1.3.6.1.2.1.2.2.1.16.$item | grep -Po '\K[0-9][0-9]*' | tail -1`
		value=$(( (value + tmp_value)))
	done
	rrdupdate traffic10G.rrd -t RX N:$value
	i=$(( i + 1 ))
done
rrdtool  graph rrdtool_10G_Node_traffic.png -w 800 -h 160 -a PNG --start -60 --end now --title "10G Sockets Transfert (Octets)" DEF:RX=traffic10G.rrd:RX:AVERAGE LINE2:RX#FF0000
rm tmp