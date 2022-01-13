Treat_Info
==========

.. code-block:: python

	def Treat_Info(Infos,IPSwitchs)

______________________________________________________________________________________________________

Definition
----------

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

*String List*

'Ready to print' String list where each item is associated with a user and have form : *'Cisco : | Vlan / Mac_@ / GiB : | Host : | Dpt : | IP_@ '*