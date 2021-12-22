#!/bin/bash

# Author : CABOS Matthieu
# Date : 15/12/2021

Content=`cat logwatch`
day=`date | cut -d " " -f1`
# echo $day
# day="mar."
month=`date | cut -d " " -f3`
Slice=""
Liste=""
CutFlag=0
del="(orglab)"

for line in $Content
do
	if [ $line == $day ] || [ $line == $month ]
	then
		CutFlag=1
	fi
	if [ $CutFlag -eq 1 ]
	then
		Slice=$Slice$line
	fi
	if [ $line == $day ] && [ $CutFlag -eq 1 ]
	then
		CutFlag=0
		Liste=$Liste" "$Slice
		Slice=""
	fi
done

count=0
Liste2=""
for item in $Liste
do
	if [ $count -gt 2 ]
	then
		Liste2=$Liste2" "$item
	fi
	count=$((count+1))
done

IP_Slice=""
User=""
ip=""
count=0
declare -a IP_list

for item in $Liste2
do
	User=`echo $item | grep -Po "\K[A-Za-z0-9_-]+@[A-Za-z0-9_-]+"`
	ip=`echo $item | grep -Po "\K([0-9]+\.){3}[0-9]+"`
	for elem in $ip  
	do
		if ! [ "$elem" == "10.14.14.20" ]
		then
			IP_Slice=$IP_Slice" ""$elem"
			ip=""
		fi
	done
	if [[ -n "$User" ]]
	then
		IP_list[$count]="$User"":""$IP_Slice"
		count=$((count + 1))
	fi
	IP_Slice=""
	User=""
done

User_IP=""
tmp=""
for i in ${!IP_list[@]}
do
	if [[ -n "$tmp" ]]
	then
		readarray t <<<"$(echo ${IP_list[$i]} $tmp | tr ' ' '\n' | sort | uniq -u)"
		User=`echo ${IP_list[$i]}| grep -Po "\K[A-Za-z0-9_-]+@[A-Za-z0-9_-]+"`
		if ! [[ $User_IP == *$User* ]]
		then
			User_IP=$User_IP" "$User":"${t[0]}
		fi
	fi
	tmp=${IP_list[$i]}
done
echo $User_IP #| grep -Po "\K[A-Za-z0-9_-êïù]+@[A-Za-z0-9_-]+\:([0-9]+\.){3}[0-9]+"