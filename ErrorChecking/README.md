# Cisco Error Checking

**Author** *CABOS Matthieu*

**Date** *10/2021*

**Organisation** *ICGM-CNRS*

______________________________________________________________________________________________________


I've been writing these Scripts for the Network Administration and Installation of the ICGM laboratory - CNRS- Montpellier FRANCE.

**Warning** All these script have been written to be executed into the own network structure of the ICGM-IBMM Network. It should be used into a different environnement **respecting the structure in any case** to make them work.

***************************

## Summary

This repository contain 2 main projects :
  * [**Script_del_block_user.py**](https://github.com/matthieucabos/Python-Scripts/tree/master/ICGM-CNRS/ErrorChecking#script_del_block_userpy) : Get on the *Cisco Network* all the err-disable Errors Sockets and solve it keeping a Trace.
  * [**Get_ThresholdExceeded.sh**](https://github.com/matthieucabos/Python-Scripts/tree/master/ICGM-CNRS/ErrorChecking#get_thresholdexceededsh) : Get on the *Network monitor ssh server* the threshold exceeded errors and return the associated Hardware Sockets.

***************************

## Script_del_block_user.py

The Script_del_block_user search into the full Cisco network all the err-disable errors (disconnected Users).
It works from these steps :
  * **Building Error dictionnary** since the Cisco Comandline : ```bash show interface | i err-disable ``` applied to each of the Cisco Switch
  * **Getting exact Gigait Ethernet Socket** from Error dictionnary and store them into Gb_dict Dictionnary using Regular Expression
  * **Brownsing Cisco list** and write & apply associated Cisco Commands :
      * **Command application** : ```bash sh int description | i socket_name```
      * **Cutting the command output by line**
      * **For each output line** :
         * Searching the exact Cisco Socket Description since regular expression
         * Get the exact Description and store it into the variable *Description*
      * **Writing the error History** into the **Error_list** file
      * **Resolving errors** using the associated Cisco Commands Script sent by Secured Shell


Please to use with the following syntax :

```bash
python3 Script_del_block_user.py
```

The version 2 of the project is usable on the same way and implement Multiprocessing features to optimise the execution time.
Please to use similary :

```bash
python3 Script_del_block_userv2.py
```

The version 3 implement a dynamic Processus building protocol using a unique parameter "nb_threads".
This value define the number of independants processus to treat the full dictionnary, wich is regulary splitted into the rounded divided size value.
Each slice of the dictionnary is treated by his own independant Process (using the Multiprocessing module of Python 3).

Please to use with the correct syntax :

```bash
python3 Script_del_block_userv3.py <nb_threads>
```

## Get_ThresholdExceeded.sh

This script has been written to detect on a Network Monitor all the highThresholdExceeded Errors and get the exact associated Sockets Name
To Use, please to respect the following syntax :

```bash
./Get_ThresholdExceeded.sh 
```

The Results are stored into the **Sockets.txt** File.

Please to ensure have the correct rights of connexion into the monitor to Use it.

***************************

## Support

For any support request, please to mail @ matthieu.cabos@umontpellier.fr
