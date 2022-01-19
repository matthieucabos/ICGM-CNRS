Get_origin_connected
====================

.. code-block:: python

	def Get_origin_connected()

_________________________________________________________________

Definition
----------

Manage a ssh session with the origin server to get the raw output of the Licence request to get connected users.
The used remote command is :


.. code-block:: shell
	
	/opt/Linux_FLEXnet_Server_ver_11.16.5.1/lmutil  lmstat -a -c /opt/Linux_FLEXnet_Server_ver_11.16.5.1/Licenses/Origin_20jetons.lic | grep "^.*origin\.srv-prive\.icgm\.fr/27000.*"

Returns
-------
String
The output of the ssh remote command