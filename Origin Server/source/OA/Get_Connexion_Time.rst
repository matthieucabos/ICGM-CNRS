Get_Connexion_Time
==================

.. code-block:: python

	def Get_Connexion_Time()

_________________________________________________________________

Definition
----------

Main algorithm manager.
It is used to organize the algorithm rules :

	* Get the raw connected users from origin request. 
	* Treating the Output via the Get_Connected method to rebuild hostname with syntax <name>@<host>
	* Associate to each hostname its timestamp using following regular expression : **[0-9]+\:[0-9]+**
	* Compute the elapsed connexion time with the previous defined *Compute_elapsed_time* method.

It returns a dictionnary associating to each hostname its connexion time. The keys of the dictionnary should be used as list entry of connected people.

Returns
-------
Dictionnary
The dictionnary associating to an user his connexion time, computed by timestamp