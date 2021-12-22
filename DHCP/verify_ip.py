import os
from sys import *
import re

##################################################
#                                                #
#	__author__="Matthieu CABOS"                  #
#	__date__=09_09_2021                          #
#                                                #
#		IP duplicate Verification                #
#		*************************                #
#                                                #
#	In case of DHCP configuration file, this     #
#	script test the presence of cloned IP        #
#	addresses in a conf file                     #
#                                                #
##################################################

os .system('cp ../*.conf .')

# Enumerative List of differents departments of network
liste_dpt=[
'dhcpd-501.conf',
'dhcpd-510.conf',
'dhcpd-511.conf',
'dhcpd-512.conf',
'dhcpd-513.conf',
'dhcpd-514.conf',
'dhcpd-515.conf',
'dhcpd-516.conf',
'dhcpd-518.conf',
'dhcpd-524.conf',
'dhcpd-525.conf',
'dhcpd-526.conf',
'dhcpd-528.conf',
'dhcpd-530.conf',
]
# capture ip flag
ip_catch=False
# @ IP & MAC list
ip=[]
mac=[]

# courding the department list
for dpt in liste_dpt:
	content=os.popen("cat "+str(dpt)).readlines() # Getting raw content of dhcp conf files
	for item in content:
		try:
			# I verify correspondance betwween MAC@ and Fixed_IP@
			if (re.search(r'fixed-address',item)[0])!=None:        
				ip.append(item)
			if (re.search(r'hardware ethernet',item)[0])!=None:
				mac.append(item)
		except:
			pass

def verify_duplicate(liste):
	# I verify the resence of duplicate fixed IP address
	error=[]
	duplicate=(False,0)
	tmp=""
	Ip=""
	# Coursing the @ list
	for i in range(len(liste)):
		tmp=liste[i]
		for j in range(i+1,len(liste)):
			if tmp==liste[j]:  # Checking errors
				regex=r"(\d+.){3}\d+"
				matches = re.finditer(regex, liste[j], re.MULTILINE)
				for matchNum, match in enumerate(matches, start=1):
					Ip=match.group()
				error.append(Ip)
	if not (error==[]):
		return error
	else:
		return None


count=len(ip)

# Console interface for results

print("\n")
print("The current network own "+str(count)+" registered computers\n")
print("Verification of address duplication (ip) : ")
print("*******************************************")
print(verify_duplicate(ip))
print("\n")
print("Verification of address duplication (mac) : ")
print("*******************************************")
print(verify_duplicate(mac))
print("\n")
os.system('rm *.conf')