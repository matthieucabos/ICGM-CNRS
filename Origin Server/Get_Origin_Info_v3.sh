#!/bin/bash

# Author : CABOS Matthieu
# Date : 24/01/2022

Content=`./Treat_log_v2.1.sh`                                                                             # Get the user:ip association
# Content="ruben@DESKTOP-SLFHFQP:10.14.18.144"                                                                                # Get the user:ip association
IP_list=""
field=""

time_list=""
index=0
Connected=`ssh origin.srv-prive.icgm.fr '/opt/Linux_FLEXnet_Server_ver_11.16.5.1/lmutil  lmstat -a -c /opt/Linux_FLEXnet_Server_ver_11.16.5.1/Licenses/Origin_20jetons.lic | grep "^.*origin\.srv-prive\.icgm\.fr/27000.*"'`
# Connected="ruben DESKTOP-SLFHFQP DESKTOP-SLFHFQP (v9.4) (origin.srv-prive.icgm.fr/27000 297), start Tue 1/25 9:58"
old_IFS=$IFS
IFS=$'
'

for item in $Connected
do
	name=`echo $item | grep -Po "\K^\s*[A-Za-zïîëêù\_\-]+"`
	time_list=$time_list" "$name":"`echo $item | grep -Po "\K[0-9]+\:[0-9]+"`"\n"
done

# echo $Content
# echo $Connected
# echo $name
# echo $time_list

for item in $Content
do
	ip=`echo $item | grep -Po "\K([0-9]+\.){3}[0-9]+"` 
	# echo $ip
	find=`grep -no $ip ./DHCPD-conf/*`
	Vlan=`echo $find | grep -Po "\K\-[0-9]{3}"`
	Vlan="${Vlan:1}"
	# echo $Vlan
	nb_line=`echo $find | grep -Po "\K\:[0-9]+\:"`
	nb_line=${nb_line:1}
	nb_line=${nb_line::-1}
	filename=`echo $find | grep -Po "\K\/[a-z0-9\-.]+"`
	filename=${filename:1}
	total_line=`wc -l ./DHCPD-conf/$filename | cut -d " " -f1`
	Info=`cat ./DHCPD-conf/$filename | tail -$((total_line-nb_line+3)) | head -10`
	MAC=`echo $Info | grep -Po "\K([A-Fa-f0-9]{2}\:){5}[A-Fa-f0-9]{2}"`
	# echo $MAC
	Hostname=`echo $Info | grep -Po '\K^host.*{'`
	Hostname=${Hostname::-1}
	Hostname=${Hostname:5}
	# echo $Hostname
	Origin_name=`echo $item | grep -Po "\K^.*\:"`
	Origin_name=${Origin_name::-1}
	# echo $Origin_name
	name=`echo $item | cut -d "@" -f1`
	# echo $name
	time=`echo -e $time_list | grep $name`                                                                 # Get the time informations associazted to the user
	now=`date +%H`":"`date +%M`                                                                            # Get the time "now"
	H1=`echo $now | cut -d ":" -f1`                                                                        # Get the "now" hours field
	H2=`echo $time | cut -d ":" -f2`                                                                       # Get the "start" hours field
	M1=`echo $now | cut -d ":" -f2`                                                                        # Get the "now" minuts field
	M2=`echo $time | cut -d ":" -f3`  
	# echo $H1
	# echo $H2
	# echo $M1
	# echo $M2
	# echo $Info
	# Cisco Socket Description
	MAC=${MAC:0:2}${MAC:3:2}"."${MAC:6:2}${MAC:9:2}"."${MAC:12:2}${MAC:15:2}

	if [[ "$Connected" == *$name* ]]                                                                       # Check if user is connected
	then
		# Description=`ssh ${Cisco^} "show interfaces description | i "$Socket" | tail -1"`                  # Use cisco and socket fields to connect the switch and get description field
		# Description=`echo $Description | grep -Po "\K[NRJPASEP]+[0-9A-Z.]+\-[0-9]+"`                       # Filter the Description by regular expression pattern
		Connexion_time=$((M1-M2 + (H1-H2)*60))                                                             # Compute connexion time
		# field=$item" | "$Cisco" | "$Vlan" | "$Mac" | "$Socket" | "$Description" | "$Connexion_time" min"   # Results display
		# echo $field >> Origin_Connexion_Time                                                              # Put in on screen
	fi
	field=$item" | "$Vlan" | "$MAC" | "$Socket" | "$Hostname" | "$Description" | "$Connexion_time" min"
	echo $field
done
exit

# 1/Recuperer triolet gigabit
# 	ssh Balard-1G-1
# 	show mac address-table | i 7478.27f5.399f 
# 	=> Gi1/0/13
# 2/Recuperer description
# 	ssh Balard-1G-1
# 	show interfaces status | i Gi1/0/13 | i 513
# 	=> Gi1/0/13     N1E14-07, vlan 513 connected    513        a-full a-1000 10/100/1000BaseTX