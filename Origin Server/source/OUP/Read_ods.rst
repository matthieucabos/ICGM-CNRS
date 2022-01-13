Read_ods
========

.. code-block:: python

	def Read_ods(path,Host_list,IP_list)

______________________________________________________________________________________________________

Definition
----------

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

*String List*

The List repertoring the following informations as item :

	* Hostname
	* MAC address
	* Departemet ID
	* IP address