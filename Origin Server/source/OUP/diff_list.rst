diff_list
=========

.. code-block:: python

	def diff_list(l1,l2)

______________________________________________________________________________________________________

Definition
----------

Compute difference between 2 lists to get the most suceptible ip to assign.
The difference between two set A and B (A-B) give us the ip addresses present in A but NOT in B.

=============== ========== ===================================================================
**Parameters**   **Type**   **Description**
**l1**           *List*     An Ip list extracted from the Treat_log method return dictionnary
**l2**           *List*     An Ip list extracted from the Treat_log method return dictionnary
=============== ========== ===================================================================

Returns
-------

*String List*

The list containing the difference between l1 and l2