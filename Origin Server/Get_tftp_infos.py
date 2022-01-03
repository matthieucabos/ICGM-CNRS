import os
import sys
import re
import datetime as dt
import time
import netmiko
from multiprocessing import Process
import multiprocessing
import pyexcel as p

__author__="CABOS Matthieu"
# __date__=03/01/2021

IPSwitchs={
'Balard-1D-1': '10.14.0.49',
'Balard-1G-1': '10.14.0.51',
'Balard-2D-1': '10.14.0.58',
'Balard-2G-1': '10.14.0.60',
'Balard-2H-1': '10.14.0.62',
'Balard-3D-1': '10.14.0.67',
'Balard-3G-1': '10.14.0.69',
'Balard-3G-2': '10.14.0.70',
'Balard-4C-1': '10.14.0.74',
'Balard-4D-1': '10.14.0.76',
'Balard-4G-1': '10.14.0.78',
'Balard-4H-1': '10.14.0.80',
'Balard-PAC-1': '10.14.0.42',
'Balard-PAC-2': '10.14.0.43'
}

def ssh_session(cisco,command,return_dict):

	# Configure and execute a SSH session with remote commands (not an option.)

	Output=""
	home= os.getenv('HOME')
	user=os.getenv('USER')
	keyfile=home+'/.ssh/cisco'
	ssh_session = netmiko.ConnectHandler(device_type='cisco_ios', ip=IPSwitchs[cisco],username=user, use_keys=True, key_file=keyfile)
	for c in command:
		Output+=(ssh_session.send_command(c))+"\n"
	ssh_session.disconnect()
	return_dict[cisco]=Output

def Treat_out(output):

	# Treating shell command ouptut since the tftp Boot informations reading

	regex_ip=r'([0-9]+\.){3}[0-9]+'
	regex_mac=r'([a-zA-Z0-9]{4}\.){2}[a-zA-Z0-9]{4}'
	regex_socket=r'Gi([0-9]+\/){2}[0-9]+'
	regex_vlan=r'\s[0-9]{3}\s'
	regex_switch=r'Balard-[0-9A-Z]+\-[0-9]+\_[0-9]+\.'

	ip=[]
	mac=[]
	socket=[]
	vlans=[]
	switch=[]
	res={}

	matches=re.finditer(regex_ip,output,re.MULTILINE)
	for matchNum, match in enumerate(matches, start=1):
		ip.append(match.group())
	matches=re.finditer(regex_mac,output,re.MULTILINE)
	for matchNum, match in enumerate(matches, start=1):
		mac.append(match.group())
	matches=re.finditer(regex_socket,output,re.MULTILINE)
	for matchNum, match in enumerate(matches, start=1):
		socket.append(match.group())
	matches=re.finditer(regex_vlan,output,re.MULTILINE)
	for matchNum, match in enumerate(matches, start=1):
		vlans.append(match.group().strip())
	matches=re.finditer(regex_switch, output, re.MULTILINE)
	for matchNum, match in enumerate(matches, start=1):
		switch.append(match.group())
	for i in range(len(ip)):
		res[ip[i]]=[mac[i],socket[i],vlans[i],switch[i][:-4]]
	return res

def Get_Description(Snoop_Dict):

	# Get the full plug name since the Snoop dictionnary.
	# Only the real connected users will be repertoried here since the snoop tftp boot repertory.

	tmp=""
	commands={}
	command=["term shell\n"]

	for k,v in Snoop_Dict.items():
		tmp=v[3]
		break

	for k,v in Snoop_Dict.items():
		if v[3] == tmp:
			command.append("show interfaces description | i "+str(v[1])+" | tail -1\n")
		else:
			commands[tmp]=command
			command=["term shell\n"]
			tmp=v[3]
			command.append("show interfaces description | i "+str(v[1])+" | tail -1\n")

	commands[tmp]=command
	output=""
	return_dict={}


	List_Dic=[]
	div=14
	List_Dic=cut_dic(IPSwitchs,div)
	manager=multiprocessing.Manager()
	return_dict=manager.dict()
	Process_List=[]
	for i in range(0,len(List_Dic)):
		cisco=list(List_Dic[i].keys())[0]
		Process_List.append(Process(target=ssh_session,args=(cisco,commands[cisco],return_dict,)))
	for i in range(0,len(List_Dic)):
		Process_List[i].start()
	for i in range(0,len(List_Dic)):
		Process_List[i].join()

	regex_socket=r"Gi([0-9]+\/){2}[0-9]+"
	regex_desc=r'[NRJPASEP]+[0-9A-Z.]+\-[0-9]+'

	socket_list=[]
	descr_list=[]
	tmp_dict={}
	Description_dictionnary={}

	for k,v in return_dict.items():
		matches=re.finditer(regex_socket, v, re.MULTILINE)
		for matchNum, match in enumerate(matches, start=1):
			socket_list.append(match.group())
		matches=re.finditer(regex_desc, v, re.MULTILINE)
		for matchNum, match in enumerate(matches, start=1):
			descr_list.append(match.group())
		for i in range(len(socket_list)):
			tmp_dict[socket_list[i]]=descr_list[i]	
		Description_dictionnary[k]=tmp_dict	
		tmp_dict={}
	return Description_dictionnary


def cut_dic(IPSwitchs,div):

	# Split Dictionnary into div differents dictionnary

	res=[]
	tmp={}
	ind=0
	size=int(round(len(IPSwitchs)/div))

	for k,v in IPSwitchs.items():
		tmp[k]=v
		ind+=1 
		if(ind==size):
			res.append(tmp)
			tmp={}
			ind=0
	if (bool(tmp)):
		res[-1].update(tmp)
	return res

def get_Dict():
	output=[]
	command=''
	Snoop_Dict={}
	Description_Dict={}

	for cisco in list(IPSwitchs.keys()):
		name=cisco[0].lower()+cisco[1:]
		command+="sed -e 's/^/"+str(cisco)+"_/' /var/lib/tftpboot/snoop/"+name+'\n'

	home= os.getenv('HOME')
	user=os.getenv('USER')
	keyfile=home+'/.ssh/known_hosts'
	output=os.popen("ssh "+str(user)+"@tftp.srv-prive.icgm.fr '"+str(command)+"'").read()
	Snoop_Dict=Treat_out(output)
	Description_Dict=Get_Description(Snoop_Dict)

	for k,v in Snoop_Dict.items():
		try:
			tmp=v 
			description=Description_Dict[v[3]][v[1]]
			Snoop_Dict[k]=[v[0],v[1],v[2],v[3],description]
		except:
			print("Error occured at : \n")
			print(k)
			print(v)
			print(Description_Dict[v[3]])
			print("Please to contact @ matthieu.cabos@umontpellier.fr\n")
	# for k,v in Snoop_Dict.items():
	# 	print(k)
	# 	print(v)
	return Snoop_Dict