Read_and_treat_log
==================

.. code-block:: python

	def Read_and_treat_log(path)

_________________________________________________________________

Definition
----------

This function make the association between a Origin user name and its own Ip address.
Read and extract the following informations from the logwatch file using regular expressions :

	* Date : **[a-z]+([^a-z]+.*[0-9]*\\n)+**
	* IP : **([0-9]+\\.)+[0-9]+**
	* Name : **\\"OriginPro\\".**
	* PC : **\\@.***
	* Time : **^[a-z].***

To get informations from the logwatch file, the algorithm is ruled by instructions :

	* **Regular Expression Definition**
	* **Variables Definition**
	* **Open and read the logwatch file**
	* **Getting IP list associated to a timed & named token.** The results are stored by time order, arbitrary indexed from 1 -> n
	* **Getting host ID from the full Origin user name** (with form name@host) => Allow multiple users sessions on the same host
	* **Compute the Set difference between two adjacents Ip set** (indexed +- 1) to get the User's associated IP

================ ========== ========================================
**Parameters**    **Type**    **Description**
**path**          *String*    The path to the logwatch file to read
================ ========== ========================================

Returns
-------
Dictionnary
The name_ip_dict dictionnary associating to an Origin user name its own ip address