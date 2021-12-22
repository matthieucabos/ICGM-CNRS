Get_switch_port_dict
====================

.. code-block:: python

	def Get_switch_port_dict(ip_switch):

_________________________________________________________________

**Algorithm**
-------------

Read the tmp file containing SNMP informations and sort and store them into a Dictionnary with form :
@Mac : Hardware Port Number

=============== ========== ===========================================
**Parameters**   **Type**   **Description**
*ip_switch*      String     The exact IP adress of the current switch
=============== ========== ===========================================

:Returns: Dictionnary : The dictionnary associating a @mac to the hardware port number

_________________________________________________________________

**Source Code**
---------------

.. code-block:: python

	liste_addr=os.popen('cat tmp'+str(ip_switch))
	regex = r"([0-9a-z]{2}:){5}[0-9a-z]{2}"
	regex2=r"\.[0-9]+"
	Switch_port_dict={}

	for line in liste_addr.readlines():
		current_mac=""
		current_port=""
		matches = re.finditer(regex, line, re.MULTILINE)
		matches2 = re.finditer(regex2, line, re.MULTILINE)

		for matchNum, match in enumerate(matches, start=1):    # Looking for @MAC
			current_mac=str(match.group())
		for matchNum, match in enumerate(matches2, start=1):    # Looking for corresponding port number
			current_port=str(match.group())
			if current_mac :
				Switch_port_dict[current_mac]=current_port[1:]

	return Switch_port_dict