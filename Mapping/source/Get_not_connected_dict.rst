Get_not_connected_dict
======================

.. code-block:: python

	def Get_not_connected_dict(file_name,Final_dict)

_________________________________________________________________

**Algorithm**
-------------

Similary building a Dictionnary with fewer informations for the disconnected Users.

=============== ============== ===========================================
**Parameters**   **Type**      **Description**
*file_name*      String        The .ods file_name to read
*Final_dict*     Dictionnary   The Main Informations Dictionnary to read
=============== ============== ===========================================

:Returns: Dictionnary :  A Dictionnary linking informations from the server to store the Disconnected Authorised Users

_________________________________________________________________

**Source Code**
---------------

.. code-block:: python

	Not_Conctd_Dict={}
	Records = p.get_array(file_name=file_name)
	dpt_dict=Get_Dpt(file_name)

	for record in Records:
		if not record[0] in Final_dict.keys():
			try:
				Not_Conctd_Dict[record[0]]=[record[1],Dpt_dict[record[0]],'','','','','','',record[3]]
			except:
				pass
	return Not_Conctd_Dict
