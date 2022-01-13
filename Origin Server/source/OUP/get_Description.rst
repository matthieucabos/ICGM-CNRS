get_Description
===============

.. code-block:: python

	def get_Description(Data)

______________________________________________________________________________________________________

Definition
----------
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

*String List*

The updated Data list with description field