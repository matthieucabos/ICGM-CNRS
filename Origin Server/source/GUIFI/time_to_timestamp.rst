time_to_timestamp
=================

.. code-block:: python

	def time_to_timestamp(str_time)

_________________________________________________________________

Definition
----------

Utilitary converter function getting timestamp from the given string date.
It uses regular expressions filtering to get time and month field.
The timestamp is generated since the retrieved informations passed as parameters of the **time.mktime()** command.

=============== ========== ==================================
**Parameters**   **Type**   **Description**
**str_time**     *String*   The date-time formated as String
=============== ========== ==================================

Returns
-------
Integer
The correct converted timestamp