#!/bin/bash

# Author : CABOS Matthieu
# Date : 08/10/2021

# To use like : ./Script_sheduler.sh 10.14.0.49 200 
# It will get 200 point values and update Round Robin Archive and associated graph

function Summ(){
	res=0
	for item in $*
	do
		res=$((res + item))
	done
	return $res
}

ip=$1
n_input=$2
i=1
tmp_value=0
value=0

snmpwalk -v 1 -c comaccess $ip:161 1.3.6.1.2.1.2.2.1.2 | grep "TenGigabitEthernet" > tmp
snmpwalk -v 1 -c comaccess 10.14.0.49:161 1.3.6.1.2.1.2.2.1.2 | grep "GigabitEthernet" > tmp2

nb_lines=`wc -l tmp | cut -d " " -f1` 
nb_lines2=`wc -l tmp2 | cut -d " " -f1` 
count=1
res=''

if [ ! -e traffic.rrd ]
then
	rrdtool create traffic.rrd --step 1 DS:RX10G:COUNTER:60:U:U DS:RX:COUNTER:60:U:U DS:Error:COUNTER:60:U:U RRA:AVERAGE:0.5:1:60
	chmod 777 traffic.rrd
fi

i=1
while [ $i -lt $n_input ]
do
	# python3 Switch_info_getter.py $ip 
	while [ $count -le $nb_lines ]
	do
		num_10G+=`cat tmp | head -$count | tail -1 | cut -d '.' -f2 | cut -d " " -f1`
		num_10G+=" "
		num+=`cat tmp2 | head -$count | tail -1 | cut -d '.' -f2 | cut -d " " -f1`
		num+=" "
		count=$(( count + 1 ))
	done
	tmp_value=0
	value=0
	for item in $num_10G
	do
		# Commande info SNMP Octets sortants 10Gb Sockets
		tmp_value=`snmpget -v 1 -c comaccess $ip:161 1.3.6.1.2.1.2.2.1.16.$item | grep -Po '\K[0-9][0-9]*' | tail -1`
		value=$(( value + tmp_value ))
	done
	rrdupdate traffic.rrd -t RX10G N:$value
	tmp_value=0
	value=0
	for item in $num
	do
		# Commande info SNMP Octets sortants Standards Sockets
		tmp_value=`snmpget -v 1 -c comaccess $ip:161 1.3.6.1.2.1.2.2.1.16.$item | grep -Po '\K[0-9][0-9]*' | tail -1`
		value=$(( value + tmp_value ))
	done
	rrdupdate traffic.rrd -t RX N:$value
	tmp_value=0
	value=0
	for item in $num
	do
		# Commande info SNMP Error All Sockets
		tmp_value=`snmpget -v 1 -c comaccess $ip:161 1.3.6.1.2.1.2.2.1.14.$item | grep -Po '\K[0-9][0-9]*' | tail -1`
		value=$(( value + tmp_value ))
	done
	rrdupdate traffic.rrd -t Error N:$value
	i=$(( i + 1 ))
done

rrdtool  graph rrdtool_RX_traffic.png -w 800 -h 160 -a PNG --start -60 --end now --title "Transfert (Octets)" DEF:RX=traffic.rrd:RX:AVERAGE LINE2:RX#FF0000

rrdtool  graph rrdtool_Error_amount.png -w 800 -h 160 -a PNG --start -60 --end now --title "Error Amount (Counter)" DEF:RX=traffic.rrd:Error:AVERAGE LINE2:RX#FF0000

rrdtool  graph rrdtool_10G_Node_traffic.png -w 800 -h 160 -a PNG --start -60 --end now --title "10G Sockets Transfert (Octets)" DEF:RX=traffic.rrd:RX10G:AVERAGE LINE2:RX#FF0000

rm tmp

rm tmp2