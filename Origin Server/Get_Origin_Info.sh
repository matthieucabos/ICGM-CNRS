#!/bin/bash

# Author : CABOS Matthieu
# Date : 24/01/2022

Content=`./Treat_log_v2.1.sh`                                                                  # Get the user:ip association
IP_list=""
field=""

time_list=""
index=0
Connected=`ssh origin.srv-prive.icgm.fr '/opt/Linux_FLEXnet_Server_ver_11.16.5.1/lmutil  lmstat -a -c /opt/Linux_FLEXnet_Server_ver_11.16.5.1/Licenses/Origin_20jetons.lic | grep "^.*origin\.srv-prive\.icgm\.fr/27000.*"'`

for item in $Connected
do
	time_list=`echo $item | grep -Po "\K[0-9]+\:[0-9]+"`" "$time_list
done

for item in $Content
do
	ip=`echo $item | grep -Po "\K([0-9]+.){3}[0-9]+"`                                          # Get the ip adress
	Info=`ssh tftp grep $ip /var/lib/tftpboot/snoop/\*`                                        # Use the ip adress to request the tftp server
	Cisco=`echo $Info | grep -Po "\Kbalard-[0-9][A-Z]\-[0-9]"`                                 # Filter the cisco name by regular expression pattern
	Vlan=`echo $Info | grep -Po "\K\s[0-9]{3}"`										           # Filter the Vlan identifier by regular expression pattern
	Mac=`echo $Info | grep -Po "\K([0-9a-f]{4}\.){2}[0-9a-f]{4}"`                              # Filter the MAC adress by regular expression pattern
	Socket=`echo $Info | grep -Po "\KGi([0-9]\/){2}[0-9]+"`                                    # Filter the Socket name by regular expression pattern
	Description=`ssh ${Cisco^} "show interfaces description | i "$Socket`                      # Use cisco and socket fields to connect the switch and get description field
	Description=`echo $Description | grep -Po "\K[NRJPASEP]+[0-9A-Z.]+\-[0-9]+"`               # Filter the Description by regular expression pattern
	time=`echo $time_list | cut -d " " -f1`                                                    # Get the time informations associazted to the user
	time_list=`echo $time_list | cut -d " " -f2-`                                              # Compute the rest of the list
	now=`date +%H`":"`date +%M`                                                                # Get the time "now"
	H1=`echo $now | cut -d ":" -f1`                                                            # Get the "now" hours field
	H2=`echo $time | cut -d ":" -f1`                                                           # Get the "start" hours field
	M1=`echo $now | cut -d ":" -f2`                                                            # Get the "now" minuts field
	M2=`echo $time | cut -d ":" -f2`                                                           # Get the "start" minuts field
	host=`echo $item | cut -d "@" -f1`                                                         # Get origin name
	if [[ "$Connected" == *$host* ]]                                                           # Check if user is connected
	then
		Connexion_time=$((M1-M2 + (H1-H2)*60))                                                 # Compute connexion time
		field=$item" "$Cisco" "$Vlan" "$Mac" "$Socket" "$Description" "$Connexion_time" min"   # Results display
	fi
	echo $field >> Origin_Connexion_History                                                    # Put in on screen
done