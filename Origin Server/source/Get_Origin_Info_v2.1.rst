Get_Origin_Info_v2.1.sh
=======================

.. code-block:: bash

	Get_Origin_Info_v2.1.sh


This is the finale version of the project. It give us the same informations as the Get_Origin_Info python files in less than 1 second.
It use a subshell by connected user to treat a large amount of users without a loss of time.

The algorithm used is similar as the python files, in fact, the optimisation is ruled by the tftp request ssh remote command (line 28).
The same output will be used to get almost all the needed informations as :
	
	* **Username**
	* **Ip address**
	* **Cisco Switch Name**
	* **Vlan Identifier**
	* **Mac address**
	* **Socket Identifier (with form Gix/y/z)**
	* **Connexion_time (in minuts)**

The last information (description of the outlet, with form N1A01-01) is extracted from a last cisco ssh remote command defined line 43.
The differents informations are extracted by a regular expression filtering defined by :

	* **Username** : *[A-Za-z0-9_-êïù]+@[A-Za-z0-9_-]+*
	* **Ip address** : *([0-9]+\\.){3}[0-9]+*
	* **Cisco Switch Name** : *balard-[0-9][A-Z]\\-[0-9]*
	* **Vlan Identifier** : *\\s[0-9]{3}\\s*
	* **Mac address** : *([0-9a-f]{4}\\.){2}[0-9a-f]{4}*
	* **Socket Identifier** : *Gi([0-9]\\/){2}[0-9]+*
	* **Connexion_time** : by the following equation *M1-M2 + (H1-H2)*60* where :

		* **H1** : *The Now date command extracted time Hours field*
		* **H2** : *The Start Connexion Time Hours field*
		* **M1** : *The Now date command extracted time Minuts field*
		* **M2** : *The Start Connexion Time Minuts field*

	* **Description** : *[NRJPASEP]+[0-9A-Z.]+\\-[0-9]+*

The main algorithm is ruled by the following steps :

	* **Get the user:ip association** from the results of the Treat_log_v2.1.sh logfile analizer script
	* **Get the ip adress** : The ip address is extracted from the Treat_log_v2.1.sh script by applying the corresponding regular expression to its output
	* **Use the ip adress to request the tftp server** : Send a request to the tftp server as a ssh session with remote command as argument : grep $ip /var/lib/tftpboot/snoop/\ where $ip contains the previous result
	* **Filter the cisco name by regular expression pattern** : The Cisco name is extracted from the tftp response by applying the corresponding regular expression
	* **Filter the Vlan identifier by regular expression pattern** : The Vlan identifier is extracted from the tftp response by applying the corresponding regular expression
	* **Filter the MAC adress by regular expression pattern** : The MAC address is extracted from the tftp response by applying the corresponding regular expression
	* **Filter the Socket name by regular expression pattern** : The Socket name is extracted from the tftp response by applying the corresponding regular expression
	* **Get origin name** : From the splitted current item (separator is ':')
	* **Get the time informations associated to the user** : Get the corresponding line in the time_list by filteering with previous name result
	* **Get the time "now"** : Get the absolute 'now' time from the command **`date +%H`":"`date +%M`**
	* **Get the "now" hours field** : Split the First field of the Now time from separator **':'**
	* **Get the "start" hours field** : Split the First field of the Start time from separator **':'**
	* **Get the "now" minuts field** : Split the Second field of the Now time from separator **':'**
	* **Get the "start" minuts field** : Split the Second field of the Start time from separator **':'**
	* **Check if user is connected** : Brownse the response of the origin ssh remote command : **/opt/Linux_FLEXnet_Server_ver_11.16.5.1/lmutil  lmstat -a -c /opt/Linux_FLEXnet_Server_ver_11.16.5.1/Licenses/Origin_20jetons.lic | grep "^.*origin\.srv-prive\.icgm\.fr/27000.*"**

		* **Use cisco and socket fields to connect the switch and get description field** : From the command **ssh ${Cisco^} "show interfaces description | i "$Socket" | tail -1"** 

			* **${Cisco^}** is the Cisco name with upper first letter
			* **$Socket** is the socket number with form **Gix/y/z**

		* **Filter the Description by regular expression pattern** : Apply the Description regular expression from the previou result
		* **Compute connexion time** : From H1, H2, M1, M2 with the equation **M1-M2 + (H1-H2)*60**

	* **Results display** : Sort the differents informations fields into a string
	* **Put in on screen** : Put them on screen OR write it in file
