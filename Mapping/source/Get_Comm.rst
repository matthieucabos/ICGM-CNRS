Get_Comm
========

.. code-block:: python

	def Get_Comm(file_name,Final_dict)

_________________________________________________________________

**Algorithm**
-------------

Getting Comments fields from the '.ods' file_name.
It returns a Dictionnary associating a Computer name to its Comments.

=============== ============= =============================================
**Parameters**   **Type**      **Description**
*file_name*      String         The .ods file_name to read
*Final_dict*     Dictionnary    The Main Informations Dictionnary to read
=============== ============= =============================================


:Returns: Dictionnary : A Dictionnary associating Comments to the linked Computer Name on the network

_________________________________________________________________

**Source Code**
---------------


.. code-block:: python

	Comm_dict={}
	Records = p.get_array(file_name=file_name)
	Comm=''

	for record in Records:
		if record[0] in Final_dict.keys():
			Comm_dict[record[0]]=record[3]
	return Comm_dict