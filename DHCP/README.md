![](https://spinati.com/wp-content/uploads/2015/03/logo-cnrs.png)

# DHCP


**Author** *CABOS Matthieu*

**Date**  *2020/2021*

**Organization** *ICGM-CNRS*

______________________________________________________________________________________________________


I've been writing these Scripts for the Network Administration and Installation of the ICGM laboratory - CNRS- Montpellier FRANCE.

**Warning** All these script have been written to be executed into the own network structure of the ICGM-IBMM Network. It should be used into a different environnement **respecting the structure in any case** to make them work.

## Summary

[1/ Script_switch.py](https://github.com/matthieucabos/ICGM-CNRS/tree/main/DHCP#script_switchpy)

[2/ dhcp2ods.py]

[3/ ods2dhcp_guest.py](https://github.com/matthieucabos/ICGM-CNRS/tree/main/DHCP#ods2dhcp_guestpy)

[4/ Ods_conf.py](https://github.com/matthieucabos/ICGM-CNRS/tree/main/DHCP#ods_confpy)

[5/ Sort_ods_table.py](https://github.com/matthieucabos/ICGM-CNRS/tree/main/DHCP#sort_ods_tablepy)

[6/ verifiy_ip.py](https://github.com/matthieucabos/ICGM-CNRS/tree/main/DHCP#verifiy_ippy)

[7/ Support](https://github.com/matthieucabos/ICGM-CNRS/tree/main/DHCP#support)

______________________________________________________________________________________________________

## Script_switch.py

This script is using the config_switch.py file to automate a DHCP server update.
It is used to update all the Cisco Informations on the server and allow new users.

Please to use with the following syntax :

```bash
python3 Script_switch.py
```

Each user have a specific field in the DHCP configuration files associated to a fixed IP adress and a fixed MAC adress.

Once each of these values informed, the dhcp configuration file is readed and these data are sent to the server.
This script has been written for and uniquely for the ICGM-CNRS laboratory, the list of Cisco Switch is associated to this laboratory.
To make it work in others Organisations, you have to adapt the Cisco List to your own Switchs Architecture.

[**top of page**](https://github.com/matthieucabos/ICGM-CNRS/tree/main/DHCP#dhcp)

## dhcp2ods.py

This script has been writtent to dress a proper and immediate DHCP dictionnary listing all the already accepted ip adresses associated to their mac address, their vlan id and vlan name.

It returns an ods file containing all the DHCP server main informations.

This utilitary script must be used on the first child level of a DHCP server (since the conf files repertory).
It must be respect the following structure : 

```bash
.
├── DHCP
│   └── dhcp2ods.py
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
└── dhcpd.conf
```

It is ruled by the following algorithm :
* **Building DHCP dictionnary** and get infos since the given IP adresses list as parameter (written as tmp file)
* **Reading raw file content** to extract informations
* **Defining Regular Expressions definitions** to treat faster as possible the dictionnary
* **Reading and filtering raw Content** since regular expressions to dress Informations Lists
* **Package lists** as an excel file content to write
* **Saving a pre-version** of the dictionnary
* **Adjusting automatic width** for columns
* **Defining layout** for the document
* **Saving file** as xlsx file (temporary excel file)
* **Convert to .ods file** and delete temporary file

[**top of page**](https://github.com/matthieucabos/ICGM-CNRS/tree/main/DHCP#dhcp)

## ods2dhcp_guest.py

This script was written to meet the requirements of a Guest subnet in a science lab (ICGM-CNRS).
It use the DHCP Protocol, in force in this establishment.


The script must be used in a correct environment with an associated **Invites.ods** file.

```bash
.
├── Invites.ods
└── ods2dhcp_guest.py
```


The algorithm is ruled by the following steps :
* **Initialization of the Guest vlan**: *We initialize the Guest vlan with the associated information (id, IP addresses, etc.)*
* **We start by rereading the old associations**: *As part of a simple update of the DHCP server, the old mac: ip associations are kept and only the last available ip address is retrieved*
* **We browse the conf file of vlan 519**: *We identify the already existing associations*
* **We read the Invites file**: *We read the Guests file to know the mac addresses of each guest*
* **We browse the content of the file read**: *We read the content line by line by retrieving the date and address information in variables.*
* **If the current date is between the arrival date and the departure date**: *The date management and comparison is carried out from the python datetime module, we only add the guest computer if the current date is between the date arrival and departure date.*
* **We add the guest to the guest network**
* **We update the DHCP information fields**: *We add the guest computer by updating the DHCP fields concerned*
* **Either the computer is already known and we keep its IP**: *If the mac: ip association exists and is valid, it is kept*
* **Either we add one**: *Otherwise we create a new association*
* **We write the information in the dhcpd-519.conf file (the DHCP Guest server)**: *We write all the DHCP fields in the configuration file*


Please to use with the correct syntax and associated files as below :

```bash
python3 ods2dhcp_guest.py
```

[**top of page**](https://github.com/matthieucabos/ICGM-CNRS/tree/main/DHCP#dhcp)

## Ods_conf.py

This Script read a file called in our organization Ordinateurs.ods containing following informations into a table with form :

**Hostname | MAC @ | Username | Comments**

Once readed, the script read again the DHCP conf file and will allow a new user without updating each of the fields of the DHCP configuration files.
I mean it will not modify the already allocated fixed Ip @.

Please to use carefully, in fact, you can update the full DHCP server once a day (for example at night).

It should be used on an exceptional basis where the DHCP authorisation is absolutely necessary without already connected users disconnected for few seconds.

This script use following functions.

### switch

Defining a C-like switch function from a dictionnary with following call syntax.

```python
switch(my_value_to_switch,
case_1,Value_1,
case_2,Value_2,
case_3,Value_3,
case_4,Value_4)
```

Where Value is the associated action to the case_n value stored in my_value variable.
Value_n should be a function name in case of multiple instructions.

### find_first_avaible_ip

Brownsing the Already allocated DHCP fixed ip adress and restitute the first avaible IP on the associated vLan.

Please to use with the following syntax :

```python
find_first_avaible_ip(vLan)
```

### ip_data_getter

Read the DHCP configuration file to build an ip2MAC adresses dictionnary.
Once done, it will restitute the builded dictionnary.

[**top of page**](https://github.com/matthieucabos/ICGM-CNRS/tree/main/DHCP#dhcp)

## Sort_ods_table.py

This script has been written to sort already populated Ods table files.
This script sort big data arrays (for example a routing table...)
To use it, please to respect the following syntax :

```bash
python3 sort_ods_table.py <name_file> <dest_name_file> <column_to_sort> 
```

Where:
* **name_file** : Designate the .ods file name to read
* **dest_name_file** : Designate the .ods destination file name to write
* **column_to_sort** : Designate the Column considered as Sorter Reference

[**top of page**](https://github.com/matthieucabos/ICGM-CNRS/tree/main/DHCP#dhcp)

## verifiy_ip.py

This script read the DHCP Configuration files and search for any Values Duplication as IP @ and MAC @.

Please to use with the following syntax directely into your DHCP configuration Folder (on the server):

```bash
python3 verifiy_ip.py
```

[**top of page**](https://github.com/matthieucabos/ICGM-CNRS/tree/main/DHCP#dhcp)

It returns the number of duplication, if founded

## Support

For any Support request, please to mail @ **matthieu.cabos@umontpellier.fr**
