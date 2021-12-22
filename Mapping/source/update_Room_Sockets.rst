update_Room_Sockets
===================

.. code-block:: python

	def update_Room_Sockets(ip_switch,Final_dict)

_________________________________________________________________

**Algorithm**
-------------

Updating the Room Sockets Name field of the Dictionnary using the Cisco2Socket Procedure.
Each Switch will be treated **independantly** from each others.
It must be applied to each Switch to get the full Contents updated.

=============== ============ =============================================
**Parameters**   **Type**     **Description**
*ip_switch*      String       The exact IP adress of the current switch
*Final_dict*     Dictionnary  The Final Dictionnary to be updated
=============== ============ =============================================

:Returns: Dictionnary : The updated Dictionnary

_________________________________________________________________

**Source Code**
---------------

.. code-block:: python

	liste=[]
	Plug_liste=[]
	for k,v in Final_dict.items():
		if v[3]==ip_switch:
			liste.append(v[5])
	ind=0
	Plug_liste=Cisco2Socket(switch_dict2[ip_switch],' '.join(liste))	
	for k,v in Final_dict.items():
		if v[3]==ip_switch:
			try:
				v[6]=Plug_liste[ind]
				ind+=1
			except:
				break

	return Final_dict