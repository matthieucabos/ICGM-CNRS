import os
import sys
import rrdtool

__author__="Matthieu CABOS"
__date__="01/10/2021"

def cumulate_res(liste):
	res=0
	for i in range(len(liste)):
		res+=int(liste[i])
	return res

def get_list(string):
	res=[]
	rez=[]
	tmp=""
	for item in string.read():
		res.append(item)

	for item in res:
		if item != '\n':
			tmp+=item
		else:
			rez.append(int(tmp))
			tmp=""
	return rez

def get_max(liste):
	tmp=(0,0)
	for item in liste:
		if item > tmp[0] and item > tmp[1]:
			if tmp[0] > tmp[1]:
				tmp=(tmp[0],item)
			else:
				tmp=(item,tmp[1])
	return tmp

ip=sys.argv[1]
ID_node=(0,0)

if ( not os.path.isfile("traffic.rrd")):
	os.system("rrdtool create traffic.rrd --step 1 DS:RX:COUNTER:60:U:U DS:Error:COUNTER:60:U:U DS:10G_NODE:COUNTER:60:U:U RRA:AVERAGE:0.5:1:60")
	os.system("chmod 777 *")

transfered_octet=os.popen("snmpwalk -v 1 -c comaccess "+str(ip)+":161 1.3.6.1.2.1.2.2.1.16 | cut -d ' ' -f4")
error_counter=os.popen("snmpwalk -v 1 -c comaccess "+str(ip)+":161 1.3.6.1.2.1.2.2.1.14 | cut -d ' ' -f4")
transfered_octet_list=get_list(transfered_octet)
Tr_Oct=int(cumulate_res(transfered_octet_list)/1000)-(Max_O[0]+Max_O[1])/1000
Err_Cnt=cumulate_res(get_list(error_counter))
value="N:"+str(int(Tr_Oct))+":"+str(int(Err_Cnt))+":"+str(int((Max_O[0]+Max_O[1])/1000))
os.system("rrdupdate traffic.rrd -t RX:Error:10G_NODE "+value)
