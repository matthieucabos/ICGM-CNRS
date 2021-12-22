#!/bin/bash

# Author : CABOS Matthieu
# Date : 22/10/2021

function Usage(){
 echo"
This script has been written to detect on a Network Monitor all the highThresholdExceeded Errors and get the exact associated Sockets Name
To Use, please to respect the following syntax :

./Get_ThreshlodExceeded.sh 

The Results are stored into the Sockets.txt File.
Please to ensure have the correct rights of connexion into the monitor to test it.
"
}

if [ "$1" == '-h' ]
then
	Usage
	exit
fi

echo "
10.14.0.49 Balard-1D-1
10.14.0.51 Balard-1G-1
10.14.0.58 Balard-2D-1
10.14.0.60 Balard-2G-1
10.14.0.62 Balard-2H-1
10.14.0.67 Balard-3D-1
10.14.0.69 Balard-3G-1
10.14.0.70 Balard-3G-2
10.14.0.74 Balard-4C-1
10.14.0.76 Balard-4D-1
10.14.0.78 Balard-4G-1
10.14.0.80 Balard-4H-1
" > tmp_cisco

ssh -t monitor << EOF 
psql -h localhost -U postgres opennms -c "select * from alarms where lasteventtime > (now() AT TIME ZONE 'Europe/Paris')::date - interval '6 hours';" > Tmp.txt
exit
EOF
scp monitor:./Tmp.txt .
cat Tmp.txt | grep -Po '\K/highThresholdExceeded.*$' | grep -Po '\KGi[0-9]/[0-9]/[0-9]*' > Gi_list
cat Tmp.txt | grep -Po '\K/highThresholdExceeded.*$' | grep -Po '\K[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+' > Ip_list
i=1
count=`wc -l Gi_list | cut -d " " -f1`

while [ $i -le $count ]
do
	Ip=`cat Ip_list | head -$i | tail -1`
	Gi=`cat Gi_list | head -$i | tail -1`
	Cisco=`cat tmp_cisco | grep $Ip | cut -d " " -f2`
	# echo "ssh -t ""$Cisco"
	# echo "show interface description | i"" $Gi"
	ssh  -t "$Cisco" "show interface description | i"" $Gi" >> YO.txt
	i=$(( i + 1 ))
done
rm Gi_list
rm Ip_list
rm tmp_cisco
rm Tmp.txt
cat YO.txt | grep -Po "\KN[0-9][A-Z][0-9]*-[0-9]*" > Sockets.txt 
rm YO.txt
cat Sockets.txt