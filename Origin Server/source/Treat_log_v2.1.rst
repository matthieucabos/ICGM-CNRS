Treat_log_v2.1
==============

.. code-block:: shell	

	Treat_log_v2.1.sh <mode>

_________________________________________________________________

Principe
--------

This script has been writtent to treat immediatly the logwatch file and associate to each **User ID** the correct **Ip address**.

To make it work, you have to write the logwatch file since the micro shell script and launcher.
(The orglabdebug.log file manager associating a date time to an event on the orglabdebug logfile)

It is ruled by automatic script : 

.. code-block:: shell

	date >> ./logwatch
	ss -n -t | grep 60213 >> ./logwatch
	tail -n 1 /usr/local/flexlm/orglabdebug.log >> ./logwatch

This script is lauched periodically with commands :

.. code-block:: shell

	inotifywait -q -m -e modify /usr/local/flexlm/orglabdebug.log|
	while read -r filename event; do
	 ./Script.sh       
	done

This script is ruled by the following algorithm :

* **Get the file logwatch** from the orgin server using the command **scp**

* **Cut and read Logwatch file** since the date fields (must be a daily Slice):

	* *Get day, month and year fields from the command* **date**
	* *Get the line number from the split must start with command* **grep -n**
	* *Get the number of line contained in the daily logwatch with the difference between the command* **wc -l** *result and the last one*
	* *Cut the logwatch from the end with the command* **tail**

* **Reading filtered content** to get the correct Informations

	* *Split the daily logwatch content from the day starting line and month starting line*

* **Filtering Ip and User** fields from Regular Expressions

	* *Associate an user variable to the following regular expression filtered data :* **[A-Za-z0-9_-êïù]+@[A-Za-z0-9_-]+**
	* *Associate an ip variable to the regular expression filtered data :* **([0-9]+\\.){3}[0-9]+**

* **Associate to each User Token Event an Ip list** containing all the Inforamtions since the **ss -n -t** command output

	* *Store the differents ip address from the* **ss -n -t** *command into the IP_slice list*
	* *If the current item is an User field, associate to each user an IP list using the index count*
	* *Increment the index at each user changing*

* **For each User, stored in time, Computing the Cantor Difference between the two Ip Sets.** The result is the associated IP of the current User. In fact the first IP is immediatly avaible and permit to find the others from the principle of deduction: 

	* *From the IP_list, define the first user name and the first ip address as loop starter (all the others will be deducted from the first ones)*
	* *Brownsing the array and make the absolute set difference between each stored ip address list to get the newest*
	* *The newest ip address is assigned to his respective hostname and stored into the User_IP list*
	* *Print the result to use it in another script as raw output*

The result is shown as a **user:ip** list association and is used in the **Get_Origin_Info_v2.1.py** to make it faster.

Usage
-----

Please to use with the correct syntax :

.. code-block:: shell	

	./Treat_log_v2.1.sh