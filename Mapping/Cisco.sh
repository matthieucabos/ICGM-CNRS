#!/bin/bash

# Author : CABOS Matthieu
# Date : 08/10/2021

IPSwitch=$1
mode=$2

function Usage(){
	echo " Use of script Cisco.sh :

	./Cisco.sh <@IP Switch Cisco> <mode>

	where :
	* @IP Switch is the exact IP adress of the switch to analyse
	* mode define the way of execution between :
		* 1 : Get the Gigabit Interface from the Cisco Port Number
		* 2 : Get the Cisco Port Number from the Gigabit triolet
	"
}

if [ "$IPSwitch" == "-h" ] || [ "$IPSwitch" == "--help" ]
then
	Usage
	exit
fi

if [ $mode -eq 1 ]
then
	snmpwalk -v 1 -c comaccess $IPSwitch:161 1.3.6.1.2.1.2.2.1.2 | cut -d " " -f4 > tmp
	echo "Veuillez entrer le numero de port du Switch Cisco : "
	read Numero_port
	echo "L'interface Gigabit Associée est :"
	cat tmp | head -$Numero_port | tail -1
	rm tmp
else
	snmpwalk -v 1 -c comaccess $IPSwitch:161 1.3.6.1.2.1.2.2.1.2 | cut -d " " -f4  > tmp
	echo "Veuillez entrer l'interface gigabit associée au Switch Cisco (de la forme 1/2/3) : "
	read Numero_port
	count=1
	while [ $count -le `wc -l tmp | cut -d " " -f1` ]
	do
		test=`cat tmp | head -$count | tail -1 | grep -Po "\K[0-9]/[0-9]/[0-9]*"`
		if [ "$Numero_port" == "$test" ]
		then
			echo "Le numero de port associé est : "$count
			break
		fi
		count=$(( count+ 1 ))
	done
fi