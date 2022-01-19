Compute_elapsed_time
====================

.. code-block:: python

	def Compute_elapsed_time(Start_dict)

_________________________________________________________________

Definition
----------

Compute the elapsed time connection dictionnary associating an user to his connexion time.
The function take one parameter : the dictionnary associating to an user a string start time extracted from the Origin Licence request.

Each user is brownsed by for loop to extract hour and minuts to make the timestamp.
The result is obtained making the timestamp difference between now and the start time, converted in minuts by dividing by 60.

=============== =============== =======================================================
**Parameters**    **Type**       **Description**
**Start_dict**    *Dictionnary*  The dictionnary associating to an user his start time
=============== =============== =======================================================

Returns
-------
Dictionnary
The dictionnary associating to an user his connexion time, computed by timestamp