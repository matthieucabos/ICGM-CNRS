import os
import sys
import re
import datetime as dt
import time
import netmiko
from multiprocessing import Process
import pyexcel as p

__author__="CABOS Matthieu"
__date__=21/12/2021

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
Vlans={
501:"IDRAC",
510:"DPT1",
511:"DPT2",
512:"DPT3",
513:"DPT4",
514:"DPT5",
515:"INSTRU-ON",
516:"INSTRU-OFF",
518:"IMPRIM",
519:"GUEST",
524:"SGAF",
525:"SSI",
526:"ExpProtect",
528:"IDRAC",
529:"Did",
530:"PT"
}

# IP_list=sys.argv[1]


IP_list=[
'10.14.23.214',
'10.14.18.135'
]

def cut_dic(Cisco_Dic,div):

	# Split Dictionnary into div differents dictionnary

	res=[]
	tmp={}
	ind=0
	size=int(round(len(Cisco_Dic)/div))

	for k,v in Cisco_Dic.items():
		tmp[k]=v
		ind+=1 
		if(ind==size):
			res.append(tmp)
			tmp={}
			ind=0
	if (bool(tmp)):
		res[-1].update(tmp)
	return res

List_Dic=[]
List_Dic=cut_dic(IPSwitchs,21)

def Del_Duplicate(liste):
	verif=liste[:]
	for item in liste:
		verif.remove(item)
		if item in verif:
			liste.remove(item)
	return liste

def ssh_session(cisco,command):
	home= os.getenv('HOME')
	user=os.getenv('USER')
	keyfile=home+'/.ssh/cisco'
	ssh_session = netmiko.ConnectHandler(device_type='cisco_ios', ip=IPSwitchs[cisco],username=user, use_keys=True, key_file=keyfile)
	Output=ssh_session.send_command(command)
	ssh_session.disconnect()
	return Output

def Get_Users_Info(IP_list):

	# Building DHCP dictionnary and get infos since the given IP adresses list as parameter

	# Variable Initialisation

	tmp_dict={}
	Users=[]
	Users_dict={}
	DHCP_Dict={}
	Content=""
	tmp=""
	socket=""
	count=0	

	# Regular Expressions Definition

	regex_MAC=r'([0-9A-Fa-f]{2}\:){5}[0-9A-Fa-f]{2}'
	regex_IP=r'fixed.*'
	regex_raw_ip=r'([0-9]+\.){3}[0-9]+'
	regex_hostname=r'\"[A-Za-z0-9-_]+\"'
	regex_cisco=r'Gi([0-9]+\/){2}[0-9]+'
	regex_description=r'[NRJPASEP]+[0-9]+[A-K0-9]+-[0-9]+'

	# Building DHCP Dictionnary

	for vlan in list(Vlans.keys()):
		f=open('../dhcpd-'+str(vlan)+'.conf')
		Content=f.read().split('}')
		for item in Content:
			matches=re.finditer(regex_MAC, item, re.MULTILINE)
			for matchNum, match in enumerate(matches, start=1):
				tmp=str(match.group())
				tmp_dict['mac']=tmp[:2]+tmp[3:5]+'.'+tmp[6:8]+tmp[9:11]+'.'+tmp[12:14]+tmp[15:17]
			matches=re.finditer(regex_IP, item, re.MULTILINE)
			for matchNum, match in enumerate(matches, start=1):
				matches2=re.finditer(regex_raw_ip, match.group(), re.MULTILINE)
				for mn, mat in enumerate(matches2, start=1):
					tmp_dict['ip']=str(mat.group())
			matches=re.finditer(regex_hostname, item, re.MULTILINE)
			for matchNum, match in enumerate(matches, start=1):
				tmp_dict['hostname']=str(match.group())
			tmp_dict['departement']=Vlans[vlan]
			tmp_dict['vlan']=vlan
			if tmp_dict != {}:
				Users.append(tmp_dict)
			tmp_dict={}
		DHCP_Dict[Vlans[vlan]]=Del_Duplicate(Users)[:-1]
		Users=[]

	# Updating Users Dictionnary since the DHCP dictionnary from the ip correspondance (as key entry of the Users dictionnary)

	for k,v in DHCP_Dict.items():
		for item in v:
			for ip in IP_list:
				if item['ip']==ip:
					Users_dict[ip]=item

	# Updating the Users Dictionnary since the Cisco output command : ssh <Cisco_name> 'show mac address' to get the associated cisco switch ID and the gigabit ethernet ID

	i=0
	Process_List=[]
	for cisco in list(IPSwitchs.keys()):
		i+=1
		try:
			# HERE !!!
			Content=ssh_session(cisco,'sh mac address')
		except:
			print(cisco+' is not avaible at the moment')

		User_liste=list(Users_dict.keys())
		ContList=Content.split('\n')
		for user in Users_dict.keys():
			for line in ContList:
				if Users_dict[user]['mac'] in line:
					Users_dict[user]['cisco']=cisco
					matches=re.finditer(regex_cisco, line, re.MULTILINE)
					for matchNum, match in enumerate(matches, start=1):
						socket=match.group()
					if socket!="":
						Users_dict[user]['socket']=socket[2:]
						count+=1
						socket=""
		if count>=len(Users_dict.keys()):
			break

	file_name='../Switchs.ods'
	records = p.get_array(file_name=file_name)
	socket=""
	for user in Users_dict.keys():
		try:
			for record in records:
				cisco=record[4]
				socket=str(record[5])+"/0/"+str(record[8])
				Description=record[2]
				if Users_dict[user]['cisco']==cisco and Users_dict[user]['socket']==socket :
					Users_dict[user]['Description']=Description		
		except:
			print(str(Users_dict[user]['hostname'])+" is not listed on the network")
	return Users_dict

def Write_in_file(to_write,path):

	# Write Infos in file

	f=open(path,'a')
	for k,v in to_write.items():
		f.write(str(k))
		f.write(str(v))
		f.write('\n')
	f.close()

def get_Connected():

	# Get connected user list since the orgin token licence

	home= os.getenv('HOME')
	user=os.getenv('USER')
	keyfile=home+'/.ssh/known_hosts'
	ssh_origin = netmiko.ConnectHandler(device_type='linux', ip='10.14.14.20',username=user, use_keys=True, key_file=keyfile)
	Connected=ssh_origin.send_command('/opt/Linux_FLEXnet_Server_ver_11.16.5.1/lmutil  lmstat -a -c /opt/Linux_FLEXnet_Server_ver_11.16.5.1/Licenses/Origin_20jetons.lic | grep "^.*origin\.srv-prive\.icgm\.fr/27000.*"').split('\n')
	ssh_origin.disconnect()

	regex_cnctd=r'[A-Za-z0-9]+\-[A-Za-z0-9]+'
	for i in range(0,len(Connected)):
		matches=re.finditer(regex_cnctd, Connected[i], re.MULTILINE)
		for matchNum, match in enumerate(matches, start=1):
			Connected[i]=match.group()
			break
	return(Connected)

def Get_Ip_list2():
	res={}
	regex_user=r'.*\:'
	regex_ip=r'([0-9]+\.){3}[0-9]+'
	user=""
	ip=""

	Content=os.popen("./Treat_log_v2.sh").readlines()
	for line in Content:
		matches=re.finditer(regex_user, line, re.MULTILINE)
		for matchNum, match in enumerate(matches, start=1):
			user=match.group()
		matches=re.finditer(regex_ip, line, re.MULTILINE)
		for matchNum, match in enumerate(matches, start=1):
			ip=match.group()
		res[ip]=user[:-1]
	return res

def time_to_timestamp(str_time):

	# Get timestamp from the given string date

	# Regular Expressions definition

	regex_time=r'[0-9]+'
	regex_month=r'[a-zéè]+'

	# Variable definition

	year=0
	month=0
	day=0
	hour=int(str_time[0:2])
	minuts=int(str_time[3:5])

	# Getting integer fields since conversion

	day=int(os.popen('date +%d').read())
	month=int(os.popen('date +%m').read())
	year=int(os.popen('date +%Y').read())
	date=dt.datetime(year,month,day,hour,minuts)
	timestamp=time.mktime(date.timetuple())

	# Return the equivalent timestamp (in seconds since epoch)

	return(timestamp)

def Get_time(Ip_list):

	# Building Time dictionnary associating a pseudo to a start time

	# Variable Definitions

	Time_dict={}
	Done=['(@orglab-SLOG@']
	time=""
	Start_flag=False
	date=os.popen('date').read()

	# Regular Expressions definition

	regex_time=r'([0-9]+\:){2}[0-9]+'
	regex_name=r'[^\s]*\@[A-Za-z-0-9_-]*'

	f=open("logwatch",'r')
	Records=f.readlines()
	for record in Records:
		if date[:13] in record :
			Start_flag=True
		if Start_flag :
			matches=re.finditer(regex_time, record, re.MULTILINE)
			for matchNum, match in enumerate(matches, start=1):
				if match.group() != "":
					time=match.group()
			matches=re.finditer(regex_name, record, re.MULTILINE)
			for matchNum, match in enumerate(matches, start=1):
				if match.group() != "" and not (match.group() in Done):
					Time_dict[match.group()]=time_to_timestamp(time) 
					time=""
					Done.append(match.group())
	return Time_dict

def get_host(origin_name):
	host=""
	regex_host=r'@.*'
	matches=re.finditer(regex_host, origin_name, re.MULTILINE)
	for matchNum, match in enumerate(matches, start=1):
		return match.group()

# Main Users Informations Finder Algorithm

host=""

# Building and associating Dictionnaries

IP_list=Get_Ip_list2()
Time_dict=Get_time(IP_list)
Users_dict=Get_Users_Info(list(IP_list.keys()))
Connected=get_Connected()

for k,v in Users_dict.items():
	if v['ip'] in list(IP_list.keys()):
		position=list(IP_list.keys()).index(v['ip'])
		Users_dict[k]['origin_name']=list(IP_list.values())[position]
		host=get_host(Users_dict[k]['origin_name'])
	
	for l,m in Time_dict.items():
		if l==v['origin_name'] and (host[1:] in Connected):
			Users_dict[k]['connexion time']=str((float(time.time())-m)/60)+" min"
			break
		elif l==v['origin_name'] :
			Users_dict[k]['connexion time']='Connection closed, started at '+str(os.popen('date -d @'+str(m)).read()[:22])
			break
		else:
			pass
	print(v)

# Writing History File

user=os.getenv('USER')
try:
	os.system('scp '+str(user)+'@origin.srv-prive.icgm.fr:/home/mcabos/Origin_history .')
except:
	pass
Write_in_file(Users_dict,'./Origin_history')
os.system('scp ./Origin_history '+str(user)+'@origin.srv-prive.icgm.fr:/home/mcabos/')