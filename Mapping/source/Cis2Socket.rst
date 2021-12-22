Cis2Socket
==========

.. code-block:: python

	def Cis2Socket(Cisco_name,Final_dict)

_________________________________________________________________

**Algorithm**
-------------

Getting the exact Room Socket Name from the GigabitEthernet Triolet provided by Cisco informations.
The Socket Name is stored in the given Dictionnary

=============== ============= ==========================================
**Parameters**   **Type**      **Description**
*Cisco_name*     String        The exact name of the Switch 
*Final_dict*     Dictionnary   The Final Dictionnary to be updated
=============== ============= ==========================================

:Returns: Dictionnary : The Final Dictionnary to be write updated

_________________________________________________________________

**Source Code**
---------------

.. code-block:: python

	regex=r'[A-Z][0-9][A-Z][0-9]+.[0-9]*'
	os.system('ssh -t '+str(Cisco_name)+' show interface description > Description_'+str(Cisco_name))
	f=open('Description_'+str(Cisco_name),'r')
	l=f.readlines()
	Tmp_dict={v:k for k,v in switch_dict2.items()}
	Plug_liste=[]

	for k,v in Final_dict.items():
		if v[4] == Tmp_dict[Cisco_name]:
			Plug_liste.append((v[6][2:],k))

	for line in l:
		for hw in Plug_liste:
		    if hw[0] in line:
		    	matches = re.finditer(regex, line,re.MULTILINE)
		    	for matchNum, match in enumerate(matches, start=1):
		    		tmp=Final_dict[hw[1]]
		    		tmp[7]=match.group()
		    		Final_dict[hw[1]]=tmp
		    	del Plug_liste[Plug_liste.index(hw)]

	return Final_dict