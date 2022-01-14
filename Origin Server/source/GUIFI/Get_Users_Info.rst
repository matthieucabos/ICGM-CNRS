Get_Users_Info
==============

.. code-block:: python

	def Get_Users_Info(IP_list)

_________________________________________________________________

Definition
----------

Building DHCP dictionnary and get infos since the given IP adresses list as parameter.

To do so, the DHCP dictionnary construction obey to the following looped instructions :

* Define the following regular expression to retrieve the differents fields from the DHCP configuration files :

	* MAC address : **([0-9A-Fa-f]{2}\:){5}[0-9A-Fa-f]{2}**
	* IP address : **fixed.***
	* Raw ip : **([0-9]+\.){3}[0-9]+**
	* Hostname : **\"[A-Za-z0-9-_]+\"**
	* Cisco name : **Gi([0-9]+\/){2}[0-9]+**
	* Outlet Description : **[NRJPASEP]+[0-9]+[A-K][0-9]+-[0-9]+**

* For each vlan present on the network :

	* Read the associated dhcps-vlanId.conf file
	* For each slice of the file :

		* Get informations since the regular expressions filtering
		* Store them into the tmp_dict dictionnary
		* Append the dictionnary to the Users list

	* Delete duplicated values from the Users list if necessary
	* Store the Users list into the DHCP_Dict dictionnary (sorted by Vlan name)

The main algorithm used to link informations together is ruled by the followings steps :

	* **Regular Expressions Definition**
	* **Building DHCP Dictionnary**
	* **Updating Users Dictionnary since the DHCP dictionnary** *from the ip correspondance (as key entry of the Users dictionnary)*
	* **Updating the Users Dictionnary since the Cisco output command** : **ssh <Cisco_name> 'show mac address'** *to get the associated cisco switch ID and the gigabit ethernet ID*

=============== =============== ===================================================================================
**Parameters**   **Type**       **Description**
**IP_list**      *String List*  The ip address list to treat as input (corresponding to the connected users list)
=============== =============== ===================================================================================

Returns
-------
Dictionnary
The Users Dictionnary repertoring all the needed informations from the DHCP configuration files.