get_ip
======

.. code-block:: python

	def get_ip(User_dic,IP_list)

______________________________________________________________________________________________________

Definition
----------

Get the real (most susceptible one) IP_@ from an user name using successives reults from functions :

	* **read_log**
	* **Treat_log**
	* **Diff_log**
	* **Treat_diff**

The favorite IP is choosen by number of appearence into the merged list of suceptibles ip address from difference.

=============== =============== ===========================================================================================================
**Parameters**   **Type**       **Description**
**User_dic**     *Dictionnary*  The dictionnary from the successive intermediate functions associating an user a merged list of candidates
**IP_list**      *String List*  The IP list of connected users
=============== =============== ===========================================================================================================

Returns
-------

*Dictionnary*

The Final dictionnary associating to an user the most suceptible IP address from logwatch analyze