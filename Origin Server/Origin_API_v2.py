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
__date__='12/01/2022'

# Shared Variable 

# Connection_Time={}
# Connection_Time=build_dict()

################################################################################

# Tftp Server Informations Getter Section

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
	"""
		Configure and execute a SSH session with remote commands (not an option.)

		It is an automatic authentified ssh session, using the envirronment parameters as :
			* Home absolute way
			* user from environment variables
			* ssh keyfile from the given absolute way

		The results will be stored into the return dict dictionnary using the Python Multithreading functions.

		=============== =============== ========================================================
		**Parameters**    **Type**       **Description**
		**cisco**        *Str*           The name of the Cisco Switch to connect
		**command**      *Str List*      The String command list to send to the cisco switch
		**return_dict**  *Dictionnary*   The dictionnary storing commands output by Cisco name
		=============== =============== ========================================================


		:Returns:  Dictionnary : The dictionnary linking to a Cisco switch name as a key its commands list output from console.
	"""
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
	"""
		Treating shell command ouptut since the tftp Boot informations reading.

		To do so, this function is ruled by regular expression as :
			* **regex_ip**
			* **regex_mac**
			* **regex_socket**
			* **regex_vlan**
			* **regex_switch**

		This method treat a commands list output from a ssh session with a cisco switch.
		It read and treat in multiline mode every met values from regular expression and store these informations into the returned dictionnary.
		The returned dictionnary is builded with the ip as key and following informations as values :
			* MAC address
			* Cisco GigabitEthernet socket (with form Gix/y/z)
			* The Vlan identifier as Integer
			* The switch name as String

		=============== =========== =======================================================================
		**Parameters**   **Type**    **Description**
		**output**        *Str*      The raw commands list output from the ssh session with a cisco switch
		=============== =========== =======================================================================

		:Returns:  Dictionnary: The builded dictionnary linking to an ip as key the Cisco informations
	"""
	regex_ip=r'([0-9]+\.){3}[0-9]+'
	regex_mac=r'([a-zA-Z0-9]{4}\.){2}[a-zA-Z0-9]{4}'
	regex_socket=r'Gi([0-9]+\/){2}[0-9]+'
	regex_vlan=r'\s[0-9]{3}\s'
	regex_switch=r'Balard-[0-9A-Z]+\-[0-9]+'

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
		res[ip[i]]=[mac[i],socket[i],vlans[i],switch[i]]
	return res

def Get_Description(Snoop_Dict):
	"""
		Get the full plug name since the Snoop dictionnary present into the tftp server (into the *var/lib/tftpboot/snoop/* repertory).

		Only the real connected users will be repertoried here since the snoop tftp boot repertory.
		This methos has been partially coded with a parallel section to treat ssh connection faster.

		This method is following this algorithm :
			* **Building Cisco Instructions list** by Switch (stored into the *tmp* variable)
			* **Manage the multiprocessing section** of the code with the splitted Switch Dictionnary and the shared return dictionnary to store results of ssh sessions.
			* **Launching the multiprocess list** with the correct method *ssh_session* and associated builded Cisco instructions list.
			* **Start and join the differents process** and rebuild the return dictionnary sorted by Cisco Switch name
			* The results of **the multiples ssh session give us the full outlet description name** (with form N1A01-01) by regular expression filtering
			* **Build the Description_dictionnary** linking to a Cisco gigabitEthernet socket (Gix/y/z) as key its outlet exact description.

		================ =========== ========================================================
		**Parameters**    **Type**    **Description**
		Snoop_Dict		  *Dict*       The snoop dictionnary extracted from the tftp server
		================ =========== ========================================================

		:Returns:  Dictionnary : The builded dictionnary associating to a cisco gigabit ethernet socket (Gix/y/z) its exact outlet description name as String.

	"""
	tmp=""
	commands={}
	command=["term shell\n"]

	for k,v in Snoop_Dict.items():
		tmp=v[3]
		break

	# Building Cisco Instructions list by Switch (stored into the *tmp* variable)

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

	# Manage the multiprocessing section of the code with the splitted Switch Dictionnary and the shared return dictionnary to store results of ssh sessions.

	List_Dic=[]
	div=14
	List_Dic=cut_dic(IPSwitchs,div)
	manager=multiprocessing.Manager()
	return_dict=manager.dict()
	Process_List=[]

	# Launching the multiprocess list with the correct method *ssh_session* and associated builded Cisco instructions list.

	for i in range(0,len(List_Dic)):
		cisco=list(List_Dic[i].keys())[0]
		try:
			Process_List.append(Process(target=ssh_session,args=(cisco,commands[cisco],return_dict,)))
		except:
			print(str(cisco)+" is not avaible as key.")

	# Start and join the differents process and rebuild the return dictionnary sorted by Cisco Switch name

	for i in range(0,len(List_Dic)):
		try:
			Process_List[i].start()
		except:
			print(str(cisco)+" is not avaible as key.")
	for i in range(0,len(List_Dic)):
		try:
			Process_List[i].join()
		except:
			print(str(cisco)+" is not avaible as key.")

	# The results of the multiples ssh session give us the full outlet description name (with form N1A01-01) by regular expression filtering

	regex_socket=re.compile(r"Gi([0-9]+\/){2}[0-9]+")
	regex_desc=r"[NRJPASEP]+[0-9A-Z.]+\-[0-9]+"

	socket_list=[]
	descr_list=[]
	tmp_dict={}
	Description_dictionnary={}

	# Build the Description_dictionnary linking to a Cisco gigabitEthernet socket (Gix/y/z) as key its outlet exact description.

	for k,v in return_dict.items():
		for item in v.split("\n"): 
			match=regex_socket.match(item)
			match2=re.findall(regex_desc,item)
			try:
				tmp_dict[match.group()]=match2[0]
			except:
				pass
		Description_dictionnary[k]=tmp_dict	
		tmp_dict={}

	return Description_dictionnary


def cut_dic(IPSwitchs,div):
	"""
		Utilitary method to split properly and in adequation with the multiprocessing parameters the given dictionnary.

		Split Dictionnary into div differents dictionnary.

		================ ========== ============================================================================
		**Parameters**   **Type**    **Description**
		**IPSwitchs**    *Dict*      The shared dictionnary associating to a Cisco switch name its IP address.
		**div**          *Integer*   The number of slices to build from the given dictionnary
		================ ========== ============================================================================

		:Returns: List: A list of dictionnary containing the main dictionnary splitted into div differents sections.
	"""
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
	"""	
		Get the main informations dictionnary repertoring these following field:
			* **IP address as key**
			* **MAC address**
			* **Cisco Socket**
			* **Vlan Identifier**
			* **Cisco Switch name**
			* **Outlet Description**

		The five firsts informations are extracted from the tftp boot server to get exact real values from cisco switch.
		The last one is extracted from Cisco switch multiple requests.


		:Returns: Dictionnary : The Snoop dictionnary repertoring all the needed network informations.
	"""
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
			pass

	return Snoop_Dict

##########################################################

# Get Connected Users & Time Section


def reverse(line):
	"""
		Perso reverse list function

		=============== =========== ========================
		**Parameters**   **Type**     **Description**
		**line**         *Str List*   A string line as list
		=============== =========== ========================

		:returns: Str List : The reversed list
	"""
	res=[]
	for i in range(len(line)-1,0,-1):
		if (line[i]!=""):
			res.append(line[i])
	return res

def pop_double(line):
	"""
		Pop double from list and build full hostname.

		To do so, we have to follow these instructions :
			* *Read the current line and store the doubled value as host*
			* *Course te rest of list and extract the user name from it*
			* *Rebuild the exact hostname and return it*

		=============== =========== =================================
		**Parameters**   **Type**     **Description**
		**line**         *Str List*   A String line listed by words
		=============== =========== =================================

		:Returns: String : The exact hostname string with form **'name@host'**
	"""
	tmp=line[:]
	host=""
	name=""
	for item in tmp:
		if tmp.count(item)==2:
			host=item
			while item in tmp:
				tmp.remove(item)
	if len(tmp)==1:
		name=''.join(tmp)
	else:
		tmp.reverse()
		name=''.join(tmp)
	if (name!="") and (host!=""):
		return(name+'@'+host)


def Get_origin_connected():
	home= os.getenv('HOME')
	user=os.getenv('USER')
	keyfile=home+'/.ssh/known_hosts'
	ssh_session = netmiko.ConnectHandler(device_type='linux', ip='10.14.14.20',username=user, use_keys=True, key_file=keyfile)
	Output=ssh_session.send_command('/opt/Linux_FLEXnet_Server_ver_11.16.5.1/lmutil  lmstat -a -c /opt/Linux_FLEXnet_Server_ver_11.16.5.1/Licenses/Origin_20jetons.lic | grep \"^.*origin\.srv-prive\.icgm\.fr/27000.*\"').split('\n')
	ssh_session.disconnect()
	return Output


def Get_Connected(Output):
	"""
		Getting the full connected users list in the origin server since the ssh remote commands.
		The automated ssh session request the users list to the origin server Licence manager.
		Once the list stored, it is treated by regular expression to extract the hostname list.
		This funtion use the pop_double method.

		:Returns: Str List : The full connected at Origin hostname list as Strings.

	"""
	# home= os.getenv('HOME')
	# user=os.getenv('USER')
	# keyfile=home+'/.ssh/known_hosts'
	# ssh_session = netmiko.ConnectHandler(device_type='linux', ip='10.14.14.20',username=user, use_keys=True, key_file=keyfile)
	# Output=ssh_session.send_command('/opt/Linux_FLEXnet_Server_ver_11.16.5.1/lmutil  lmstat -a -c /opt/Linux_FLEXnet_Server_ver_11.16.5.1/Licenses/Origin_20jetons.lic | grep \"^.*origin\.srv-prive\.icgm\.fr/27000.*\"').split('\n')
	# ssh_session.disconnect()

	
	current=[]
	regex_hostname=re.compile('^\s*[0-9A-Za-zïëîê_\s-]+')

	# format the list with the correct form

	Output=[regex_hostname.match(line).group() for line in Output]

	# Treating and extracting hostnames from the list

	name=""
	host=""
	Host_list=[]
	for line in Output:
		current=reverse(line.split(' '))
		Host_list.append(pop_double(current))
	return Host_list


def is_connected(user,Connected_content):
	"""
		Check if the given user is in the connected list.
		The connected list is given by the Get_Connected Section method.

		======================= =========== ==============================
		**Parameters**           **Type**    **Description**
		**user**                 *Str*        The user's hostname to test
		**Connected_content**    *Str List*   The Connected Hostnames list
		======================= =========== ==============================


		:Returns: Boolean : The Boolean value return True if present False else 
	"""
	return user in Connected_content
	
def Compute_elapsed_time(Start_dict):
	Time_dict={}
	year=int(os.popen('date +%Y').read())
	month=int(os.popen('date +%m').read())
	day=int(os.popen('date +%d').read())
	hour=0
	minuts=0
	seconds=0

	regex_number=r'[0-9]+'

	for k,v in Start_dict.items():
		matches=re.finditer(regex_number, v, re.MULTILINE)
		for matchNum, match in enumerate(matches, start=1):
			if matchNum==1:
				hour=int(match.group())
			elif matchNum==2:
				minuts=int(match.group())
			else:
				pass
		date=dt.datetime(year,month,day,hour,minuts,seconds)
		Start_dict[k]=int(time.mktime(date.timetuple()))
		now=int(time.time())
		Time_dict[k]=int((now-Start_dict[k])/60)

	return Time_dict


def Get_Connexion_Time():
	Output=Get_origin_connected()  # Variable globale
	# Output="    Raptor ZBOOK-3 ZBOOK-3 (v9.4) (origin.srv-prive.icgm.fr/27000 196), start Tue 1/11 07:54\n    Student DAMP-ST1 DAMP-ST1 (v9.4) (origin.srv-prive.icgm.fr/27000 196), start Tue 1/11 06:09\n    Romain DESKTOP-V7KRJB0 DESKTOP-V7KRJB0 (v9.4) (origin.srv-prive.icgm.fr/27000 1655), start Tue 1/11 05:18\n    jerome PC-Jerome PC-Jerome (v9.4) (origin.srv-prive.icgm.fr/27000 1165), start Tue 1/11 06:35\n    Rana C2m-PC C2m-PC (v9.4) (origin.srv-prive.icgm.fr/27000 262), start Tue 1/11 07:40".split('\n')


	Output_host=Get_Connected(Output)
	regex_start_time=r'[0-9]+\:[0-9]+'

	matches=re.finditer(regex_start_time, "".join(Output), re.MULTILINE)

	Start_dict={}

	for matchNum, match in enumerate(matches, start=1):
		Start_dict[Output_host[matchNum - 1]]=match.group()

	return(Compute_elapsed_time(Start_dict))
