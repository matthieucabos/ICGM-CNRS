![](https://spinati.com/wp-content/uploads/2015/03/logo-cnrs.png)

# Origin Server


**Author** *CABOS Matthieu*

**Date**  *2021/2022*

**Organization** *ICGM-CNRS*

______________________________________________________________________________________________________

These Scripts have been written to manage properly an Origin Server (See [*Origin*](https://ritme.com/software/origin/) )

It is adapted to the Origin ssh platform (reading and treating **opt/Linux_FLEXnet_Server_ver_11.16.5.1/Licenses** and **/usr/local/flexlm/orglabdebug.log**
wich are the Licence File and the Tokens Log file.

These scripts require two main extension :

* **netmiko** : *Automate the authentified ssh session*
* **pyexcel** : *Treat and write ods and excel files*

These scripts need a ssh session access into the origin server (with form origin.domain.fr)

The associated documentation may be founded [**here**](https://github.com/matthieucabos/ICGM-CNRS/raw/main/Origin%20Server/origin_server.pdf) or by html generation using the command :

```bash
make html
```

These main scripts have been written to automate the DHCP Informations retrievment and Origin Server essentials informations : 

[1/ Get_Origin_Info_v2.1.sh](https://github.com/matthieucabos/ICGM-CNRS/tree/main/Origin%20Server#get_origin_info_v21sh)

[2/ Origin_API.py](https://github.com/matthieucabos/ICGM-CNRS/tree/main/Origin%20Server#origin_apipy)

[3/ Get_Origin_Info.py](https://github.com/matthieucabos/ICGM-CNRS/tree/main/Origin%20Server#get_origin_infopy)

[4/ Get_User_Info_From_IP_v2.py](https://github.com/matthieucabos/ICGM-CNRS/tree/main/Origin%20Server#get_user_info_from_ip_v3py)

[5/ Treat_log_v2.sh](https://github.com/matthieucabos/ICGM-CNRS/tree/main/Origin%20Server#treat_log_v2sh)

[6/ Origin_Users.py](https://github.com/matthieucabos/ICGM-CNRS/tree/main/Origin%20Server#origin_userspy)

[7/ Get_Connexion_Time.py](https://github.com/matthieucabos/ICGM-CNRS/tree/main/Origin%20Server#get_connexion_timepy)

[8/ Treat_tokens.sh](https://github.com/matthieucabos/ICGM-CNRS/tree/main/Origin%20Server#treat_tokenssh)

[9/ Support](https://github.com/matthieucabos/ICGM-CNRS/tree/main/Origin%20Server#support)

___________________________________________________________________________________________________

## Get_Origin_Info_v2.1.sh

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

[**Top of Page**](https://github.com/matthieucabos/ICGM-CNRS/tree/main/Origin%20Server#origin-server)

## Origin_API.py

### Since version 2

This update contains following modificaton :
* **Get connexion time rewritted**
* **Merged sections** :
   *  *Get Connexion Time Section*
   *  *Get Connected Users Section*

The two sections have been merged to optimise the execution time storing the Conneceted users and elapsed connection time in the same dictionnary using only one ssh authentified session.

### Since version 1

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
```bash
from Origin_API import *
```

[**Top of Page**](https://github.com/matthieucabos/ICGM-CNRS/tree/main/Origin%20Server#origin-server)
___________________________________________________________________________________________________

## Get_Origin_Info.py

### Since shell version

The shell version of the script give us the same results as the python ones.
Please to use with the following syntax :

```bash
./Get_Origin_Info.sh
```

### Since Version 2.2

The update concern the used versions of Origin_API (the version 2 will be used here) and the Treat_log script (the version 2.1 will be used here).
Once the newest extensions loaded, the results are treated in real time and the execution time is about 20 seconds.

### Since Version 2.1

The most efficient version using the Origin_API extension.

It write the orgin activities history containing all the DHCP extracted informations in concordance with the tftp boot server (listing only **real** connected users).

In fact, you have to use it into a similar structure as following :
```bash
Origin
├── Get_Origin_Info_v2.1.py
├── Origin_API.py
├── Treat_log_v2.sh
└── Treat_tokens.sh
```

These actions need an efficient log file since the Origin server orglabdebug.log file.
I use a logwatch intermediate file with allocated token inserted into the token log file.
It is ruled by a shell automated script containing the following instructions: 

```bash
date >> ./logwatch
ss -n -t | grep 60213 >> ./logwatch
tail -n 1 /usr/local/flexlm/orglabdebug.log >> ./logwatch
```
where 60213 is the communication port of the Origin application.

This shell script is lauched periodically with the following linux commands.
It must be launched with the **nohup** linux command to make it write properly and permanently the logwatch file.

```bash
inotifywait -q -m -e modify /usr/local/flexlm/orglabdebug.log|
while read -r filename event; do
 ./Script.sh       
done
```

With this way of work, the orglabdebug.log file and the logwatch file will never be altered.

This script require differents ssh authorizations keys as :
   * **Cisco Switch connected to the network** *(All the Balard-XY-Z switch access)*
   * **tftp.srv-prive.icgm.fr** *(All the daily connected repertored users)*
   * **origin.srv-prive.icgm.fr** *(The main origin server)*

With access to these ssh passerel you will be able to retrieve all the needed informations to identify and keep tracability on your Origin server.

### Since Version 2

That version is similar to the first one. There is no display in this one but the Origin History file is properly written.


Please to use with the correct following syntax :
```bash
python3 Get_Origin_Info_v2.py
```

### Since Version 1

This script is the full optimised and parallelized code version of the Origin Users Informations Getter.
It allow us to get since an Origin server and the tftp server repertoring connected people the full informations content since the log description to the connection time.


It uses : 
* **Treat_log_v2.sh** file to get an immediate association between user ID and their IP.
* **Treat_tokens.sh** script to get a tokens manager into your Python Code
* **Get_Connexion_Time.py** Library to get the connexion time elapsed by user.
* **Get_tftp_infos.py** Library to treat and manage a Tftp content from the server

It must be used into the equivalent environment :

```bash
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
```
This Script use the already written associated script.
The ssh sessions connections have been parallelized to make the script faster than ever.

The algorithm follow these steps in order :
* **Get the logwatch file**
* **Treat the Treat_log_v2.sh output** since regular expressions to get the correct user2ip list
* **Get the Snoop dictionnary** since the tftp server of connected people (cf [**DHCP Snooping**](https://en.wikipedia.org/wiki/DHCP_snooping))
* **Get the connection time** since the *Get_Connexion_Time* library

Please to use with the correct following syntax :
```bash
python3 Get_Origin_Info.py
```

[**Top of Page**](https://github.com/matthieucabos/ICGM-CNRS/tree/main/Origin%20Server#origin-server)

___________________________________________________________________________________________________

## Get_User_Info_From_IP_v2.py

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

```bash
python3 Get_User_Info_From_IP_v3.py
```

The script must be used into an equivalent environment structure :

```bash
.
├── DHCP
│   └── Get_User_Info_From_IP_v3.py
└── dhcpd-vlan_i.conf
└── dhcpd-vlan_i+1.conf
.
.
.
└── dhcpd-vlan_n.conf
```

The result is shown with the following syntax :

```bash
{'mac': '90b1.1ca3.3575', 'ip': '10.14.18.145', 'hostname': '"BBBAACCC"', 'departement': 'DPT4', 'vlan': 513, 'cisco': 'Balard-PAC-2', 'socket': '1/0/36', 'Description': 'RJLG07-01', 'origin_name': 'c2mstud@c2mstud3-pc', 'connexion time': '198.3088238040606 min'}
```

With :


| **Field Identifier** | **Data Type**      | **Description**                                                                           |
|----------------------|--------------------|-------------------------------------------------------------------------------------------|
| **mac**              | Hexadecimal string | *The full mac address of the current User*                                                |
| **ip**               | Decimal string     | *The full fixed IP from the origin server*                                                | 
| **hostname**         | String             | *The Hostname from the DHCP server (could be different from the Origin server Hostname)*  |
| **departement**      | String             | *The departement description section*                                                     |
| **vlan**             | Integer            | *The sub-network lan Identifier*                                                          |
| **cisco**            | String             | *The Cisco Switch Identifier Name*                                                        |
| **socket**           | Decimal String     | *The associated Gigabit Ethernet socket (with form **x/y/z**)*                            |
| **Description**      | String             | *The associated outlet exact name (as it is written in a Cisco Switch)*                   |
| **origin_name**      | String             | *The Origin User's avatar name*                                                           |
| **connexion time**   | Float              | *If still connected, the connection time of the User, else the starting connection time*  |

Finally written into the Origin_history file into the **origin.srv-prive.icgm.fr** server.

[**Top of Page**](https://github.com/matthieucabos/ICGM-CNRS/tree/main/Origin%20Server#origin-server)

## Treat_log_v2.sh

### Since Version 2.1

This update concern the user with few tokens to be treated as well as others.
One only token is now enough to find the ip address.

### Since version 2

This script has been writtent to treat immediatly the logwatch file and associate to each User ID the correct Ip address.
To make it work, you have to write the logwatch file since the micro shell script and launcher from Get_User_Info_From_IP_v3.py
(The orglabdebug.log file manager associating a date time to an event on the orglabdebug logfile)

It is ruled by automatic script : 

```bash
date >> ./logwatch
ss -n -t | grep 60213 >> ./logwatch
tail -n 1 /usr/local/flexlm/orglabdebug.log >> ./logwatch
```
This script is lauched periodically with commands :

```bash
inotifywait -q -m -e modify /usr/local/flexlm/orglabdebug.log|
while read -r filename event; do
 ./Script.sh       
done
```
This script is ruled by the following algorithm :
* **Cut and read Logwatch file** since the date fields (must be a daily Slice)
* **Reading filtered content** to get the correct Informations
* **Filtering Ip and User** fields from Regular Expressions
* **Associate to each User Token Event an Ip list** containing all the Inforamtions since the ss -n -t command
* **For each User, stored in time, Computing the Cantor Difference between the two Ip Sets.** The result is the associated IP of the current User. In fact the first IP is immediatly avaible and permit to find the others from the principle of deduction.

The result is shown as a user:ip list and is used in the **Get_User_Info_From_IP_v3.py** to make it faster.

Please to use with the correct syntax :

```bash
./Treat_log_v2.sh
``` 
 [**Top of Page**](https://github.com/matthieucabos/ICGM-CNRS/tree/main/Origin%20Server#origin-server)
 
## Origin_Users.py

### From Version 1

This script is used to get a full repertory of connected Users on the [*Origin*](https://fr.wikipedia.org/wiki/Origin_(logiciel)) server of the ICGM laboratory.
It use the Licence informations to write the proper Connection history file.

To make it, the algorithm follow these steps below :
* **Initialisation** : *Variables definition to store the temporary infos*
* **Getting Users acount informations since the top level** : *Using the os.getenv function, I get the ssh needed informations to connect*
* **Connecting an ssh session to the origin.srv-prive.icgm.fr server** : *Starting an ssh session with netmiko*
* **Getting users list Informations** : *Getting the connected users informations since Origin's jetons*
* **Getting the Port Informations** : *Getting the port numbers informations since the* ```netstat -anp ```
* **Getting the raw IP list informations** : *Getting and treating the IP list informations since the* ```ss -n -t``` *command*
* **Getting the raw hostname list Informations** : *Getting and treating Port numbers informations since the* ```ss -n -t -r``` *command*
* **Exit the ssh session and read the Ordinateurs.ods file** : *Close the current session with netmiko*
* **Updating the Origin_history file since the newest Informations** : *Updating history with the command*
```bash 
scp ./Origin_history <user>@origin.srv-prive.icgm.fr
```

### From Version 2 :

These actions need an efficient log file since the Origin server orglabdebug.log file.
I use a logwatch intermediate file with allocated token inserted into the token log file.
It is ruled by automatic script : 

```bash
date >> /tmp/logwatch
ss -n -t | grep 60213 >> /tmp/logwatch
tail -n 1 /usr/local/flexlm/orglabdebug.log >> /tmp/logwatch
```
This script is lauched periodically with commands :

```bash
inotifywait -q -m -e modify /usr/local/flexlm/orglabdebug.log|
while read -r filename event; do
 bin/script.sh       
done
```
Once the logwatch file properly instanced, I read it and treat informations since the token allocations.
The intermediate algorithm is ruled by following steps :

* **Cut logfile** since the date (today as default)
* **Read** the log file
* **Treat Log file content** since regular expression to get 
  * *IP_@ list*
  * *New user information*
* **Associate a new user** to the difference between 2 log slice
* **Compute the Set Cantor difference** by User ID
* **Get the real (most susceptible one) IP_@** from user name

Once these informations found, there are linked to the already existing database since the IP adress to obtain the exact Elapsed connection time and the exact login name foreach user.

The result is shown with the following syntax :

```bash
<Switch Cisco Name> | <Vlan Number> <MAC_@> <Cisco Socket> | <Hostname> | <Departement> | <Ip_@> | <Socket Description> | <User login> | <Time Elapsed>
```
Finally written into the Origin_history file into the **origin.srv-prive.icgm.fr** server.

Please to use this script with the correct syntax (and the latest version):

```bash
python3 Origin_Users_parallelisation_v2.py
```

The script must be used into an equivalent environment structure :

```bash
.
├── DHCP
│   └── Origin_Users.py
└── Ordinateurs.ods
```

Where Ordinateurs.ods is the DHCP authorisation list table with form :

```bash
<Hostname> | <MAC_@> | <Vlan> | <Relative Informations>
```

[**Top of Page**](https://github.com/matthieucabos/ICGM-CNRS/tree/main/Origin%20Server#origin-server)

## Get_Connexion_Time.py

This script allow to get the daily Connexion Time Dictionnary sorted by User.

It use the associated **Treat_tokens.sh** to get immediate shell values from the logfile.

The algorithm is ruled by the following steps :
* **Building Timestamp Dictionnary** to compute the connection time
* **Reading the results of the Treat_tokens.sh script**
* **Sort and Store** them into lists
* **Initialising Dictionnaries**
* **Populate Dictionnaries**
* **Computing the connection time** since the first OUT token and the last IN token

The last Data Structure is a dictionnary, linkable with the rest of the informations.

Please to use with the correct syntax :

```bash
python3 Get_Connexion_Time.py
```
[**Top of Page**](https://github.com/matthieucabos/ICGM-CNRS/tree/main/Origin%20Server#origin-server)

## Treat_tokens.sh

### Principe

The Treat_tokens.sh script has been writtent to automate the Tokens Management into an Origin Server :

* *Each User take an **OUT** token to start a working session.*
* *Each OUT token will be followed by an IN token, the last emitted IN token sign the closure of the connection*
* *Each Token is associated to a name and a time*

You have to Dress a *"Token map"* of the already distributed tokens.
To do so, see the followings methods :

* **Get the immediate Content of the daily logwatch file** *(generated with the same nohup script auto sheduled than the first Script)*
* **Get the raw Token list** associating User ID and the time field
* **Sorting tokens** by Type (IN or OUT)
* **Associate to each token an User ID** or Hostname (filtered by regular expressions)
* **Associate to each token the correct Timestamp**
* **Treat the input** entries as a switch

### Usage

Please to use with the correct syntax :

```bash
./Treat_tokens.sh <mode>
```

where mode balance between :

* **1** : *Get the IN tokens*
* **2** : *Get the OUT tokens*
* **3** : *Get the IN Tokens Hostname*
* **4** : *Get the OUT Toekns Hostname*
* **5** : *Get the IN Tokens Timestamp Sorted List*
* **6** : *Get the OUT Tokens Timestamp Sorted List*

[**Top of Page**](https://github.com/matthieucabos/ICGM-CNRS/tree/main/Origin%20Server#origin-server)

## Support

For any Support request, please to mail @ **matthieu.cabos@umontpellier.fr**
