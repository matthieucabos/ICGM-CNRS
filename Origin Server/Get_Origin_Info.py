import os
import sys
import re
from Get_tftp_infos import *
from Get_Connexion_Time import *

user=os.getenv('USER')
os.system('scp '+str(user)+'@origin.srv-prive.icgm.fr:~/logwatch .')
Users=os.popen('./Treat_log_v2.sh').read()

regex_user=r'.*\:'
regex_ip=r'([0-9]+\.){3}[0-9]+'

user_list=[]
ip_list=[]
user_ip_dict={}

matches=re.finditer(regex_user, Users, re.MULTILINE)
for matchNum, match in enumerate(matches,start=1):
	user_list.append(match.group())
matches=re.finditer(regex_ip, Users, re.MULTILINE)
for matchNum, match in enumerate(matches,start=1):
	ip_list.append(match.group())
for i in range(len(user_list)):
	user_ip_dict[ip_list[i]]=user_list[i]
Snoop_Dict=get_Dict()
for k,v in user_ip_dict.items():
	print(k)
	print(v)
	print(Snoop_Dict[k])

Connection_Time=Get_Connection_Time()
print(Connection_Time)