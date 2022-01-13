treat_Users
===========

.. code-block:: python

	def treat_Users(Users)

______________________________________________________________________________________________________

Definition
----------

Managing Tokens allocation (Time Elapsed since the first Token).
This method read the content of the requested Licence file.

Differents regular expressions manage the results :

	* *month* : **[0-9]+\/+**
	* *day* : **[^a-z]\/[0-9]+**
	* *hour* : **[0-9]+\:**
	* *minuts* : **\:[0-9]+**
	* *user* : **^\s*[^:\s]+**
	* *PC* : **[A-Z0-9]+-[A-Z0-9]+**

Once the differents fields retireved from regular expressions, the return dictionnary is populated with users name and the linked timestamp.

=============== ============  ==================================================================
**Parameters**    **Type**     **Description**
**Users**         *String*     The output of the Origin Licence Request to get Connected users
=============== ============  ==================================================================

Returns
-------

*Dictionnary*

The dictionnary associating to an user name its connexion starting timestamp