get_Connected
=============

.. code-block:: python

	def get_Connected()

_________________________________________________________________

Definition
----------

Get connected user list since the orgin token licence.
The function read the Licence manager from Origin and extract the connected users name list.
This function use regular expression matching to get user name from the ssh remote command output :

.. code-block:: bash

	/opt/Linux_FLEXnet_Server_ver_11.16.5.1/lmutil  lmstat -a -c /opt/Linux_FLEXnet_Server_ver_11.16.5.1/Licenses/Origin_20jetons.lic | grep "^.*origin\.srv-prive\.icgm\.fr/27000.*"

Returns
-------
String List
The list containing all the Origin connected hostnames