Origin_Users_parallelisation_v2
===============================

Here the pages dedied to the Pré-versions of the project.

The first one, called Origin_Users_parallelisation_v2.py use the DHCP configuration ods file to retrieve the main informations.
The principe is a bit different and will be xplained function by function.

This is the main function of the algorithm used to update Origin History since log file.

This algorithm is ruled by followings steps :

	* **Getting Users acount informations since the top level** : *Environnment variable getter*
	* **Connecting an ssh session to the origin.srv-prive.icgm.fr server** : *Using netmiko module to automate authentified ssh session*
	* **Getting raw users list Informations** : *From the output of the Origin Licence Request, Retrieve the connected users list*
	* **Getting the Port Informations** : *From the* **netstat -anp** *command, retrieve the Origin server's used port number*
	* **Getting the raw IP list informations** : *From the* **ss -n -t** *command, Dress the list of present IP in connexion table*
	* **Getting the raw hostname list Informations** : *From the* **ss -n -t -r** *command, Get the hostname list preset in connexion table*
	* **Exit the ssh session and read the Ordinateurs.ods file** : *From the Ordinateurs.ods file, Fid and store all the others needed informations as MAC @, Vlan Id, ...*
	* **Updating the Origin_history file since the newest Informations** 

The results are dispayed at screen but could be write in an Origin History

