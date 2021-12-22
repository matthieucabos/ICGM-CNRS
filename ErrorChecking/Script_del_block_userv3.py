import os
import sys
import re
import netmiko
# from multiprocessing import Pool
from multiprocessing import Process
import time as t

__author__="CABOS Matthieu"
__date__=25/11/2021

Cisco_Dic={
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

def timeit(func):

	# Time a function using @timeit syntax.

	def do(*arg,**kwarg):
		i=0
		start=t.time()
		for i in range(0,10):
			func(*arg,**kwarg)
		now=t.time()-start
		print(str(func.__name__)+" executed 10 times in "+str(now)+" = "+str(now/10000)+" s/exec.")
		return(func(*arg,**kwarg))
	return do

# @timeit
def Treat(Cisco_Dic):

	#Buildig Error dictionnary

	IPSwitchs=Cisco_Dic
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

	# Brownsing Cisco list and write & apply associated shell script

	output=""
	f=open('Error_liste.txt','a')
	for Cisco in Gb_dict.keys():
		if not Gb_dict[Cisco]==[]:
			home= os.getenv('HOME')
			user=os.getenv('USER')
			keyfile=home+'/.ssh/cisco'
			ssh_session = netmiko.ConnectHandler(device_type='cisco_ios', ip=IPSwitchs[Cisco],
		                                         username=user, use_keys=True, key_file=keyfile)
			for item in Gb_dict[Cisco]:
				Description=''
				if item != None:
					command=['interface GigabitEthernet'+str(item),'shutdown','no shutdown']
					output = ssh_session.send_command("sh int description | i "+str(item))
					output=output.split("\n")
					regex=re.escape(item) +r'\b.*'
					regex2=r'[NR].*-[0-9]+'
					for out in output:
						matches= re.finditer(regex, out, re.MULTILINE)
						for matchNum, match in enumerate(matches, start=1):
							if (item in match.group()):
								matches2=re.finditer(regex2, str(match.group()), re.MULTILINE)
								for matchNum2, match2 in enumerate(matches2, start=1):
									Description=str(match2.group())
					Cisco_name=Cisco
					Socket_name=item
					f.write(str(Cisco_name)+" GigabitEthernet"+''.join(Socket_name)+" | Socket Description : "+str(Description)+"\n")
					ssh_session.send_config_set(command)
			ssh_session.disconnect()
	f.close()

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
div=int(sys.argv[1])
List_Dic=cut_dic(Cisco_Dic,div)

# Generating automatic Process to treat each Splitted dictionnary independantly from each others

Process_List=[]
for i in range(0,len(List_Dic)):
	Process_List.append(Process(target=Treat,args=(List_Dic[i],)))
for i in range(0,len(List_Dic)):
	Process_List[i].start()
for i in range(0,len(List_Dic)):
	Process_List[i].join()
quit()