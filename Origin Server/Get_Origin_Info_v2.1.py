import os
import sys
import re
from Origin_API import *

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

to_write=[]
Sheet=[['adresse ip','hostname','adresse mac','Socket','Vlan','Switch','Description','Connexion Time']]  # Rajouter le start time, la date et l'heure ?
Connection_Time=build_dict()

# Connected_content=os.popen('ssh mcabos@origin.srv-prive.icgm.fr \'/opt/Linux_FLEXnet_Server_ver_11.16.5.1/lmutil  lmstat -a -c /opt/Linux_FLEXnet_Server_ver_11.16.5.1/Licenses/Origin_20jetons.lic | grep "^.*origin\.srv-prive\.icgm\.fr/27000.*" | cut -d " " -f6\'').readlines()
# Connected_content=[ item.replace("\n","") for item in Connected_content]


for k,v in user_ip_dict.items():
	hostname=v[:-1]
	if is_connected(hostname,Connected_content):   # Récupérer uniquement les utilisateurs connéctés
		to_write.append(k)
		to_write.append(hostname)
		to_write.extend(Snoop_Dict[k])
		try:
			to_write.append(str(Connection_Time[hostname])+' min')
		except:
			print("Connection time not avaible for user "+str(hostname))
	Sheet.append(to_write)
	to_write=[]

print(Sheet)

f=open('Origin_history','a')
for item in Sheet:
	f.write(" | ".join(item))
	f.write("\n")
f.close()
os.system('scp ./Origin_history '+str(user)+'@origin.srv-prive.icgm.fr:~')