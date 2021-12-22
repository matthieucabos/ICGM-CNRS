import os
import sys

__author__="Matthieu CABOS"
__date__="08/10/2021"

# Usage : python3 Cisco2Socket.py <@IP Switch Cisco> 
# where
# @IP Switch Cisco is the exact @IP of the Cisco Switch to analyse
switch_dict2={
'10.14.0.49':'Balard-1D-1',
'10.14.0.51':'Balard-1G-1',
'10.14.0.58':'Balard-2D-1',
'10.14.0.60':'Balard-2G-1',
'10.14.0.62':'Balard-2H-1',
'10.14.0.67':'Balard-3D-1',
'10.14.0.69':'Balard-3G-1',
'10.14.0.70':'Balard-3G-2',
'10.14.0.74':'Balard-4C-1',
'10.14.0.76':'Balard-4D-1',
'10.14.0.78':'Balard-4G-1',
'10.14.0.80':'Balard-4H-1'
}

Cisco_name=switch_dict2[sys.argv[1]]

Socket_name=[]
for i in range(2,len(sys.argv)):
	Socket_name.append(sys.argv[i])

def Cisco2Socket():
	Cisco_list=['Balard-EP-1','Balard-PAC-1','Balard-PAC-2','Balard-RDC-1','Balard-1C-1','Balard-1D-1','Balard-1G-1','Balard-1G-2','Balard-1H-1','Balard-2C-1','Balard-2D-1','Balard-2G-1','Balard-2H-1','Balard-2H-2','Balard-3C-1','Balard-3D-1','Balard-3G-1','Balard-3G-2','Balard-3H-1','Balard-4C-1','Balard-4D-1','Balard-4G-1','Balard-4H-1']
	f=open("Cisco2Socket.sh","a")
	f.write('#!/bin/bash\n# Author : CABOS Matthieu\n# Date : 08/10/2021\nterm shell\n')

	Cisco_Rep=[]	
	res={}

	for i in range(1,4):
		for j in range(1,49):
			f.write('show interface GigabitEthernet'+str(i)+'/0/'+str(j)+' | grep "N[0-9][A-Z][0-9][0-9]*-[0-9]*" \n')
	f.write('show interface GigabitEthernet0/0/0')
	f.close()
	os.system('ssh '+str(Cisco_name)+" < Cisco2Socket.sh > tmp2.txt")
	os.system('grep -v "^[[:space:]]*$" tmp2.txt > tmp2')
	os.system('rm tmp2.txt')
	i=7
	nb_ligne=int(os.popen('wc -l tmp2 | cut -d " " -f1').read())-i
	ind=1
	jnd=1
	while i <= nb_ligne:
		res[str(ind)+'/0/'+str(jnd)] = os.popen('cat tmp2 | head -'+str(i)+' | tail -2 | grep "N[0-9][A-Z][0-9][0-9]*-[0-9]*" | cut -d " " -f4 | sed "s/,//"').read()
		i+=2
		jnd+=1
		if jnd==49:
			ind=(ind + 1) if (ind <= 4) else 1 
			jnd=1
	os.system('rm tmp2')
	os.system('rm Cisco2Socket.sh')

	rez=[]
	GBname=''
	for socket in Socket_name :
		for k,v in res.items():
			if k==socket:
				GBname=v
				break		
		rez.append(GBname[:-1])
	return rez

test=Cisco2Socket()
print(test)