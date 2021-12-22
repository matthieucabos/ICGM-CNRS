import os
import sys
import re
import datetime as dt
import time
import netmiko
from multiprocessing import Process

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

Time_dict={}
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
	regex_description=r'[NRJPASEP]+[0-9]+[A-K][0-9]+-[0-9]+'

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
		# //
		# print(IPSwitchs[cisco])
		# print(List_Dic[i])
		i+=1
		try:
			# HERE !!!
			Content=ssh_session(cisco,'sh mac address')

		except:
			print(cisco+' is not avaible at the moment')

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

	Content=""
	for k,v in Users_dict.items():
		# //
		try:
			# HERE !!!
			home= os.getenv('HOME')
			Content=ssh_session(v['cisco'],'sh int gigabitethernet '+v['socket'])
		except:
			print('Informations missing about user'+str(v))

		matches=re.finditer(regex_description, Content, re.MULTILINE)
		for matchNum, match in enumerate(matches, start=1):
			Users_dict[k]['Description']=match.group()
	return Users_dict

def Cut_log():

	# Cut logfile since the date (today as default)

	try:
		os.system('scp mcabos@origin.srv-prive.icgm.fr:~/logwatch .')
	except:
		pass

	f=open('./logwatch','r')
	date=os.popen('date').read()
	Content=f.readlines()
	Keep_flag=False
	to_write=[]

	for line in Content:
		if(date[:13] in line) and not Keep_flag:
			Keep_flag=True
		if Keep_flag:
			to_write.append(line)
	f.close()
	f=open('./logwatch','w')
	for line in to_write:
		f.write(line)
	f.close()

def time_to_timestamp(str_time):

	# Get timestamp from the given string date

	# Regular Expressions definition

	regex_time=r'[0-9]+'
	regex_month=r'[a-zéè]+'

	# Variable definition

	year=0
	month=0
	day=0
	hour=0
	minuts=0

	# Getting integer fields since conversion

	matches=re.finditer(regex_time,str_time,re.MULTILINE)
	for matchNum, match in enumerate(matches, start=1):
		if matchNum == 1:
			day=int(match.group())
		elif matchNum == 2 :
			hour=int(match.group())
		elif matchNum == 3 :
			minuts=int(match.group())
		elif matchNum == 5 :
			year=int(match.group())
	matches=re.finditer(regex_month, str_time, re.MULTILINE)
	month=int(os.popen('date +%m').read())
	date=dt.datetime(2021,month,day,hour,minuts)
	timestamp=time.mktime(date.timetuple())

	# Return the equivalent timestamp (in seconds since epoch)

	return(timestamp)

def Read_and_treat_log(path):

	# Read and extract informations from the logwatch file

	# Regular Expression Definition

	regex_date=r'[a-z]+([^a-z]+.*[0-9]*\n)+'
	regex_ip=r'([0-9]+\.)+[0-9]+'
	regex_name=r'\"OriginPro\".*'
	regex_pc=r'\@.*'
	regex_time=r'^[a-z].*'

	# Variables Definition

	banned=['10.14.14.20']
	name=""
	ip_set=set()
	find_ip_dict={}
	name_ip_dict={}
	time_dict={}
	tmp_dict={}
	diff={}
	count=0
	tmp={}

	# Open and read the logwatch file

	Cut_log()
	f=open('./logwatch')
	Content=f.read()
	match_list=[]

	# 1/ Getting IP list associated to a timed & named token. The resultys are stored by time order, arbitrary indexed from 1 -> n

	matches=re.finditer(regex_date, Content, re.MULTILINE)
	for matchNum, match in enumerate(matches, start=1):
		match_list.append(match.group())
	for item in match_list:
		matches=re.finditer(regex_ip, item, re.MULTILINE)
		for matchNum, match in enumerate(matches, start=1):
			if not match.group() in banned:
				ip_set.add(match.group())
		matches=re.finditer(regex_name, item, re.MULTILINE)
		for matchNum, match in enumerate(matches, start=1):
			name=match.group()[12:]
		tmp_dict[name]=ip_set.copy()
		if name != "" and len(ip_set)!=0:
			find_ip_dict[str(count)]=tmp_dict.copy()
			matches=re.finditer(regex_time, item, re.MULTILINE)
			for matchNum, match in enumerate(matches,start=1):
				time_dict[str(count)]=time_to_timestamp(match.group())
		tmp_dict.clear()
		ip_set.clear()
		name=""
		count+=1

	# 2/ Getting host ID from the full Origin user name (with form name@host) => Allow multiple users sessions on the same host

	TEMP='@'
	for k,v in find_ip_dict.items():
		if list(find_ip_dict[k].keys())[0] != TEMP:
			Time_dict[list(find_ip_dict[k].keys())[0]]=time_dict[k]
		TEMP=list(find_ip_dict[k].keys())[0]
		matches=re.finditer(regex_pc, list(v.keys())[0], re.MULTILINE)
		for matchNum, match in enumerate(matches, start=1):
			host=match.group()
		if len(name_ip_dict)==0:
			name_ip_dict[host]=list(v.values())[0].pop()
		else:

			# 3/ Compute the Cantor difference between two adjacents set (indexed +- 1) to get the User's associated IP

			diff=(list(v.values())[0])-tmp
			if len(diff)!=0:
				name_ip_dict[host]=diff.pop()
		tmp=list(v.values())[0].copy()
	return name_ip_dict

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

# Main Users Informations Finder Algorithm

name_ip_dict={}
name_ip_dict=Read_and_treat_log('./logwatch')
IP_list=list(name_ip_dict.values())
Users_dict=Get_Users_Info(IP_list)
Connected=get_Connected()

for k,v in Users_dict.items():
	if v['ip'] in list(name_ip_dict.values()):
		position=list(name_ip_dict.values()).index(v['ip'])
		Users_dict[k]['origin_name']=list(name_ip_dict.keys())[position]
	for l,m in Time_dict.items():
		try:		
			if (v['origin_name'][1:] in l) and (v['origin_name'][1:].strip() in Connected):
				Users_dict[k]['connexion time']=str(float(time.time())-m)
				break
			else:
				Users_dict[k]['connexion time']='not avaible, start at '+str(m)
		except:
			print('Error occured, user is not present into log archive.')
			break
	print(k)
	print(v)

user=os.getenv('USER')
try:
	os.system('scp '+str(user)+'@origin.srv-prive.icgm.fr:/home/mcabos/Origin_history .')
except:
	pass
Write_in_file(Users_dict,'./Origin_history')
os.system('scp ./Origin_history '+str(user)+'@origin.srv-prive.icgm.fr:/home/mcabos/')