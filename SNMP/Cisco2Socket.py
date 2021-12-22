import os
import sys

__author__="Matthieu CABOS"
__date__="08/10/2021"

# Usage : python3 Cisco2Socket.py <Switch Cisco Name> 
# where
# @IP Switch Cisco is the exact Name of the Cisco Switch to analyse

Cisco_list=['Balard-EP-1','Balard-PAC-1','Balard-PAC-2','Balard-RDC-1','Balard-1C-1','Balard-1D-1','Balard-1G-1','Balard-1G-2','Balard-1H-1','Balard-2C-1','Balard-2D-1','Balard-2G-1','Balard-2H-1','Balard-2H-2','Balard-3C-1','Balard-3D-1','Balard-3G-1','Balard-3G-2','Balard-3H-1','Balard-4C-1','Balard-4D-1','Balard-4G-1','Balard-4H-1']
f=open("Cisco2Socket.sh","a")
f.write('#!/bin/bash\n# Author : CABOS Matthieu\n# Date : 08/10/2021\nterm shell\n')

Cisco_Rep=[]	
res={}
Cisco_name=sys.argv[1]

for i in range(1,4):
	for j in range(1,49):
		f.write('show interface GigabitEthernet'+str(i)+'/0/'+str(j)+' | grep "N[0-9][A-Z][0-9][0-9]*-[0-9]*" \n')
f.write('show interface GigabitEthernet0/0/0')
f.close()
os.system('ssh '+str(Cisco_name)+" < Cisco2Socket.sh > tmp.txt")
os.system('grep -v "^[[:space:]]*$" tmp.txt > tmp')
os.system('rm tmp.txt')
i=7
nb_ligne=int(os.popen('wc -l tmp | cut -d " " -f1').read())-i
ind=1
jnd=1
while i <= nb_ligne:
	res['GigabitEthernet'+str(ind)+'/0/'+str(jnd)] = os.popen('cat tmp | head -'+str(i)+' | tail -2 | grep "N[0-9][A-Z][0-9][0-9]*-[0-9]*" | cut -d " " -f4 | sed "s/,//"').read()
	i+=2
	jnd+=1
	if jnd==49:
		ind=(ind + 1) if (ind <= 4) else 1 
		jnd=1
os.system('rm tmp')
os.system('rm Cisco2Socket.sh')
Socket_name=input("Entrer le nom complet de la prise (de type N1A01-01) : ")
Socket_name+='\n'
GBname=''
for k,v in res.items():
	if v==Socket_name:
		GBname=k
		break		
print("Le port Gigabit Ethernet associé à la prise "+str(Socket_name)+" sur le Switch Cisco "+str(Cisco_name)+" est : "+str(GBname))
