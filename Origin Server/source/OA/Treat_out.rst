Treat_out
=========

.. code-block:: python

	def Treat_out(output)

_________________________________________________________________

Definition
----------

Treating shell command ouptut since the tftp Boot informations reading.

To do so, this function is ruled by regular expression as :

* *regex_ip* : **([0-9]+\\.){3}[0-9]+**
* *regex_mac* : **([a-zA-Z0-9]{4}\\.){2}[a-zA-Z0-9]{4}**
* *regex_socket* : **Gi([0-9]+\\/){2}[0-9]+**
* *regex_vlan* : **\\s[0-9]{3}\\s**
* *regex_switch* : **Balard-[0-9A-Z]+\\-[0-9]+**

This method treat a commands list output from a ssh session with a cisco switch.
It read and treat in multiline mode every met values from regular expression and store these informations into the returned dictionnary.
The returned dictionnary is builded with the ip as key and following informations as values :

* **MAC address**
* **Cisco GigabitEthernet socket (with form Gix/y/z)**
* **The Vlan identifier as Integer**
* **The switch name as String**

=============== =========== =======================================================================
**Parameters**   **Type**    **Description**
**output**        *Str*      The raw commands list output from the ssh session with a cisco switch
=============== =========== =======================================================================

Returns
-------

*Dictionnary*

The builded dictionnary linking to an ip as key the Cisco informations