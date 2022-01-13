get_time
========

.. code-block:: python

	def get_time(Data,User_rep,User_list)

______________________________________________________________________________________________________

Definition
----------

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

*String List*

The updated Data list with field Time Elapsed