# Cisco Mapping

**Author** : *CABOS Matthieu*

**Release** : *15/10/2021*

**Organisation** : *ICGM-CNRS*

______________________________________________________________________________________________________


I've been writing these Scripts for the Network Administration and Installation of the ICGM laboratory - CNRS- Montpellier FRANCE.

**Warning** All these script have been written to be executed into the own network structure of the ICGM-IBMM Network. It should be used into a different environnement **respecting the structure in any case** to make them work.

____________________________________________________________________________

# Install

To install, please launch first the Shell Script using the syntax :

**./Requirements.sh**

# Usage

To use it, you have to pass your own Cisco Switch List and Dictionnary preserving the use strucutre.
The readed 'Ordinateurs.ods' file is the DHCP Authorized list recorded in .ods file using the form :

**Hostname | Mac@ | Vlan | User**

It must be present at top level of Mapping.py :

Folder Structure::

************************************
```bash
Server Administrator Tools/
├── Mapping_Folder
│   ├── Cisco2.sh
│   ├── Cisco2Socket2.py
│   ├── Cisco2Socket.py
│   ├── Cisco2Socket.sh
│   └── Mapping.py
└── Ordinateurs.ods
 ```
     
************************************

 To get tftpboot informations, please to refer the tftp server and replace command at line 417 :
 
 *os.system('scp mcabos@tftp.srv-prive.icgm.fr:/var/lib/tftpboot/snoop/\* .')*
 
 by :
 
 *os.system('scp [user@tftp server]:/var/lib/tftpboot/snoop/\* .')*
   
 Once the Structure properly builded, please to use with the following syntax since the Mapping_Folder : 
 
 **python3 Mapping.py**
 
 It will produce a Tftpboot.ods file readable containing all the linked informations of the network.
 
   

# Support

For any support request, please mail @ matthieu.cabos@umontpellier.fr
