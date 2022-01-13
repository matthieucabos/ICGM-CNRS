import os
import sys
import re
import netmiko
import pyexcel as p
import datetime as d
import time
import itertools as it

__author__="CABOS Matthieu"
__date__=29/11/2021

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

def get_Port(output):
	"""
		Getting port number since the regular expressions using the output stdout from the ssh remote command output
	
		=============== ========== ======================================================
		**Parameters**   **Type**   **Description**
		**output**       *String*   The ssh remote command output specified as parameter
		=============== ========== ======================================================

		Returns
		-------
		Integer

		The port number used by the origin server.
	"""
	port=0
	regex=r'[0-9]*'
	maxi=0
	matches = re.finditer(regex, output, re.MULTILINE)
	for matchNum, match in enumerate(matches, start=1):
		try:
			port=int(match.group())
		except:
			pass
		if port > maxi:
			maxi=port 
	return maxi

def get_IP_list(IP):
	"""
		Getting IP list since the regular expressions using the output stdout from the ssh remote command output
		The filtering operation is done in multiline mode and will be coursed match by match.
		The result is shown as a list of ip address.

		=============== ========== =======================================================
		**Parameters**   **Type**   **Description**
		**IP**           *String*   The ssh remote command output specified as parameter
		=============== ========== =======================================================

		Returns
		-------
		String List
		The list containing all the ipaddress founded in the ssh remote command output.

	"""
	banned=['127.0.0.1','10.14.14.20','10.14.14.9']
	res=[]
	tmp=[]
	regex=r"([0-9]*\.){3}[0-9]+"
	matches = re.finditer(regex, IP, re.MULTILINE)
	for matchNum, match in enumerate(matches, start=1):
		tmp.append(match.group())
	for item in tmp:
		if not item in banned:
			res.append(item)
	return list(dict.fromkeys(res))

def get_Host_list(Host):
	"""
		Getting Host list since the regular expressions using the output stdout from the ssh remote command output.
		Brownsing the string output line by line and filter each line independantly from the others to get the correct hostnames contained.
		The hostnames have form *name.dsi0.icgm.fr:60213*, this is the form present into the output of a **ss -n -t -r** command. 

		The result is the sorted list of the hostnames. To sort them, I use the **list(dict.fromkeys(liste))** command

		=============== =========== ======================================================
		**Parameters**   **Type**    **Description**
		**Host**         *String*    The ssh remote command output specified as parameter
		=============== =========== ======================================================

		Returns
		-------
		String List
		A list containing all the hostnames founded into the ssh remote command output.
	"""
	regex=r'[A-Z-]+\.[dsi0-9]+\.icgm.fr:[0-9]*'
	Host_real=""
	Host_list=Host.split('\n')

	for item in Host_list:
		matches=re.finditer(regex,item,re.MULTILINE)
		for matchNum, match in enumerate(matches,start=1):
			Host_real+=str(match.group())+'\n'
	res=[]
	regex=r'^[a-zA-Z0-9_-]*'
	matches = re.finditer(regex, Host_real, re.MULTILINE)
	for matchNum, match in enumerate(matches, start=1):
		if (match.group()!=''):
			res.append(match.group())
	return list(dict.fromkeys(res))

def Read_ods(path,Host_list,IP_list):
	"""
		Reading the Ordinateurs.ods file to get associated MAC_@ & Departement ID.
		The Ordinateurs.ods file contain all the authorized host into the DHCP server (and so the MAC address and the Departement ID).

		================ =============== ===================================================================
		**Parameters**    **Type**        **Description**
		**path**          *String*        Define the path of the .ods file to read 
		**Host_list**     *String List*   The given Hostname list to find values into the ods file content
		**IP_list**       *String List*   The given IP list to link the differents informations together
		================ =============== ===================================================================

		Returns
		-------
		String List
		The List repertoring the following informations as item :

			* Hostname
			* MAC address
			* Departemet ID
			* IP address
	"""
	records = p.get_array(file_name=path)
	ind=0
	res=[]
	mac=''
	for record in records:
		if record[0] in Host_list:
			ind=Host_list.index(record[0])
			mac=record[1][:2]+record[1][3:5]+'.'+record[1][6:8]+record[1][9:11]+'.'+record[1][12:14]+record[1][15:17]
			res.append([record[0],mac,record[2],IP_list[ind]])
			mac=''
			ind=0
	return res

def ssh_session_Treat_info(cisco,IPSwitchs):
	"""
		Automated authentified ssh session with parameters.
		The associated remote command is **sh mac address-table** to automate the Cisco request y ssh.

		=============== =============== ================================================================
		**Parameters**   **Type**        **Description**
		**cisco**        *String*        The Cisco Switch name to connect
		**IPSwitchs**    *Dictionnary*   The dictionnary associating to each Switch name its IP address
		=============== =============== ================================================================

		Returns
		-------
		String
		The raw output of the ssh remote command
	"""
	home= os.getenv('HOME')
	user=os.getenv('USER')
	keyfile=home+'/.ssh/cisco'
	ssh_session = netmiko.ConnectHandler(device_type='cisco_ios', ip=IPSwitchs[cisco],username=user, use_keys=True, key_file=keyfile)
	output=ssh_session.send_command('sh mac address-table')
	ssh_session.disconnect()
	return output

def Treat_Info(Infos,IPSwitchs):
	"""
		Treat Infos getted since the ods file and the ssh output both. Etablishing a link between the MAC_@ and the Cisco Socket Number.
		The result will be stored in a 'ready to print' list.
		This function is ruled by a looped algorithm :

		**for each cisco in the network** :

			* **request the associated cisco**
			* **get the Cisco gigabitethernet socket** from the **sh mac address-table** output : 

				* *Filter by the following regular expression* : **Gi([0-9]\/){2}[0-9]+**

			* **Store the informations** with form : *'Cisco : | Vlan / Mac_@ / GiB : | Host : | Dpt : | IP_@ '*
		
		=============== ================ =================================================================	
		**Parameters**    **Type**        **Description**
		**Infos**         *String list*   A list containing all the needed informations linked to an user
		**IPSwitchs**     *Dictionnary*   The dictionnary associating to each Switch name its IP address
		=============== ================ =================================================================

		Returns
		-------
		String List
		'Ready to print' String list where each item is associated with a user and have form : *'Cisco : | Vlan / Mac_@ / GiB : | Host : | Dpt : | IP_@ '*
	"""
	res=[]
	for cisco in IPSwitchs.keys():
		out=[]
		home= os.getenv('HOME')
		user=os.getenv('USER')
		keyfile=home+'/.ssh/cisco'
		ssh_session = netmiko.ConnectHandler(device_type='cisco_ios', ip=IPSwitchs[cisco],username=user, use_keys=True, key_file=keyfile)
		output=ssh_session.send_command('sh mac address-table')
		ssh_session.disconnect()
		# output=ssh_session_Treat_info(cisco,IPSwitchs)
		out=output.split('\n')
		regex=r'Gi([0-9]\/){2}[0-9]+'
		for info in Infos:
			for line in out:
				if info[1] in line:
					matches=re.finditer(regex, line , re.MULTILINE)
					for matchNum, match in enumerate(matches, start=1):
						if match.group() != None :
							res.append('Cisco : '+str(cisco)+' | Vlan / Mac_@ / GiB : '+str(line[:22])+str(line[36:])+' | Host : '+str(info[0])+' | Dpt :  '+str(info[2])+' | Ip_@ : '+str(info[3]))		
					if(len(res)==len(Infos)):
						return res
	return(res)

def Write_in_file(to_write,path):
	"""
		Write/Update Infos in file from the path name.
		The Infos parameter must be with type Sorted String List as defined in the Treat_Info method.

		=============== ================ ===============================================================
		**Parameters**    **Type**        **Description**
		**to_write**      *String List*   The full content to write as defined in the treat_Info method
		**path**          *String*        The raw path of the fle to write/update
		=============== ================ ===============================================================
	"""
	f=open(path,'a')
	for item in to_write:
		f.write(item)
		f.write('\n')
	f.close()

def get_Description(Data):
	"""
		Updating Socket Description field and add a timestamp to the Information.
		To do so, I'm uing the following regular expressions :

			* *Cisco socket getter* : **Gi([0-9]\/){2}[0-9]+**
			* *Outlet Description getter* : **[NRJPASEP]+[0-9]+[A-K][0-9]+-[0-9]+**
			* *Cisco Name getter* : **Balard-[EPACRDGH1234]+-[0-9]**

		Foreach dataline in the Data list:

			* Filter the two needed fields and store them in their respective variable cisco and socket 
			* use a ssn session to get the output of the command **show interface gigabitethernet**
			* Filter the output with the Outlet Description getter expression
			* Add the Description field to the dataline
			* Rebuild a full Data list as result

		=============== =============== ==============================================================================
		**Parameters**   **Type**       **Desccription**
		**Data**         *String List*  The String Datas as list, each dataline contain the following informations :

											* Cisco Name
											* Vlan id
											* MAC address
											* Cisco Socket
											* Hostname
											* Departemet id
											* IP address
		=============== =============== ==============================================================================

		Returns
		-------
		String List
		The updated Data list with description field

	"""
	regex=r'Gi([0-9]\/){2}[0-9]+'
	regex2=r'[NRJPASEP]+[0-9]+[A-K][0-9]+-[0-9]+'
	regex3=r'Balard-[EPACRDGH1234]+-[0-9]'
	socket=""
	description=""
	res=[]
	tmp=""

	home= os.getenv('HOME')
	user=os.getenv('USER')
	keyfile=home+'/.ssh/cisco'
	for item in Data:
		matches=re.finditer(regex3,item,re.MULTILINE)
		for matchNum, match in enumerate(matches, start=1):
			cisco=str(match.group())
		matches=re.finditer(regex,item, re.MULTILINE)
		for matchNum, match in enumerate(matches, start=1):
			socket=str(match.group())
		ssh_session = netmiko.ConnectHandler(device_type='cisco_ios', ip=IPSwitchs[cisco],username=user, use_keys=True, key_file=keyfile)
		output=ssh_session.send_command('show interface gigabitethernet '+str(socket[2:]))
		ssh_session.disconnect()
		matches=re.finditer(regex2, output, re.MULTILINE)
		for matchNum, match in enumerate(matches, start=1):
			description=str(match.group())
		tmp=item+' | Socket Description : '+description+''
		res.append(tmp)
		cisco=""
		socket=""
		description=""
		tmp=""
	return res

def reverse(liste):
	"""
		Standard list reverse function

		=============== =========== ====================
		**Parameters**   **Type**   **Description**
		**liste**        List       The list to reverse
		=============== =========== ====================

		Returns
		-------
		List
		The reversed list
	"""
	res=[]
	for i in range(len(liste)-1,-1,-1):
		res.append(liste[i])
	return res

def get_time(Data,User_rep,User_list):
	"""
		Getting exact time duration since already recorded timestamp and add it to the Main Data List.
		This method is ruled by the followings steps:

			* foreach dataline in Datas :

				* Get the IP address since regular expression filtering
				* Get the name and check if present in the User_list
				* If present, associate a timestamp 
				* If the timestamp is defined, compute the difference between the now timestamp and the starting timestamp to get the Connexion time elapsed
				* Update the Data list with the Time Elapsed field

		================ ================ ===================================================================================================
		**Parameters**     **Type**        **Description**
		**Data**           *String List*   The String Datas as list, each dataline contain the following informations :

											* Cisco Name
											* Vlan id
											* MAC address
											* Cisco Socket
											* Hostname
											* Departemet id
											* IP address
											* Socket Description
		**User_rep**       *Dictionnary*   The users dictionnary extracted from the logwatch file linking to an user his strating timestamp
		**User_list**      *Dictionnary*   The User dictionnary  extracted from the logwatch file linking to an user his IP address
		================ ================ ===================================================================================================

		Returns
		-------
		String List
		The updated Data list with field Time Elapsed
	"""
	res=[]
	tmp=""
	tmp_name=''
	timestamp=0.0
	regex=r'([0-9]+\.){3}[0-9]+'
	now=float(time.time())

	for item in Data:
		tmp_name=''
		matches=re.finditer(regex, item, re.MULTILINE)
		for matchNum, match in enumerate(matches, start=1):
			ip=str(match.group())
		if(ip in list(User_rep.values())):
			tmp_name=str(list(User_rep.keys())[list(User_rep.values()).index(ip)])
			for name in list(User_list.keys()):
				if tmp_name in  name:
					timestamp=User_list[name]
					break
				else:
					timestamp=0.0
			print(timestamp)
			print(now)
			print(now-timestamp)
			if (timestamp != 0.0):
				tmp=item+' | pseudo = '+str(list(User_rep.keys())[list(User_rep.values()).index(ip)])+' | Time Elapsed = '+str((now-timestamp)/60)+' min'
				timestamp=0.0
			else:
				tmp=item+' | pseudo = '+str(list(User_rep.keys())[list(User_rep.values()).index(ip)])+' | Time Elapsed not avaible'
		else:
			tmp=item
		res.append(tmp)
		tmp=''
	
	return reverse(res)

def treat_Users(Users):
	"""
		Managing Tokens allocation (Time Elapsed since the first Token).
		This method read the content of the requested Licence file.

		Differents regular expressions manage the results :

			* *month* : **[0-9]+\/+**
			* *day* : **[^a-z]\/[0-9]+**
			* *hour* : **[0-9]+\:**
			* *minuts* : **\:[0-9]+**
			* *user* : **^\s*[^:\s]+**
			* *PC* : **[A-Z0-9]+-[A-Z0-9]+**

		Once the differents fields retireved from regular expressions, the return dictionnary is populated with users name and the linked timestamp.

		=============== ============  ==================================================================
		**Parameters**    **Type**     **Description**
		**Users**         *String*     The output of the Origin Licence Request to get Connected users
		=============== ============  ==================================================================

		Returns
		-------
		Dictionnary
		The dictionnary associating to an user name its connexion starting timestamp
	"""
	Jeton_dic={}
	regex=r'[0-9]+\/+'
	regex2=r'[^a-z]\/[0-9]+'
	regex3=r'[0-9]+\:'
	regex4=r'\:[0-9]+'
	regex5=r'^\s*[^:\s]+'
	regex6=r'[A-Z0-9]+-[A-Z0-9]+'
	User_dic={}
	User_list=Users.split('\n')

	if Users!="":

		for item in User_list:
			matches=re.finditer(regex,item,re.MULTILINE)
			for matchNum, match in enumerate(matches, start=1):
				month=int(match.group()[:-1])
			matches=re.finditer(regex2,item,re.MULTILINE)
			for matchNum, match in enumerate(matches, start=1):
				day=int(match.group()[2:])
			matches=re.finditer(regex3,item,re.MULTILINE)
			for matchNum, match in enumerate(matches, start=1):
				hour=int(match.group()[:-1])
			matches=re.finditer(regex4,item,re.MULTILINE)
			for matchNum, match in enumerate(matches, start=1):
				minuts=int(match.group()[1:])
			matches=re.finditer(regex5,item,re.MULTILINE)
			for matchNum, match in enumerate(matches, start=1):
				user=match.group()
			matches=re.finditer(regex6, item, re.MULTILINE)
			for matchNum, match in enumerate(matches, start=1):
				PC=match.group()
			user=user+'@'+PC
			date=d.datetime(2021,month,day,hour,minuts)
			User_dic[user]=time.mktime(date.timetuple())
		return User_dic
	else:
		return None

def cut_dic(Cisco_Dic,div):
	"""
		Split Dictionnary into div differents dictionnary to treat them with parallelism.

		================ ============== ========================================
		**Parameters**   **Type**       **Description**
		**Cisco_Dic**    *Dictionnary*  The Cisco 2 Ip main dictionnary
		**div**          *Integer*      The number of dictionnary slice needed
		================ ============== ========================================

		Returns
		-------
		Dictionnary List
		A list af *div* differents dictiononary 
	"""
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

def Cut_log():
	"""
		Cut logfile since the date (today as default).
		The logwatch file is primary stored into the local folder.
		Once done, It cut the logwatch file since the today date.

		It write the daily logwatch content instead of your local copy of the logwatch file.
	"""
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

def read_log(path):
	"""
		Read the log file and filter the content by regular expression to get the main content of the logwatch file.

		=============== ========== =======================================
		**Parameters**   **Type**   **Description**
		**path**         *String*   The path where the logwatch is stored
		=============== ========== =======================================

		Returns
		-------
		List of List
		The list of list containing the main content sorrted by token in order
	
	"""
	regex=r'[a-z]+([^a-z]+.*[0-9]*\n)+'
	match_list=[]
	tmp=[]
	res=[]
	f=open(path,'r')
	Content=f.read()
	matches=re.finditer(regex, Content, re.MULTILINE)
	for matchNum, match in enumerate(matches, start=1):
		match_list.append(str(match.group()))
	for match in match_list:
		tmp=match.split('\n')
		res.append(tmp)
		tmp=[]
	f.close()

	return res

def Treat_log(match_list):
	"""
		Treat Log file content since regular expression to get 

			* *IP_@ list* : **([0-9]+\.)+[0-9]+**
			* *New user information* : **[A-Za-zëùî0-9]+@[A-Z0-9]+-[A-Z0-9]+**

		The content analized is the outputof the read_log method sorted by token.
		This function link an user to an ip list. This ip list contain all the suceptible ip for this user.

		=============== =============== =========================================================================
		**Parameters**    **Type**        **Description**
		**match_list**    *List of List   The list of list containing the main content sorrted by token in order
		=============== =============== =========================================================================

		Returns
		-------
		Dictionnary
		A dictionnary associating to an user name the associated ip address list from the logwatch file content

	"""
	regex=r'([0-9]+\.)+[0-9]+'
	regex2=r'[A-Za-zëùî0-9]+@[A-Z0-9]+-[A-Z0-9]+'
	banned=['10.14.14.20']
	tmp=[]
	user=''
	User_list={}
	Dic_flag=True
	index=0

	for item in match_list:
		for line in item:

			matches=re.finditer(regex, line, re.MULTILINE)
			matches2=re.finditer(regex2, line, re.MULTILINE)
			for matchNum, match in enumerate(matches2, start=1):
				Dic_flag=(match.group()==None)
				user=match.group()
			for matchNum, match in enumerate(matches, start=1):
				if not (match.group() in banned):
					tmp.append(str(match.group()))
			if not Dic_flag:
				User_list[str(user)+str(index)]=tmp
				tmp=[]
				Dic_flag=True
				index+=1
	return User_list

def diff_list(l1,l2):
	"""
		Compute difference between 2 lists to get the most suceptible ip to assign.
		The difference between two set A and B (A-B) give us the ip addresses present in A but NOT in B.

		=============== ========== ===================================================================
		**Parameters**   **Type**   **Description**
		**l1**           *List*     An Ip list extracted from the Treat_log method return dictionnary
		**l2**           *List*     An Ip list extracted from the Treat_log method return dictionnary
		=============== ========== ===================================================================

		Returns
		-------
		String List
		The list containing the difference between l1 and l2
	"""
	res=[]
	if(len(l1)>len(l2)):
		m=l1
		n=l2
	else:
		m=l2
		n=l1
	for item in m:
		if not item in n:
			res.append(item)
	return res

def Diff_log(User_dic):
	"""
		Associate a new user to the difference between 2 log slice. Reults will be stored into a python dictionnary.

		This function is ruled by the following instructions :

			* **Brownsing the User_dic dictionnary** and filter the hostname by regular expression
			* **Computing the difference between two adjacents lists** using the diff_list function
			* **Associate to an user name its own ip addresses set**

		=============== ================ ======================================================================================================================================
		**Parameters**    **Type**       **Description**
		**User_dic**      *Dictionnary*  The dictionnary associating to an user name the associated ip address list from the logwatch file content from the Treat_log function
		=============== ================ ======================================================================================================================================

		Returns
		-------
		Dictionnary
		The dictionnary associating to an user name an ip addresses set.
	"""
	tmp=[]
	res={}
	for k,v in User_dic.items():
		if not tmp:
			tmp=v
			res[k]=[]
		else:
			diff=diff_list(v,tmp)
			res[k]=diff
			tmp=v
	return res

def Treat_diff(User_dic):
	"""
		Compute the Set difference by User ID between two sets of ip address to get the correct one.
		In fact treat the output of the Diff_log function (removing indexes and merge list if necessary)

		=============== ============= ============================================================================================
		**Parameters**   **Type**      **Description**
		**User_dic**     *Dictionnary  The dictionnary associating to an user name an ip addresses set from the Diff_log function
		=============== ============= ============================================================================================

		Returns
		-------
		Dictionnary
		The updated dictionnary associating to an user name an ip addresses


	"""
	res={}
	regex=r'[A-Za-zëùî0-9]+@[A-Z0-9]+-[A-Z0-9]+'
	index=0

	for k,v in User_dic.items():

		matches=re.finditer(regex,k,re.MULTILINE)
		for matchNum, match in enumerate(matches, start=1):
			if index<10 :
				name=str(match.group())[:-1]
			elif index >=10 and index<100:
				name=str(match.group())[:-2]
			elif index >=100 and index<1000:
				name=str(match.group())[:-3]
			elif index >=1000 and index<10000:
				name=str(match.group())[:-4]
			index+=1
		if v :
			try:
				res[name].extend(v)
			except:
				res[name]=v
	return res

def get_max(liste):
	"""
		Get the max value's index of the list.

		=============== ========== ================================
		**Parameters**   **Type**   **Description**
		**liste**        *List*     Integer or Float list to treat
		=============== ========== ================================

		Returns
		-------
		Integer / Float
		The index of the maximum value of the list
	"""
	maxi=0
	for item in liste:
		if item >= maxi:
			maxi=item
	return liste.index(maxi)

def get_ip(User_dic,IP_list):
	"""
		Get the real (most susceptible one) IP_@ from an user name using successives reults from functions :

			* **read_log**
			* **Treat_log**
			* **Diff_log**
			* **Treat_diff**

		The favorite IP is choosen by number of appearence into the merged list of suceptibles ip address from difference.

		=============== =============== ===========================================================================================================
		**Parameters**   **Type**       **Description**
		**User_dic**     *Dictionnary*  The dictionnary from the successive intermediate functions associating an user a merged list of candidates
		**IP_list**      *String List*  The IP list of connected users
		=============== =============== ===========================================================================================================

		Returns
		-------
		Dictionnary
		The Final dictionnary associating to an user the most suceptible IP address from logwatch analyze
	"""
	favorite=''
	ip_id=[]
	count=[0]*32
	index=0
	User_rep={}

	for k,v in User_dic.items():
		ip_id=list(dict.fromkeys(v))
		for ip in ip_id:
			if not ip in IP_list:
				ip_id.remove(ip)
		if len(ip_id) > 1 :
			for ip in ip_id:
				count[index]=v.count(ip)
				index+=1
			favorite=ip_id[get_max(count)]
			count=[0]*32
			index=0
		else:
			favorite=v[0]
		User_rep[k]=favorite
		favorite=''
	return User_rep	

def diff_ip(ipA,ipB):
	"""
		Get the raw difference between 2 ip address.

		Exemple :

			* IP_a=10.14.20.1
			* IP_b=10.14.21.3

		The difference will be 1.3

		=============== ========== ========================
		**Parameters**   **Type**   **Description**
		**ipA**          *String*   IP address to compare
		**ipB**          *String*   IP address to compare
		=============== ========== ========================

		Returns
		-------
		String
		The raw difference between both of the ip address
	"""
	if len(ipA) > len(ipB):
		while len(ipA)!=len(ipB):
			ipB+='_'
	elif len(ipB) > len(ipA):
		while len(ipA)!=len(ipB):
			ipA+='_'
	return "".join(y for x, y in it.zip_longest(ipA,ipB) if x != y)

def get_IP_from_log(IP_list):
	"""
		DHCP data finder Main Resolution Algorithm.
		This algorithm use and manage the functions:

			* **read_log**
			* **Treat_log**
			* **Diff_log**
			* **Treat_diff**
			* **get_ip**
			* **diff_ip**

		It restore the final dictionnary associating to an user its ip address.

		=============== =============== ==========================================================
		**Parameters**   **Type**       **Description**
		**IP_list**      *String List*  The list extracted from the command's output **ss -n -t**
		=============== =============== ==========================================================

		Returns
		-------
		Dictionnary 
		The Final dictionnary associating to an user the most suceptible IP address from logwatch analyze
	"""
	not_assigned=[]
	current=''
	mini=10

	test=read_log('./logwatch')
	test2=Treat_log(test)
	test3=Diff_log(test2)
	test4=Treat_diff(test3)
	test5=get_ip(test4,IP_list)
	for k,v in test5.items():
		try:
			IP_list.remove(v)
		except:
			not_assigned.append(v)

	for k,v in test5.items():
		if v in not_assigned:
			for ip in IP_list:
				if (len(diff_ip(v,ip))) < mini :
					mini=(len(diff_ip(v,ip)))
					current=ip 
			test5[k]=current
			try:
				IP_list.remove(current)
			except:
				pass
		mini=12
	return test5

def Update_history():
	"""
		This is the main function of the algorithm used to update Origin History since log file.

		This algorithm is ruled by followings steps :

			* **Getting Users acount informations since the top level** : *Environnment variable getter*
			* **Connecting an ssh session to the origin.srv-prive.icgm.fr server** : *Using netmiko module to automate authentified ssh session*
			* **Getting raw users list Informations** : *From the output of the Origin Licence Request, Retrieve the connected users list*
			* **Getting the Port Informations** : *From the* **netstat -anp** *command, retrieve the Origin server's used port number*
			* ** Getting the raw IP list informations** : *From the* **ss -n -t** *command, Dress the list of present IP in connexion table*
			* **Getting the raw hostname list Informations** : *From the* **ss -n -t -r** *command, Get the hostname list preset in connexion table*
			* **Exit the ssh session and read the Ordinateurs.ods file** : *From the Ordinateurs.ods file, Fid and store all the others needed informations as MAC @, Vlan Id, ...*
			* **Updating the Origin_history file since the newest Informations** 

		The results are dispayed at screen but could be write in an Origin History
	"""

	# Getting Users acount informations since the top level

	home= os.getenv('HOME')
	user=os.getenv('USER')
	keyfile=home+'/.ssh/known_hosts'

	# Connecting an ssh session to the origin.srv-prive.icgm.fr server

	ssh_session = netmiko.ConnectHandler(device_type='linux', ip='10.14.14.20', username=user, use_keys=True, key_file=keyfile)

	# Getting raw users list Informations

	Users=ssh_session.send_command('/opt/Linux_FLEXnet_Server_ver_11.16.5.1/lmutil  lmstat -a -c /opt/Linux_FLEXnet_Server_ver_11.16.5.1/Licenses/Origin_20jetons.lic | grep "^.*origin\.srv-prive\.icgm\.fr/27000.*"')
	User_list=treat_Users(Users)
	if User_list==None:
		print("No users connected")
		quit()
	print("Getting informations from the network Scan, Please to wait few minuts...\n")
	print(User_list)

	# Getting the Port Informations

	Nb_Port = ssh_session.send_command('netstat -anp | grep ":::*" | grep LISTEN')
	Real_port=get_Port(Nb_Port)
	print(Real_port)

	if (Real_port > 27000):

		# Getting the raw IP list informations

		IP=ssh_session.send_command('ss -n -t | grep '+str(Real_port)) # | grep -Po "\K([0-9]*\.){3}[0-9]+" 
		IP_list=get_IP_list(IP)
		print(IP_list)

		# Getting the raw hostname list Informations

		Host=ssh_session.send_command('ss -n -t -r | grep '+str(Real_port))
		Host_list=get_Host_list(Host)
		print(Host_list)

		# Exit the ssh session and read the Ordinateurs.ods file

		ssh_session.disconnect()
		Infos=Read_ods('../Ordinateurs.ods',Host_list,IP_list)

		# Updating the Origin_history file since the newest Informations

		User_rep=get_IP_from_log(IP_list)
		print(User_rep)
		to_write=Treat_Info(Infos,IPSwitchs)
		to_write=get_Description(to_write)
		to_write=get_time(to_write,User_rep,User_list)
		for item in to_write:
			print(item)

		# try:
		# 	os.system('scp '+str(user)+'@origin.srv-prive.icgm.fr:/home/mcabos/Origin_history .')
		# except:
		# 	pass
		# Write_in_file(to_write,'./Origin_history')
		# os.system('scp ./Origin_history '+str(user)+'@origin.srv-prive.icgm.fr:/home/mcabos/')

# Initialisation

User_list={}
IP=""
Nb_Port=""
Host=""
IP_list=[]
Host_list=[]
Infos=[]
to_write=[]
User_rep={}
Process_List=[]

# Launching section

Cut_log()
Update_history()
os.system('rm logwatch')
quit()