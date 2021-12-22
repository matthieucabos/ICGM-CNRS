import os
import sys
import re
import netmiko

__author__="CABOS Matthieu"
__date__=23/11/2021

IPSwitchs={
    'Balard-1C-1': '10.14.0.47',
    'Balard-1D-1': '10.14.0.49',
    'Balard-1G-1': '10.14.0.51',
    'Balard-1H-1': '10.14.0.54',
    'Balard-2C-1': '10.14.0.56',
    'Balard-2D-1': '10.14.0.58',
    'Balard-2G-1': '10.14.0.60',
    'Balard-2H-1': '10.14.0.62',
    'Balard-2H-2': '10.14.0.63',
    'Balard-3C-1': '10.14.0.65',
    'Balard-3D-1': '10.14.0.67',
    'Balard-3G-1': '10.14.0.69',
    'Balard-3G-2': '10.14.0.70',
    'Balard-3H-1': '10.14.0.72',
    'Balard-4C-1': '10.14.0.74',
    'Balard-4D-1': '10.14.0.76',
    'Balard-4G-1': '10.14.0.78',
    'Balard-4H-1': '10.14.0.80',
    'Balard-EP-1': '10.14.0.40',
    'Balard-PAC-1': '10.14.0.42',
    'Balard-PAC-2': '10.14.0.43'
    }

def Cisco2Socket(Cisco_name):

	# Dictionnary builder function

	print("Building Sockets Database, please to wait few minuts...")
	res={}

	# Writing the associated shell script to be sent to the Cisco ssh access

	f=open("Cisco2Socket.sh","a")
	f.write('#!/bin/bash\n# Author : CABOS Matthieu\n# Date : 08/10/2021\nexit\nterm shell\n')

	for i in range(1,4):
		for j in range(1,49):
			f.write('show interface GigabitEthernet'+str(i)+'/0/'+str(j)+' | grep "N[0-9][A-Z][0-9][0-9]*-[0-9]*" \n')
	f.close()

	# Etablishing an ssh connection with the given Cisco name from function parameter.

	home= os.getenv('HOME')
	user=os.getenv('USER')
	keyfile=home+'/.ssh/cisco'

	ssh_session = netmiko.ConnectHandler(device_type='cisco_ios', ip=IPSwitchs[Cisco_name],username=user, use_keys=True, key_file=keyfile)
	output = ssh_session.send_config_from_file('Cisco2Socket.sh')

	# Read and treat the direct output from the ssh console

	output=output.split('\n')
	indice=0
	regex=r"N[0-9][A-Z][0-9]*-[0-9]*"
	regex2=r"[0-9]/[0-9]/[0-9]*"
	Interface=''
	Description=''
	for line in output:
		matches = re.finditer(regex2, line, re.MULTILINE)
		for matchNum, match in enumerate(matches, start=1):
			Interface=match.group()
		matches = re.finditer(regex, line, re.MULTILINE)
		for matchNum, match in enumerate(matches, start=1):
			Description=match.group()
		if ( Interface != '' and Description != '' ):
			res[Interface]=Description
			Interface=''
			Description=''
	os.system('rm Cisco2Socket.sh')
	ssh_session.disconnect()
	return (res)

#Buildig Error dictionnary

Error_dict={}
Cisco_list=[]
for Cisco in IPSwitchs.keys():
	home= os.getenv('HOME')
	user=os.getenv('USER')
	keyfile=home+'/.ssh/cisco'
	ssh_session = netmiko.ConnectHandler(device_type='cisco_ios', ip=IPSwitchs[Cisco],
                                         username=user, use_keys=True, key_file=keyfile)
	if (ssh_session.send_command("show interface | i err-disable") != '' ):
		Error_dict[Cisco]=ssh_session.send_command("show interface | i err-disable")
		if not Cisco in Cisco_list:
			Cisco_list.append(Cisco)

# Getting exact Gigabit Ethernet Socket from Error dictionnary and store them into Gb_dict Dictionnary

regex=r'([0-9]/){2}[0-9]+'
Gb_dict={}
for k,v in Error_dict.items():
	Gb=[]
	matches = re.finditer(regex, v, re.MULTILINE)
	for matchNum, match in enumerate(matches, start=1):
		Gb.append(match.group())
	Gb_dict[k]=Gb

# Building Socket2Description Dictionnary to associate the Interface Description to the Registred Error File

# Cisco_list=(list(IPSwitchs.keys())) # Get the full Network Dictionnary
Description_dict={}
for Cisco_name in Cisco_list:
	print(Cisco_name)
	Description_dict[Cisco_name]=Cisco2Socket(Cisco_name)

# Update the Regitred Errors txt File with Cisco name, Socket name and Interface Description fields

f=open('Error_liste.txt','a')
for k,v in Gb_dict.items():
	Cisco_name=k
	Socket_name=v
	Description=Description_dict[Cisco_name][Socket_name]
	f.write(str(Cisco_name)+" GigabitEthernet"+''.join(Socket_name)+" | Socket Description : "+str(Description)+"\n")
	# Description=Cisco2Socket(Cisco_name,Socket_name)   # ICI !!!
	# f.write(str(Description) + '\n')
f.close()

# Brownsing Cisco list and write & apply associated shell script

for Cisco in Gb_dict.keys():
	if not Gb_dict[Cisco]==[]:
		home= os.getenv('HOME')
		user=os.getenv('USER')
		keyfile=home+'/.ssh/cisco'
		ssh_session = netmiko.ConnectHandler(device_type='cisco_ios', ip=IPSwitchs[Cisco],
	                                         username=user, use_keys=True, key_file=keyfile)
		for item in Gb_dict[Cisco]:
			if item != None:
				command=['interface GigabitEthernet'+str(item),'shutdown','no shutdown']
				ssh_session.send_config_set(command)
		# ssh_session.send_command("exit\n",expect_string=r"#")
		ssh_session.disconnect()

quit()