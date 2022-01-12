Get_Connected
=============

.. code-block:: python

	def Get_Connected()

_________________________________________________________________

Definition
----------

Getting the full connected users list in the origin server since the ssh remote commands.

The automated ssh session request the users list to the origin server Licence manager.

Once the list stored, it is treated by regular expression to extract the hostname list.

This funtion use the pop_double method.

Returns
-------

*Str List*

The full connected at Origin hostname list as Strings.