get_Dict
========

.. code-block:: python

	def get_Dict()

_________________________________________________________________

Definition
----------

Get the main informations dictionnary repertoring these following field:

* **IP address as key**
* **MAC address**
* **Cisco Socket**
* **Vlan Identifier**
* **Cisco Switch name**
* **Outlet Description**

The five firsts informations are extracted from the tftp boot server to get exact real values from cisco switch.
The last one is extracted from Cisco switch multiple requests.


Returns
-------

*Dictionnary*

The Snoop dictionnary repertoring all the needed network informations.