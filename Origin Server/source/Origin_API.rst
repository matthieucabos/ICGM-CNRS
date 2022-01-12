Origin_API
==========



**Author** *CABOS Matthieu*

**Date**  *2021/2022*

**Organization** *ICGM-CNRS*


This is the main methods repertory needed to manage properly an Origin Server.

It contains all the following functions : 

* **The Get Connexion Time Section** :
    * *Init_dict* : Initialize a dictionnary with defaults values
    * *get_max* : get the ma value from a list
    * *get_min* : Get the min value from a list
    * *is_connected* : Check if a specific user is connected
    * *build_dict* : Build the Commexion time elapsed dictionnary sort by user hostname
* **The Tftp Server Informations Getter Section** :
    * *ssh_session* : Automate an authentified ssh session
    * *Treat_out* : treat the Cisco output of an ssh session
    * *Get_Description* : Get the outlet description from a gigabithethernet socket
    * *cut_dic* : Split a dictionnary into slices to treat the parallel section
    * *get_Dict* : Get the tftp Snoop dictionnary repertoring all the needed informations
* **The Get Connected Users Section**:
    * *reverse* : Reverse the given list
    * *pop_double* : Treat the string list to retrieve hostname information
    * *Get_Connected* : Get the full hostname list from the connected users list

All these functions have been wrote for the ICGM laboratry network and must be adapted to another network (Ssh passerel identification informations, Cisco switchs name and addresses, etc...)   

Please to load it directly into a Python interpreter from the command :

.. code-block:: python

	from Origin_API import *


.. toctree::
	:maxdepth: 1

	Init_dict
	get_max
	get_min
	is_connected
	build_dict
	ssh_session
	Treat_out
	Get_Description
	cut_dic
	get_Dict
	reverse
	pop_double
	Get_Connected