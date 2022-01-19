get_IP_list
===========

.. code-block:: python

	def get_IP_list(IP)

______________________________________________________________________________________________________

Definition
----------

Getting IP list since the regular expressions using the output stdout from the ssh remote command output
The filtering operation is done in multiline mode and will be coursed match by match.
The result is shown as a list of ip address.

=============== ========== =======================================================
**Parameters**   **Type**   **Description**
**IP**           *String*   The ssh remote command output specified as parameter
=============== ========== =======================================================

Returns
-------

*String List*

The list containing all the ipaddress founded in the ssh remote command output.