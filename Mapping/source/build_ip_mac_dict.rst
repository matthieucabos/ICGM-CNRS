build_ip_mac_dict
=================

.. code-block:: python

	def build_ip_mac_dict(tftp_Content):

_________________________________________________________________

**Algorithm**
-------------

Building Ip 2 @Mac dictionnarry from tftp boot server files (connected people).
We are getting the full connected Users Mac => IP dictionnary using regular expression :

	* **[0-9a-z]{4}\\.[0-9a-z]{4}\\.[0-9a-z]{4}**  : Give us the MAC adress since the tftpboot files
	* **([0-9]\\/){2}[0-9]***  : Give us the Hardware Cisco Port Number since the tftpboot files 
	* **\\d+\\.\\d+\\.\\d+\\.\\d+** : Give us the IP Adress since the tftpboot files

=============== ========== ===============================
**Parameters**   **Type**   **Description**
*tftp_Content*   string     The tftpboot file raw content
=============== ========== ===============================

:Returns: Dictionnary : The dictionnary with ip/mac correspondance 

_________________________________________________________________

**Source Code**
---------------

.. code-block:: python

	ip2mac={}
	MAC=""
	regex = r"[0-9a-z]{4}\.[0-9a-z]{4}\.[0-9a-z]{4}"
	regex2=r"([0-9]\/){2}[0-9]*"
	ip=re.compile(r'\d+\.\d+\.\d+\.\d+')
	for line in tftp_Content:
		matches = re.finditer(regex, line, re.MULTILINE)
		res_ip=ip.match(line)
		for matchNum, match in enumerate(matches, start=1):
			if (not res_ip == None):
				MAC=match.group()[0:2]+":"+match.group()[2:4]+":"+match.group()[5:7]+":"+match.group()[7:9]+":"+match.group()[10:12]+":"+match.group()[12:14]
		matches = re.finditer(regex2, line, re.MULTILINE)
		for matchNum, match in enumerate(matches, start=1):
			GiPort=str(match.group())
			if (not res_ip == None):
				ip2mac[MAC]=(res_ip.group(0),GiPort)
	return ip2mac