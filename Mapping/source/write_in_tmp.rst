write_in_tmp
============

.. code-block:: python

	def write_in_tmp(ip_switch):

_________________________________________________________________

**Algorithm**
-------------

Get SNMP informations and store it into the tmp file.

=============== ========== ===========================================
**Parameters**   **Type**   **Description**
*ip_switch*      String     The exact IP adress of the current switch
=============== ========== ===========================================

:Returns: None

_________________________________________________________________

**Source Code**
---------------

.. code-block:: python

	os.system('snmpwalk -v 1 -c comaccess '+str(ip_switch)+':161 1.3.6.1.2.1.2.2.1.6 > tmp'+str(ip_switch))