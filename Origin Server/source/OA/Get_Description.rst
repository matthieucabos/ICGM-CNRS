Get_Description
===============

.. code-block:: python

	def Get_Description(Snoop_Dict)

_________________________________________________________________

Definition
----------

Get the full plug name since the Snoop dictionnary present into the tftp server (into the *var/lib/tftpboot/snoop/* repertory).

Only the real connected users will be repertoried here since the snoop tftp boot repertory.
This methos has been partially coded with a parallel section to treat ssh connection faster.

This method is following this algorithm :

* **Building Cisco Instructions list** by Switch (stored into the *tmp* variable)
* **Manage the multiprocessing section** of the code with the splitted Switch Dictionnary and the shared return dictionnary to store results of ssh sessions.
* **Launching the multiprocess list** with the correct method *ssh_session* and associated builded Cisco instructions list.
* **Start and join the differents process** and rebuild the return dictionnary sorted by Cisco Switch name
* The results of **the multiples ssh session give us the full outlet description name** (with form N1A01-01) by regular expression filtering
* **Build the Description_dictionnary** linking to a Cisco gigabitEthernet socket (Gix/y/z) as key its outlet exact description.

================ =========== ========================================================
**Parameters**    **Type**    **Description**
**Snoop_Dict**    *Dict*      The snoop dictionnary extracted from the tftp server
================ =========== ========================================================

Returns
-------

*Dictionnary*

The builded dictionnary associating to a cisco gigabit ethernet socket *(Gix/y/z)* its exact outlet description name as String.