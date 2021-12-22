Get_Dpt
=======


.. code-block:: python

	def Get_Dpt(file_name)

_________________________________________________________________

**Algorithm**
-------------

Getting Departement ID from the file_name ods file containing all the Vlans Informations.
The Vlan name is readed and associated to its Id number.

=============== =========== =========================
**Parameters**   **Type**   **Description**
*file_name*       String     An .ods file to read
=============== =========== =========================

:Returns: Dictionnary : The Departement dictionnary associating a Departement Id to a Computer Name on the network

_________________________________________________________________

**Source Code**
---------------


.. code-block:: python

	Dpt2Int_dict={
	'DPT1':510,
	'DPT2':511,
	'DPT3':512,
	'DPT4':513,
	'DPT5':514,
	'SGAF':524,
	'INSTRU-ON':515,
	'SSI':525,
	'INSTRU-OFF':516,
	'IMPRIM':518,
	'IDRAC-CIN':528,
	'IDRAC':501,
	'ExpProtect':526
	}

	Dpt_dict={}
	Records = p.get_array(file_name=file_name)
	Dpt_name=''

	for record in Records:
		for Dpt,v in Dpt2Int_dict.items():
			if Dpt in record[2] :
				Dpt_dict[record[0]]=v 
				break

	return Dpt_dict