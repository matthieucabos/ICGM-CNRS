Diff_log
========

.. code-block:: python

	def Diff_log(User_dic)

______________________________________________________________________________________________________

Definition
----------

Associate a new user to the difference between 2 log slice. Results will be stored into a python dictionnary.

This function is ruled by the following instructions :

	* **Brownsing the User_dic dictionnary** and filter the hostname by regular expression
	* **Computing the difference between two adjacents lists** using the diff_list function
	* **Associate to an user name its own ip addresses set**

=============== ================ ======================================================================================================================================
**Parameters**    **Type**       **Description**
**User_dic**      *Dictionnary*  The dictionnary associating to an user name the associated ip address list from the logwatch file content from the Treat_log function
=============== ================ ======================================================================================================================================

Returns
-------

*Dictionnary*

The dictionnary associating to an user name an ip addresses set.