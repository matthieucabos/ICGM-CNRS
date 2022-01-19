Treat_log
=========

.. code-block:: python

	def Treat_log(match_list)

______________________________________________________________________________________________________

Definition
----------

Treat Log file content since regular expression to get 

	* *IP_@ list* : **([0-9]+\\.)+[0-9]+**
	* *New user information* : **[A-Za-zëùî0-9]+@[A-Z0-9]+-[A-Z0-9]+**

The content analized is the outputof the read_log method sorted by token.
This function link an user to an ip list. This ip list contain all the suceptible ip for this user.

=============== =============== =========================================================================
**Parameters**    **Type**        **Description**
**match_list**  *List of List*   The list of list containing the main content sorrted by token in order
=============== =============== =========================================================================

Returns
-------

*Dictionnary*

A dictionnary associating to an user name the associated ip address list from the logwatch file content