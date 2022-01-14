ssh_session
===========

.. code-block:: python

	def ssh_session(cisco,command)

_________________________________________________________________

Definition
----------

Treat a ssh remote command session. Automate the authentified ssh connexion and restitute the remote command output

=============== ============== ====================================
**Parameters**   **Type**       **Description**
**cisco**        *String*       The cisco switch name to connect
**command**      *String List*  The command list as a string list
=============== ============== ====================================

Returns
-------
String
The remote command output