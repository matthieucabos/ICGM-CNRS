Get_User_Info_From_IP_v2
========================

This script is the optimised version of the Origin_Users.py script.

It uses the **Treat_log_v2.sh** file to get an immediate association between user ID and their IP.

Since the two first versions, the optimised version is ruled differently from the first one :

* **Cut logfile** since the date (today as default)
* **Read and extract informations** from the logwatch file with the associated *Treat_log_v2.sh* Scripot
* **Open, read & Treat the logwatch** file :

  * **Getting IP list** associated to a timed & named token. The resultys are stored by time order, arbitrary indexed from 1 -> n
  * **Getting host ID** from the full Origin user name (with form name@host) => Allow multiple users sessions on the same host
  * **Compute the Cantor difference** between two adjacents set (indexed +- 1) to get the User's associated IP

* **Building DHCP dictionnary** and get infos since the given IP adresses list as parameter :

  * **Building DHCP Dictionnary**
  * **Updating Users Dictionnary** since the DHCP dictionnary from the ip correspondance (as key entry of the Users dictionnary)
  * **Updating the Users Dictionnary** since the Cisco output command : ssh <Cisco_name> 'show mac address' to get the associated cisco switch ID and the gigabit ethernet ID

* **Finaly write the RAM stored informations dictionnary** into the Origin_history file

Please to use with the correct syntax :

.. code-block:: bash

  python3 Get_User_Info_From_IP_v3.py


The script must be used into an equivalent environment structure :

.. code-block:: bash

  .
  ├── DHCP
  │   └── Get_User_Info_From_IP_v3.py
  └── dhcpd-vlan_i.conf
  └── dhcpd-vlan_i+1.conf
  .
  .
  .
  └── dhcpd-vlan_n.conf


The result is shown with the following syntax :

.. code-block:: bash

  {'mac': '90b1.1ca3.3575', 'ip': '10.14.18.145', 'hostname': '"BBBAACCC"', 'departement': 'DPT4', 'vlan': 513, 'cisco': 'Balard-PAC-2', 'socket': '1/0/36', 'Description': 'RJLG07-01', 'origin_name': 'c2mstud@c2mstud3-pc', 'connexion time': '198.3088238040606 min'}


With :

====================== ===================== =============================================================================================
**Field Identifier**   **Data Type**          **Description**                                                                           
**mac**                *Hexadecimal string*    *The full mac address of the current User*                                                
**ip**                 *Decimal string*        *The full fixed IP from the origin server*                                                 
**hostname**           *String*                *The Hostname from the DHCP server (could be different from the Origin server Hostname)*  
**departement**        *String*                *The departement description section*                                                     
**vlan**               *Integer*               *The sub-network lan Identifier*                                                          
**cisco**              *String*                *The Cisco Switch Identifier Name*                                                        
**socket**             *Decimal String*        *The associated Gigabit Ethernet socket (with form **x/y/z**)*                            
**Description**        *String*                *The associated outlet exact name (as it is written in a Cisco Switch)*                   
**origin_name**        *String*                *The Origin User's avatar name*                                                           
**connexion time**     *Float*                 *If still connected, the connection time of the User, else the starting connection time*  
====================== ===================== =============================================================================================

Finally written into the Origin_history file into the **origin.srv-prive.icgm.fr** server.