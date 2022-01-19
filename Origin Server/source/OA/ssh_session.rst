ssh_session
===========

.. code-block:: python

	def ssh_session(cisco,command,return_dict)

_________________________________________________________________

Definition
----------

Configure and execute a SSH session with remote commands (not an option.)

It is an automatic authentified ssh session, using the environment parameters as :

* **Home absolute way**
* **user from environment variables**
* **ssh keyfile from the given absolute way**

The results will be stored into the return dict dictionnary using the Python Multithreading functions.

=============== =============== ========================================================
**Parameters**    **Type**       **Description**
**cisco**        *Str*           The name of the Cisco Switch to connect
**command**      *Str List*      The String command list to send to the cisco switch
**return_dict**  *Dictionnary*   The dictionnary storing commands output by Cisco name
=============== =============== ========================================================


Returns
-------

*Dictionnary*

The dictionnary linking to a Cisco switch name as a key its commands list output from console.