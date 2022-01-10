import os
import time
import re

__author__="CABOS Matthieu"
__date__=22/12/2021

def Init_dict(Hostname,flag):

	# Intialisation of Dictionnaries with default values

	res={}
	for i in range(len(Hostname)):
		if not flag:
			res[Hostname[i]]=999999999999
		else:
			res[Hostname[i]]=0
	return res 

def get_max(liste):
	maxi=0
	for item in liste:
		if item> maxi:
			maxi=item 
	return maxi  

def get_min(liste):
	mini=99999999999999
	for item in liste:
		if item< mini:
			mini=item 
	return mini  

def is_connected(user,Connected_content):
	for item in Connected_content:
		if (item in user):
			return True 
		else:
			return False

def build_dict():

	time_dict_in={}
	time_dict_out={}

	# I first read the results of the Treat_tokens.sh script

	IN_Hostname=os.popen('./Treat_tokens.sh 3').readlines()
	OUT_Hostname=os.popen('./Treat_tokens.sh 4').readlines()
	IN_TIME=os.popen('./Treat_tokens.sh 5').readlines()
	OUT_TIME=os.popen('./Treat_tokens.sh 6').readlines()

	# Sort and Store them into lists

	IN_Hostname=[item.replace('\n','') for item in IN_Hostname]
	OUT_Hostname=[item.replace('\n','') for item in OUT_Hostname]
	IN_TIME=[item.replace('\n','') for item in IN_TIME]
	OUT_TIME=[item.replace('\n','') for item in OUT_TIME]

	Host_list=IN_Hostname[:]
	Host_list.extend(OUT_Hostname)

	Token_list=IN_TIME[:]
	Token_list.extend(OUT_TIME)
	Token_dict={}
	times=[]
	Done=[]
	current=Host_list[0]

	for i in range(len(Host_list)):
		print(current)
		print(Host_list[i])
		print(Token_list[i])
		if current==Host_list[i]:
			print("HERE")
			times.append(int(Token_list[i]))
		else:
			print("NOT HERE")
			if not (current in Done) and (current != '@orglab-SLOG@)'):
				Token_dict[current]=times
				Done.append(current)
			else:
				if (current != '@orglab-SLOG@)'):
					Token_dict[current].extend(times)
			current=Host_list[i]
			times=[int(Token_list[i])]
		print("________________________________________")

	try:
		Token_dict[current].extend(times)
	except:
		Token_dict[current]=(times)
	res={}

	Connected_content=os.popen('ssh mcabos@origin.srv-prive.icgm.fr \'/opt/Linux_FLEXnet_Server_ver_11.16.5.1/lmutil  lmstat -a -c /opt/Linux_FLEXnet_Server_ver_11.16.5.1/Licenses/Origin_20jetons.lic | grep "^.*origin\.srv-prive\.icgm\.fr/27000.*" | cut -d " " -f6\'').readlines()
	Connected_content=[ item.replace("\n","") for item in Connected_content]

	for k,v in Token_dict.items():
		if is_connected(k,Connected_content):
			now=int(time.time())
			res[k]=round(abs(get_min(v)-now)/60)
		else:
			res[k]=round(abs(get_max(v)-get_min(v))/60)

	return res

build_dict()
Connection_Time=build_dict()
print(Connection_Time)