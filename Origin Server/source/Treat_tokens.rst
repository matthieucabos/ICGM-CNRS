Treat_tokens
============

.. code-block:: shell	

	Treat_tokens.sh <mode>

_________________________________________________________________

Principe
--------

To use the Treat_tokens.sh script, you have to already instanced the **nohup** automated script to read and analyze the logwatch file.
The logwatch file must be contained into the same folder than the script.

The Treat_tokens.sh script has been writtent to automate the Tokens Management from an Origin Server log file:

* Each User take an **OUT** token to start a working session.
* Each **OUT** token will be followed by an **IN** or **OUT** token, the last emitted **IN** or **OUT** token sign the closure of the connection
* Each Token is associated to a **hostname** and a **timestamp**
* Each connected **user is managed by tokens** during his session
* Each tokens allocation and restitution is stored into the **orglabdebug.log** file

I am Dressing a *"Token map"* or *"Token array"* of the already distributed tokens.

To do so, see the followings methods :

* **Get the immediate Content of the daily logwatch file** *(generated with the same nohup script auto sheduled than the first Script)* : 

	* *Get day, month and year fields from the command date*
	* *Get the line number from the split must start with command* **grep -n**
	* *Get the number of line contained in the daily logwatch with the difference between the command* **wc -l** *result and the last one*
	* *Cut the logwatch from the end with the command* **tail**

* **Get the raw Token list** associating User ID and the time field :

	* *Brownse the daily logwatch content*
	* *Filter by regular expressions line by line to get the following fields :*

		* **Tokens (IN and OUT)**
		* **Associated Hostnames (for both of them)**
		* **Exact Date-Time field**

* **Sorting tokens** by Type (IN or OUT):

	* *Converting the Date-Time field to timestamp using the command* **date -d**
	* *Switch the mode as parameter 1*

* **Treat the input** entries as a switch

	* *Differents mode filter differents results from the same list using regular expression*

* **Associate to each token an User ID** or Hostname (filtered by regular expressions):

	* *Keeping in the same order the tokens list and the hostname list*

* **Associate to each token the correct Timestamp**:

	* *From the timestamp conversion, print the correct timestamp associated to a token*

Usage
-----


Please to use with the correct syntax :

.. code-block:: shell	
	
	./Treat_tokens.sh <mode>


where mode balance between :

* **1** : *Get the IN tokens*
* **2** : *Get the OUT tokens*
* **3** : *Get the IN Tokens Hostname*
* **4** : *Get the OUT Toekns Hostname*
* **5** : *Get the IN Tokens Timestamp Sorted List*
* **6** : *Get the OUT Tokens Timestamp Sorted List*