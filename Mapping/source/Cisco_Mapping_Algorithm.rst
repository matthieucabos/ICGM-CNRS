Cisco_Mapping_Algorithm
=======================

**Algorithm**
-------------

Welcome to the Cisco Mapping Source Code documentation.
This code has been provided to manage informations from Cisco Switch (as number of connected people, with their associated informations).
It should be used to Administrate a DHCP server using Tftpboot to store Connected Users informations.
A DHCP server is ruled by mac adresses, each fixed ip adress have one and only one associated mac adress.
The DHCP server provide to Authorised Users the full network access. A non-authorised hostname won't get any access on the network.

The used algorithm is ruled by the followings steps :
	* **Getting infos from the Tftpboot server** : We get the stored informations since the Tftp server (stored in the /var/lib/tftpboot/snoop/ folder)
	* **Building IP:MAC dict** : We build the dictionnary of the ip adresses associated to the hardware mac adresses of the connected users
	* **Brownsing ods file** : We read the Configuration ods file containing Hostnames, Mac adresses, Vlan informations, and comments
	* **Searching current mac in @MAC database and updating Dictionnary Fields** : We populate the Final dictionnary with the form : Hostname | @mac | Vlan Id | @ip | switch name | switch @ip | Port number | Switch Gigabit informations |  Socket Number | Comments
	* **Updating Comments Field** : We update the Comments Fields from the Configuration ods file
	* **Updating Room Sockets Names Field** : We update The Socket Number fields using the Cisco *show interface description* command
	* **Building the not-conected Dictionnarry** : We build as a second Sheet the non-connected authorised Users of the DHCP Server
	* **Packaging as array to write** : We package these arrays to be wrote into an ods file
	* **Saving ods file** : We save the Raw Content generated by the script into the output ods file.
	* **Setting Ods Document Layout** : Using the openpyxl API, we apply a parametered Layout

All these steps of the algorithm have been released using the following functions.
Each of these one have been explained into a specific paragraph.

_________________________________________________________________

**Source Code**
---------------

.. code-block:: python

	# switch_dict=sys.argv[1]
	# switch_dict2=sys.argv[2]
	# Cisco_list=sys.argv[3]

	switch_dict={
	'balard-1D-1':'10.14.0.49',
	'balard-1G-1':'10.14.0.51',
	'balard-2D-1':'10.14.0.58',
	'balard-2G-1':'10.14.0.60',
	'balard-2H-1':'10.14.0.62',
	'balard-3D-1':'10.14.0.67',
	'balard-3G-1':'10.14.0.69',
	'balard-3G-2':'10.14.0.70',
	'balard-4C-1':'10.14.0.74',
	'balard-4D-1':'10.14.0.76',
	'balard-4G-1':'10.14.0.78',
	'balard-4H-1':'10.14.0.80',
	'balard-SRV':'10.14.0.20',
	'balard-SRV-SUP':'10.14.0.21',
	'balard-srv-cines':'10.14.0.30',
	'balard-sup-cines':'10.14.0.31'
	}

	switch_dict2={
	'10.14.0.49':'Balard-1D-1',
	'10.14.0.51':'Balard-1G-1',
	'10.14.0.58':'Balard-2D-1',
	'10.14.0.60':'Balard-2G-1',
	'10.14.0.62':'Balard-2H-1',
	'10.14.0.67':'Balard-3D-1',
	'10.14.0.69':'Balard-3G-1',
	'10.14.0.70':'Balard-3G-2',
	'10.14.0.74':'Balard-4C-1',
	'10.14.0.76':'Balard-4D-1',
	'10.14.0.78':'Balard-4G-1',
	'10.14.0.80':'Balard-4H-1',
	'10.14.0.20':'Balard-SRV',
	'10.14.0.21':'Balard-SRV-SUP',
	'10.14.0.30':'Balard-SRV-CINES',
	'10.14.0.31':'Balard-SUP-CINES'
	}

	Cisco_list=[
	'Balard-EP-1',
	'Balard-PAC-1',
	'Balard-PAC-2',
	'Balard-RDC-1',
	'Balard-1C-1',
	'Balard-1D-1',
	'Balard-1G-1',
	'Balard-1G-2',
	'Balard-1H-1',
	'Balard-2C-1',
	'Balard-2D-1',
	'Balard-2G-1',
	'Balard-2H-1',
	'Balard-2H-2',
	'Balard-3C-1',
	'Balard-3D-1',
	'Balard-3G-1',
	'Balard-3G-2',
	'Balard-3H-1',
	'Balard-4C-1',
	'Balard-4D-1',
	'Balard-4G-1',
	'Balard-4H-1',
	'Balard-SRV',
	'Balard-SRV-SUP',
	'Balard-SRV-CINES',
	'Balard-SUP-CINES']


	# Getting infos from the Tftpboot server
	os.system('scp mcabos@tftp.srv-prive.icgm.fr:/var/lib/tftpboot/snoop/* .')
	Dpt_dict=Get_Dpt('../Ordinateurs.ods')

	#Building IP:MAC dict
	ip2mac={}
	for switch in switch_dict.keys():
		Content=get_content(switch)
		ip2mac[switch]=build_ip_mac_dict(Content)

	# Brownsing ods file
	file_name='../Ordinateurs.ods'
	records = p.get_array(file_name=file_name)
	regex=r"/[0-9]+$"
	Final_dict={}
	Final_dict['Nom de la machine']=['@mac','Departement', '@ip machine', 'nom switch', '@ip switch', 'n?? port', 'Triolet Gigabit','n?? Prise','Commentaires']

	# Searching current mac in @MAC database and updating Dictionnary Fields
	for record in records:
		for switch in switch_dict.keys():
			for k,v in ip2mac[switch].items():
				if record[1] == k : 
					matches=re.finditer(regex,v[1],re.MULTILINE)
					for matchNum, match in enumerate(matches, start=1):
						port=match.group()[1:]
					Final_dict[record[0]]=[k,Dpt_dict[record[0]],v[0],switch,switch_dict[switch],port,"Gi"+v[1],"",'']

	# Updating Comments Field
	Comm=Get_Comm('../Ordinateurs.ods',Final_dict)
	for k,v in Final_dict.items():
		if not (k == 'Nom de la machine'):
			tmp=v 
			tmp[8]=Comm[k]
			Final_dict[k]=tmp

	# for sw in liste_switch:
	# 	Final_dict=update_Room_Sockets(sw,Final_dict)

	# Updating Room Sockets Names Field
	for Cisco_name in switch_dict2.values():
		Final_dict=Cis2Socket(Cisco_name,Final_dict)

	# Building the not-conected Dictionnarry
	Not_Conctd_Dict=Get_not_connected_dict('../Ordinateurs.ods',Final_dict)

	# Packaging as array to write
	line=[]
	to_write=[]
	for k,v in Final_dict.items():
		line=[]
		line.append(k)
		line.extend(v)
		to_write.append(line)

	to_write_ntc=[['Nom de la machine','@mac','Departement', '@ip machine', 'nom switch', '@ip switch', 'n?? port', 'Triolet Gigabit','n?? Prise','Commentaires']]
	for k,v in Not_Conctd_Dict.items():
		line=[]
		line.append(k)
		line.extend(v)
		to_write_ntc.append(line)

	Content={'Sheet 1':to_write, 'Sheet2':to_write_ntc}

	# Saving ods file
	book = p.Book(Content)
	book.save_as('TftpBoot_List.xlsx')
	os.system('rm Description*')
	os.system('rm balard*')


	# Setting Ods Document Layout
	from openpyxl import *

	Wb=load_workbook(filename='TftpBoot_List.xlsx')

	border=styles.borders.Border(left=styles.borders.Side(style='medium'), 
	                     right=styles.borders.Side(style='medium'), 
	                     top=styles.borders.Side(style='medium'), 
	                     bottom=styles.borders.Side(style='double'))
	border2=styles.borders.Border(left=styles.borders.Side(style='thin'), 
	                     right=styles.borders.Side(style='double'), 
	                     top=styles.borders.Side(style='thin'), 
	                     bottom=styles.borders.Side(style='thin'))
	border3=styles.borders.Border(left=styles.borders.Side(style='thin'), 
	                     right=styles.borders.Side(style='thin'), 
	                     top=styles.borders.Side(style='thin'), 
	                     bottom=styles.borders.Side(style='thin'))
	font=styles.Font(color="00333333",size=12,bold=True)
	font2=styles.Font(color="00333333",size=11,bold=False)
	font3=styles.Font(color="00333300",italic=True)
	fill = styles.PatternFill("solid",fgColor="DDDDDD")
	fill2 = styles.PatternFill("solid",fgColor="e8e8e8")

	for Ws in Wb.worksheets:
		for col in Ws.columns:
			maxi=0
			column=utils.get_column_letter(col[0].column)
			for cell in col:
				try:
					if(len(str(cell.value)) > maxi):
						maxi=len(cell.value)
				except:
					pass 
			adj_width=(maxi + 2)*1.2
			Ws.column_dimensions[column].width = adj_width
		Ws.showGridLines = True
		for i in range(1,11):
			Ws.cell(row=1,column=i).border=border
			Ws.cell(row=1,column=i).font=font
			Ws.cell(row=1,column=i).fill=fill
		for i in range(2,Ws.max_row+1):
			Ws.cell(row=i,column=1).border=border2
			Ws.cell(row=i,column=1).font=font2
			Ws.cell(row=i,column=1).fill=fill
			if(i<Ws.max_row):
				Ws.cell(row=i,column=2).font=font3
				Ws.cell(row=i,column=2).fill=fill2
				Ws.cell(row=i,column=2).border=border3
				Ws.cell(row=i,column=3).fill=fill2
				Ws.cell(row=i,column=3).border=border3
				Ws.cell(row=i,column=4).font=font3
				Ws.cell(row=i,column=4).fill=fill2
				Ws.cell(row=i,column=4).border=border3
				Ws.cell(row=i,column=5).fill=fill2
				Ws.cell(row=i,column=5).border=border3
				Ws.cell(row=i,column=6).font=font3
				Ws.cell(row=i,column=6).fill=fill2
				Ws.cell(row=i,column=6).border=border3
				Ws.cell(row=i,column=7).fill=fill2
				Ws.cell(row=i,column=7).border=border3
				Ws.cell(row=i,column=8).fill=fill2
				Ws.cell(row=i,column=8).border=border3
				Ws.cell(row=i,column=9).fill=fill2
				Ws.cell(row=i,column=9).border=border3
				Ws.cell(row=i,column=10).fill=fill2
				Ws.cell(row=i,column=10).border=border3
	Wb.save(filename='TftpBoot_List.xlsx')

	# Convert to .ods file
	os.system('soffice --headless --convert-to ods *.xlsx')
	os.system('rm *.xlsx')