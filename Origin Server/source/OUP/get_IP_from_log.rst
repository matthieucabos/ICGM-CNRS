get_IP_from_log
===============

.. code-block:: python

	def get_IP_from_log(IP_list)

______________________________________________________________________________________________________

Definition
----------

DHCP data finder Main Resolution Algorithm.
This algorithm use and manage the functions:

	* **read_log**
	* **Treat_log**
	* **Diff_log**
	* **Treat_diff**
	* **get_ip**
	* **diff_ip**

It restore the final dictionnary associating to an user its ip address.

=============== =============== ==========================================================
**Parameters**   **Type**       **Description**
**IP_list**      *String List*  The list extracted from the command's output **ss -n -t**
=============== =============== ==========================================================

Returns
-------

*Dictionnary*

The Final dictionnary associating to an user the most suceptible IP address from logwatch analyze