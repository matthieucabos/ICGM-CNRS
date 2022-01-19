cut_dic
=======

.. code-block:: python

	def cut_dic(IPSwitchs,div)

_________________________________________________________________

Definition
----------

Utilitary method to split properly and in adequation with the multiprocessing parameters the given dictionnary.

Split Dictionnary into div differents dictionnary.

================ ========== ============================================================================
**Parameters**   **Type**    **Description**
**IPSwitchs**    *Dict*      The shared dictionnary associating to a Cisco switch name its IP address.
**div**          *Integer*   The number of slices to build from the given dictionnary
================ ========== ============================================================================

Returns
-------

*List*

A list of dictionnary containing the main dictionnary splitted into div differents sections.