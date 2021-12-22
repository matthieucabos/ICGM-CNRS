Cisco2Socket
============

.. code-block:: python

	def Cisco2Socket(Cisco_name,*args)

_________________________________________________________________

**Algorithm**
-------------

Getting the exact Room Socket Name from the GigabitEthernet Triolet provided by Cisco informations.

=============== ========== =========================================================================================
**Parameters**   **Type**   **Description**
*Cisco_name*     String     The exact name of the Switch 
*args*           String     A long string containing all the Hardware Cisco Port Number separated with a space key
=============== ========== =========================================================================================

:Returns: List : A List containing all the Room Socket Exact Name

_________________________________________________________________

**Source Code**
---------------

.. code-block:: python

	Socket_name=[]
	for i in range(len(args)):
		Socket_name.append(args[i])

	Cisco_list=['Balard-EP-1','Balard-PAC-1','Balard-PAC-2','Balard-RDC-1','Balard-1C-1','Balard-1D-1','Balard-1G-1','Balard-1G-2','Balard-1H-1','Balard-2C-1','Balard-2D-1','Balard-2G-1','Balard-2H-1','Balard-2H-2','Balard-3C-1','Balard-3D-1','Balard-3G-1','Balard-3G-2','Balard-3H-1','Balard-4C-1','Balard-4D-1','Balard-4G-1','Balard-4H-1']
	f=open("Cisco2Socket.sh","a")
	f.write('#!/bin/bash\n# Author : CABOS Matthieu\n# Date : 08/10/2021\nterm shell\n')
	Cisco_Rep=[]	
	res={}

	for i in range(1,4):
		for j in range(1,49):
			f.write('show interface GigabitEthernet'+str(i)+'/0/'+str(j)+' | grep "N[0-9][A-Z][0-9][0-9]*-[0-9]*" \n')
	
	f.write('show interface GigabitEthernet0/0/0')
	f.close()
	os.system('ssh '+str(Cisco_name)+" < Cisco2Socket.sh > tmp2.txt")
	os.system('grep -v "^[[:space:]]*$" tmp2.txt > tmp2')
	os.system('rm tmp2.txt')
	i=7
	nb_ligne=int(os.popen('wc -l tmp2 | cut -d " " -f1').read())-i
	ind=1
	jnd=1
	while i <= nb_ligne:
		res[str(ind)+'/0/'+str(jnd)] = os.popen('cat tmp2 | head -'+str(i)+' | tail -2 | grep "N[0-9][A-Z][0-9][0-9]*-[0-9]*" | cut -d " " -f4 | sed "s/,//"').read()
		i+=2
		jnd+=1
		if jnd==49:
			ind=(ind + 1) if (ind <= 4) else 1 
			jnd=1
	os.system('rm tmp2')
	os.system('rm Cisco2Socket.sh')
	rez=[]
	GBname=''
	for socket in Socket_name :
		for k,v in res.items():
			if k==socket:
				GBname=v
				break		
		rez.append(GBname[:-1])
	return rez