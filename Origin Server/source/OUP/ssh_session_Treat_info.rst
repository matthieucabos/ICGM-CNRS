ssh_session_Treat_info
======================

.. code-block:: python

	def ssh_session_Treat_info(cisco,IPSwitchs)

______________________________________________________________________________________________________

Definition
----------

Automated authentified ssh session with parameters.
The associated remote command is **sh mac address-table** to automate the Cisco request y ssh.

=============== =============== ================================================================
**Parameters**   **Type**        **Description**
**cisco**        *String*        The Cisco Switch name to connect
**IPSwitchs**    *Dictionnary*   The dictionnary associating to each Switch name its IP address
=============== =============== ================================================================

Returns
-------

*String*

The raw output of the ssh remote command