Get_Port_and_GB
===============

.. code-block:: python

	def Get_Port_and_GB(ip_switch,Final_dict)

_________________________________________________________________

**Algorithm**
-------------

Populate the Final Dictionnary with Hardware Port Number values from Cisco SNMP Values (as verification of configuration...).

=============== ============= ===========================================
**Parameters**   **Type**     **Description**
*ip_switch*      String       The exact IP adress of the current switch
*Final_dict*     Dictionnary  The Final Dictionnary to be updated
=============== ============= ===========================================

:Returns: Dictionnary : The Final Dictionnary to be write updated

_________________________________________________________________

**Source Code**
---------------

.. code-block:: python

	Switch_port_dict=Get_switch_port_dict(ip_switch) # As example
	liste_addr=[]

	# Gettind @mac list
	for k in Switch_port_dict.keys():
		liste_addr.append(k)

	# Populate the Final Dictionnary to be write
	for k,v in Final_dict.items():
		if (v[0] in liste_addr):
			v[4]=Switch_port_dict[v[0]]
			v[5]=os.popen('./Cisco.sh '+str(v[3])+' 1 '+str(v[4])).read()
		pass

	return Final_dict