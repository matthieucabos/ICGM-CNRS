Get_Origin_Info.py
==================

Version 2.1
-----------

The most efficient version using the Origin_API extension.

It write the orgin activities history containing all the DHCP extracted informations in concordance with the tftp boot server (listing only **real** connected users).

In fact, you have to use it into a similar structure as following :

.. code-block:: bash

	Origin
	├── Get_Origin_Info_v2.1.py
	├── Origin_API.py
	├── Treat_log_v2.sh
	└── Treat_tokens.sh

These actions need an efficient log file since the Origin server orglabdebug.log file.

I use a logwatch intermediate file with allocated token inserted into the token log file.

It is ruled by a shell automated script containing the following instructions: 

.. code-block:: bash

	date >> ./logwatch
	ss -n -t | grep 60213 >> ./logwatch
	tail -n 1 /usr/local/flexlm/orglabdebug.log >> ./logwatch

where **60213** is the communication port number of the Origin application.

This shell script is lauched periodically with the following linux commands.
It must be launched with the **nohup** linux command to make it write properly and permanently the logwatch file.

.. code-block:: bash

	inotifywait -q -m -e modify /usr/local/flexlm/orglabdebug.log|
	while read -r filename event; do
	 ./Script.sh       
	done


With this way of work, the orglabdebug.log file and the logwatch file will never be altered.

This script require differents ssh authorizations keys as :

* **Cisco Switch connected to the network** *(All the Balard-XY-Z switch access)*
* **tftp.srv-prive.icgm.fr** *(All the daily connected repertored users)*
* **origin.srv-prive.icgm.fr** *(The main origin server)*

With access to these ssh passerel you will be able to retrieve all the needed informations to identify and keep tracability on your Origin server.


Version 2
---------

That version is similar to the version 1. There is no display in this one but the Origin History file is properly written.
The version 2 is treating the **full daily logwatch content** and should be used at the end of a day for exemple or to verify the results of the version 2.1.

It give us the **same informations than the version 2.1** but it will display into the Origin history file **all the activities** on the **origin server**.

It must be consider as a **pre-version of version 2.1** and should be used also as a **log file analyzer**.

**Susbtitute the differents date** variables (as *day, month, year, etc*) **with a specific date** will treat the logwatch file **since this specific date**. 

This script will be used as a logwatch analizer instead of a real time analizer like the version 2.1 and it could be really interesting with **network management** and **administration tool**.

Please to use with the correct following syntax :

.. code-block:: bash

	python3 Get_Origin_Info_v2.py


Version 1
---------

This script is the full optimised and parallelized code version of the Origin Users Informations Getter.
It allow us to get since an Origin server and the tftp server repertoring connected people the full informations content since the log description to the connection time.


It uses : 

* **Treat_log_v2.sh** file to get an immediate association between user ID and their IP.
* **Treat_tokens.sh** script to get a tokens manager into your Python Code
* **Get_Connexion_Time.py** Library to get the connexion time elapsed by user.
* **Get_tftp_infos.py** Library to treat and manage a Tftp content from the server

It must be used into the equivalent environment :

.. code-block:: bash

	.
	├── dhcpd-501.conf
	├── dhcpd-510.conf
	├── dhcpd-511.conf
	├── dhcpd-512.conf
	├── dhcpd-513.conf
	├── dhcpd-514.conf
	├── dhcpd-515.conf
	├── dhcpd-516.conf
	├── dhcpd-518.conf
	├── dhcpd-519.conf
	├── dhcpd-524.conf
	├── dhcpd-525.conf
	├── dhcpd-526.conf
	├── dhcpd-528.conf
	├── dhcpd-529.conf
	├── dhcpd-530.conf
	├── dhcpd.conf
	└── Origin_Manager
	    ├── Get_Connexion_Time.py
	    ├── Get_Origin_Info.py
	    ├── Get_tftp_infos.py
	    ├── Treat_log_v2.sh
	    └── Treat_tokens.sh

This Script use the already written associated script.
The ssh sessions connections have been parallelized to make the script faster than ever.

The algorithm follow these steps in order :

* **Get the logwatch file**
* **Treat the Treat_log_v2.sh output** since regular expressions to get the correct user2ip list
* **Get the Snoop dictionnary** since the tftp server of connected people (cf  `DHCP Snooping <https://en.wikipedia.org/wiki/DHCP_snooping>`_ )
* **Get the connection time** since the *Get_Connexion_Time* library

Please to use with the correct following syntax :

.. code-block:: bash

	python3 Get_Origin_Info.py