cut_dic
=======

.. code-block:: python

	def cut_dic(Cisco_Dic,div)

_________________________________________________________________

Definition
----------

Split Dictionnary into div differents dictionnary.
Useful function for parallelism section.

=============== =============== ========================================================================
**Parameters**   **Type**        **Description**
**Cisco_Dic**    *Dictionnary*   The dictionnary containing all the Cisco name:IP address informations
**div**          *Integer*       The number of slice to get
=============== =============== ========================================================================

Returns
-------
List of Dictionnaries
The List of Sliced dictionnaries