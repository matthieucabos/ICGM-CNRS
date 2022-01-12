build_dict
==========

.. code-block:: python

	def build_dict()

_________________________________________________________________

Definition
----------

Building Timing dictionnary from the logwatch file.

To do so, I use the treat_tokens.sh script file with the following arguments 3,4,5,6 to get respectively the following informations :

* **IN Tokens Hostname**
* **OUT Token Hostname**
* **IN Tokens Timestamp allocation**
* **OUT Tokens Timestamp allocation**

The builder algorithm is defined as following : 

* **Once informations retrieved** from Treat_tokens script, **transtype** them to python list and merge IN and OUT hostname lists and IN and OUT Timestamp Lists.
* **For each user found in the Hostname list, store the associated timestamps** into a temporary list and associate the list to a user name via Python Dictionnary Token_dict.
* Brownsing the Token_dict and **for each hostname present in the Connected Users List, Compute the absolute time value.**

The Final reult is given as a dictionnary associating to each connected user hostname its connection time elapsed.

Returns
-------

*Dictionnary*

The Timer dictionnary associating to a hostname its connection time