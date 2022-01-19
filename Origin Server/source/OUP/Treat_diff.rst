Treat_diff
==========

.. code-block:: python

	def Treat_diff(User_dic)

______________________________________________________________________________________________________

Definition
----------

Compute the **Set difference by User ID** between two sets of ip address to get the correct one.

In fact treat the output of the **Diff_log** function (removing indexes and merge list if necessary)

=============== ============= ============================================================================================
**Parameters**   **Type**      **Description**
**User_dic**    *Dictionnary*  The dictionnary associating to an user name an ip addresses set from the Diff_log function
=============== ============= ============================================================================================

Returns
-------

*Dictionnary*

The updated dictionnary associating to an user name an ip addresses