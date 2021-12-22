# SNMP

**Author** : *CABOS Matthieu*

**Release** : *15/10/2021*

**Organisation** : *ICGM-CNRS*

______________________________________________________________________________________________________


I've been writing these Scripts for the Network Administration and Installation of the ICGM laboratory - CNRS- Montpellier FRANCE.

**Warning** All these script have been written to be executed into the own network structure of the ICGM-IBMM Network. It should be used into a different environnement **respecting the structure in any case** to make them work.

______________________________________________________________________________________________________

## Summary

[1/ Cisco2.sh](https://github.com/matthieucabos/ICGM-CNRS/tree/main/SNMP#cisco2sh)

[2/ Cisco2Socket.py](https://github.com/matthieucabos/ICGM-CNRS/tree/main/SNMP#cisco2socketpy)

[3/ Cisco2Socket2.py](https://github.com/matthieucabos/ICGM-CNRS/tree/main/SNMP#cisco2socket2py)

[4/ Get10GSocket.sh](https://github.com/matthieucabos/ICGM-CNRS/tree/main/SNMP#get10gsocketsh)

[5/ Script_sheduler.sh](https://github.com/matthieucabos/ICGM-CNRS/tree/main/SNMP#script_shedulersh)

[6/ Script_sheduler2.sh](https://github.com/matthieucabos/ICGM-CNRS/tree/main/SNMP#script_sheduler2sh)

[7/ Switch_info_getter.py](https://github.com/matthieucabos/ICGM-CNRS/tree/main/SNMP#switch_info_getterpy)

[8/ Support](https://github.com/matthieucabos/ICGM-CNRS/tree/main/SNMP#support)


## Cisco2.sh


### Usage

Please to Use of script Cisco.sh with the following syntax :

```bash
./Cisco.sh <@IP Switch Cisco> <mode>
```

where :
* **@IP Switch** is the exact IP adress of the switch to analyse
* **mode** define the way of execution between :
  * **1** : Get the Gigabit Interface from the Cisco Port Number
  * **2** : Get the Cisco Port Number from the Gigabit triolet

[**Top of Page**](https://github.com/matthieucabos/ICGM-CNRS/tree/main/SNMP#snmp)

## Cisco2Socket.py

### Usage

Please to Use of script Cisco2Socket.py with the following syntax :

```bash
python3 Cisco2Socket.py <Switch Cisco Name> 
```
where **Switch Cisco Name** is the exact Name of the Cisco Switch to analyse.

The following input is the Socket name (with form N1A01-01) and the output is a Cisco Gigabit triolet with form 1/0/11

[**Top of Page**](https://github.com/matthieucabos/ICGM-CNRS/tree/main/SNMP#snmp)

## Cisco2Socket2.py

### Usage

Getting the exact Room Socket Name from the GigabitEthernet Triolet provided by Cisco informations.

Please to Use of script Cisco2Socket2.py with the following syntax :

```bash
python3 Cisco2Socket2.py <@IP of the switch> <Cisco Gigabit Triolets>
```
where :
  * **@IP of the switch** is the exact Ip adress of the switch to analyse
  * **Cisco Gigabit Triolets** is the exact Cisco Gigabit Triolet to search (with form 1/0/1)

It give a List containing all the Room Socket Exact Name

[**Top of Page**](https://github.com/matthieucabos/ICGM-CNRS/tree/main/SNMP#snmp)

## Get10GSocket.sh


### Usage

Get 10Gb Socket Transfered Octets Round Robin Database and draw the associated graph

Please to Use of script Get10GSocket.sh with the following syntax :

```bash
./Get10GSockets.sh <@IP of the switch> <Number of samples>
```

where :
  * **@Ip of the switch** is the exact Ip adress of the switch to analyse
  * **Number of samples** is the exact number of sampled value from SNMP to populate .rdd files
 
The associated graph .png will appear in the current folder with its associated .rdd file.

The standard number of samples value for this script is arround 200.

[**Top of Page**](https://github.com/matthieucabos/ICGM-CNRS/tree/main/SNMP#snmp)

## Script_sheduler.sh

### Usage

Get Socket Transfered Octets and Errors amount Round Robin Database and draw the associated graphs using SNMP.

Please to Use of script Script_sheduler.sh with the following syntax :
```bash
./Script_sheduler.sh <@IP of the switch> <Number of samples>
```

where :
  * **@Ip of the switch** is the exact Ip adress of the switch to analyse
  * **Number of samples** is the exact number of sampled value from SNMP to populate .rdd files

It will get **Number of samples** point values and update Round Robin Archive and associated graph

The standard number of samples value for this script is arround 200.

[**Top of Page**](https://github.com/matthieucabos/ICGM-CNRS/tree/main/SNMP#snmp)

## Script_sheduler2.sh

### Usage

Updated version of Script_sheduler using snmp and get ransfered Octets, Errors and 10Gb Transfert Octets into Round Robin Database and draw the associated graphs.


Please to Use of script Script_sheduler2.sh with the following syntax :
```bash
./Script_sheduler2.sh <@IP of the switch> <Number of samples>
```
where :
  * **@Ip of the switch** is the exact Ip adress of the switch to analyse
  * **Number of samples** is the exact number of sampled value from SNMP to populate .rdd files

It will get **Number of samples** point values and update Round Robin Archive and associated graph

The standard number of samples value for this script is arround 200.

[**Top of Page**](https://github.com/matthieucabos/ICGM-CNRS/tree/main/SNMP#snmp)

## Switch_info_getter.py

It is the main SNMP samples getter of the Script sheduler script.

It permit to get multiples values since a SNMP command.

Associated to a script sheduler to update Round Robin Archive, it allow to draw RRD graph and integrate them into an openNMS interface.


Please to Use of script Switch_info_getter.py with the following syntax :

```bash
python3 Switch _info_getter.py <@IP of the switch>
```

Where the parameter is the IP of the switch to analyse.

[**Top of Page**](https://github.com/matthieucabos/ICGM-CNRS/tree/main/SNMP#snmp)

## Support

For any support request, please to mail @ matthieu.cabos@umontpellier.fr
