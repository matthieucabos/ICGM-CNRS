#!/bin/bash

# Author : CABOS Matthieu
# Date : 22/12/2021

Usage(){

	echo "
Welcome to the associated help of the tokens getter shell script.

Please to use with the correct syntax :

./Treat_tokens.sh <mode>

where mode balance between :

* 1 : Get the IN tokens
* 2 : Get the OUT tokens 
* 3 : Get the IN Tokens Hostname  
* 4 : Get the OUT Toekns Hostname
* 5 : Get the IN Tokens Timestamp Sorted List
* 6 : Get the OUT Tokens Timestamp Sorted List
	"
}

if [ $# -ne 1 ] || ! [[ "$1" =~ [0-9] ]]
then
	echo "Nombre d'argument incorrect"
	Usage
	exit
fi

day=`date | cut -d " " -f1`
month=`date | cut -d " " -f2`
num=`date | cut -d " " -f3`
today="$day $month $num"
today="mer. déc. 15"
cut_line=`cat logwatch | grep -n "$today" | head -1 | grep -Po "\K^[0-9]+"`
nb_line=`wc -l logwatch | grep -Po "\K^[0-9]+"`
read_line=`echo $(($nb_line-$cut_line))`
Content=`cat logwatch | tail -$read_line`
Keep_flag=0
tmp=""
Token_Liste=""
Token_Liste_OUT=""
count=0
User=""

for line in $Content
do
	if [[ "$line" =~ \@.* ]]
	then
		User=`echo $line` 
	fi
	test=`echo $line | grep -Po "\K([0-9]+\:){2}[0-9]+"`
	if [ $Keep_flag -eq 1 ] && [ $count -lt 4 ]
	then
		tmp=$tmp$line  
		count=$((count+1))
		if [ $Keep_flag -eq 1 ] && [ $count -eq 3 ]
			then
				tmp=$tmp$User
				count=4
		fi
	else
		Keep_flag=0
		count=0
	fi
	if [ $count -eq 2 ]
	then
		if ! ([ $line == "IN:" ] || [ $line == "OUT:" ])
		then
			tmp=""
			count=4
		fi
	fi
	if [ -n "$test" ]
	then
		Keep_flag=1
		tmp=$line
	fi
	test=""
	if [ $count -eq 4 ]
	then
		Token_Liste=$Token_Liste" "$tmp
	fi
done

Month=`date +%m`
Day=`date +%d`
Year=`date +%Y`

for line in $Token_Liste
do
	Hour=`echo $line | grep -Po "\K^[0-9]*"`
	Minuts=`echo $line | grep -Po "\K:[0-9]+:" | tr -d ':'`
	Seconds=`echo $line | grep -Po "\K:[0-9]+\(" | tr -d ':('`
	timestamp=`date -d $Year"-"$Month"-"$Day" "$Hour":"$Minuts":"$Seconds +%s`
	# echo $line
	case $1 in 
		1 ) 
			echo $line | grep "IN" | sed 's/(orglab)/-/g' | sed 's/"OriginPro"//g';;
		2 ) 
			echo $line | grep "OUT" | sed 's/(orglab)/-/g' | sed 's/"OriginPro"//g';;
		3 ) 
			echo $line | grep "IN" | grep -Po "\K[\sA-Za-z]*\@.*";; 
		4 ) 
			echo $line | grep "OUT" | grep -Po "\K[\sA-Za-z]*\@.*";;
		5 ) 
			if [[ -n `echo $line | grep "IN"` ]]
			then
				echo $timestamp
			fi;;
		6 ) 
			if [[ -n `echo $line | grep "OUT"` ]]
			then
				echo $timestamp
			fi;;
	esac	
done