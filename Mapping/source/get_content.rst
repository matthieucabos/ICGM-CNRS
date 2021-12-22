get_content
===========

.. code-block:: python

	def get_content(switch_name):

_________________________________________________________________

**Algorithm**
-------------

Get content from file since the switch_name argument.
This function read the file and store informations into the return value.

============== ============ =============================================
**Parameters**   **Type**   **Description**
*switch_name*  String       The exact switch_name from switch_dict keys
============== ============ =============================================

:Returns: String : The full Content of the file stored into a String Variable

_________________________________________________________________

**Source Code**
---------------

.. code-block:: python

	f=open(switch_name,'r')
	return f.readlines()