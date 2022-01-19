get_Host_list
=============

.. code-block:: python

	def get_Host_list(Host)

______________________________________________________________________________________________________

Definition
----------

Getting Host list since the regular expressions using the output stdout from the ssh remote command output.
Brownsing the string output line by line and filter each line independantly from the others to get the correct hostnames contained.
The hostnames have form *name.dsi0.icgm.fr:60213*, this is the form present into the output of a **ss -n -t -r** command. 

The result is the sorted list of the hostnames. To sort them, I use the **list(dict.fromkeys(liste))** command

=============== =========== ======================================================
**Parameters**   **Type**    **Description**
**Host**         *String*    The ssh remote command output specified as parameter
=============== =========== ======================================================

Returns
-------

*String List*

A list containing all the hostnames founded into the ssh remote command output.