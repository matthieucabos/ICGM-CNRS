import os
import pyexcel as p
import re

__author__="CABOS Matthieu"
__date__=25/10/2021

def gen(size,maxi=100):
	# Generator for relative size array
	res=[]
	for i in range(size):
		ok=False
		while not ok:
			tmp=r.randint(65,122)
			if (tmp >= 65 and tmp <= 90) or (tmp >= 97 and tmp <=122):
				ok=True
				res.append(chr(tmp))
				tmp=0
	return res

def complete_permutation(permutation):
	# Completing secondaries permutations since 1.1
	rez=[]
	for item in permutation:  
		rez.append(item)
		k=item[1]
		l=item[1]+1
		while l<=item[0]:
			rez.append((k,l,0))
			k+=1
			l+=1
	return rez

def shellSort(liste):
	# Shell sort algorithm with permutation memory as list
	permutation=[]
	count=0
	for i in range(len(liste)):
		count=0
		for j in range(i,len(liste)):
			tmp=liste[j]
			k=j
			while(k>=i and liste[k-i]>tmp):
				liste[k]=liste[k-i]
				k-=i
				count+=1
			liste[k]=tmp
			if(j!=k):
				permutation.append((j,k,1))
	final_perm=[]
	# 1.1
	final_perm=complete_permutation(permutation)
	return (liste,final_perm)

def permutation(liste,permutation):
	# Realize the signed permutation iven as second return of shellSort function
	final_liste=liste[:]
	for i in permutation:
		if (i[2]==1):
			liste=final_liste[:]
		final_liste[i[1]]=liste[i[0]]
	return final_liste

def Del_duplicate(records):
	res=[]
	for i in range(len(records)):
		if not (records[i] in records[i+1:]):
			res.append(records[i])
	return res

def switch(x,*arg):
	dic ={}
	for i in range(int(len(arg)-1)):
		dic[arg[i]]=arg[i+1]
	return dic.get(x,'default')

def Get_Bloc(RoomName,Niveau):
	if ('A' in RoomName):
		bloc=switch(Niveau,
			2,12,
			3,27,
			4,40,
			5,52)
	elif ('B' in RoomName):
		bloc=switch(Niveau,
			2,16,
			3,28,
			4,41,
			5,53)
	elif ('C' in RoomName):
		bloc=switch(Niveau,
			2,17,
			3,29,
			4,42,
			5,54)
	elif ('D' in RoomName):
		bloc=switch(Niveau,
			2,18,
			3,30,
			4,43,
			5,55)
	elif ('E' in RoomName):
		bloc=switch(Niveau,
			2,19,
			3,31,
			4,44,
			5,56)
	elif ('F' in RoomName):
		bloc=switch(Niveau,
			2,20,
			3,32,
			4,45,
			5,57)
	elif ('G' in RoomName):
		bloc=switch(Niveau,
			2,21,
			3,33,
			4,46,
			5,58)
	elif ('H' in RoomName):
		bloc=switch(Niveau,
			2,22,
			3,34,
			4,47,
			5,59)
	elif ('I' in RoomName):
		bloc=switch(Niveau,
			2,23,
			3,35,
			4,48,
			5,60)
	elif ('J' in RoomName):
		bloc=switch(Niveau,
			2,24,
			3,36,
			4,49,
			5,61)
	elif ('K' in RoomName):
		bloc=switch(Niveau,
			2,25,
			3,37,
			4,50,
			5,62)
	elif ('Z' in RoomName):
		bloc=switch(Niveau,
			2,26,
			3,38,
			4,51,
			5,63)

	return bloc

def Set_Room():
	file_name='../Switchs.ods'
	dest_file_name="Switchs2.ods"
	column_id=0

	# Getting ods file as array
	records = p.get_array(file_name=file_name)
	id_list=[]

	for record in records:
		id_list.append(record[column_id])       # Getting Plug numbers (as example)

	sorting=shellSort(id_list)                  # Sorting Id List
	out_array=permutation(records,sorting[1])   # Apply permutation to full array

	file_name='Switchs2.ods'
	etage=''
	done=[]
	values=[]

	records=out_array
	loc_id=0
	for rec in records:
		if (not rec[0] in done) and (not rec[0] == '') and (not rec[0] == 'Bureau') and (not rec[0] == 'CINES'):
			# Sorting by Floor
			if ('N1' in rec[0]):
				etage='Étage 1'
				loc_id=Get_Bloc(rec[0],2)
				IntFloor=2
			elif ('N2' in rec[0]):
				etage='Étage 2'
				loc_id=Get_Bloc(rec[0],3)
				IntFloor=3
			elif ('N3' in rec[0]):
				etage='Étage 3'
				loc_id=Get_Bloc(rec[0],4)
				IntFloor=4
			elif ('N4' in rec[0]):
				etage='Étage 4'
				loc_id=Get_Bloc(rec[0],5)
				IntFloor=5
			elif ('RJPA' in rec[0]) or ('RJLG' in rec[0]):
				etage='PAC'
				loc_id=64
				IntFloor=7
			elif ('SSPA' in rec[0]):
				etage='PAC'
				loc_id=64
				IntFloor=7
			elif ('RJEP' in rec[0]):
				etage='Exp Prot'
				loc_id=65
				IntFloor=9
			elif ('SSEP' in rec[0]):
				etage='Exp Prot'
				loc_id=66
				IntFloor=9

			# Updating values fields
			Room="\""
			Room=Room+str(rec[0])+"\""
			Str_bloc=switch(loc_id,
				12,'bloc A',
				16,'bloc B',
				17,'bloc C',
				18,'bloc D',
				19,'bloc E',
				20,'bloc F',
				21,'bloc G',
				22,'bloc H',
				23,'bloc I',
				24,'bloc J',
				25,'bloc K',
				26,'bloc Z',
				27,'bloc A',
				28,'bloc B',
				29,'bloc C',
				30,'bloc D',
				31,'bloc E',
				32,'bloc F',
				33,'bloc G',
				34,'bloc H',
				35,'bloc I',
				36,'bloc J',
				37,'bloc K',
				38,'bloc Z',
				40,'bloc A',
				41,'bloc B',
				42,'bloc C',
				43,'bloc D',
				44,'bloc E',
				45,'bloc F',
				46,'bloc G',
				47,'bloc H',
				48,'bloc I',
				49,'bloc J',
				50,'bloc K',
				51,'bloc Z',
				52,'bloc A',
				53,'bloc B',
				54,'bloc C',
				55,'bloc D',
				56,'bloc E',
				57,'bloc F',
				58,'bloc G',
				59,'bloc H',
				60,'bloc I',
				61,'bloc J',
				62,'bloc K',
				63,'bloc Z',
				64,'RDJ',
				65,'RDJ',
				66,'Sous-sol'
				)
			if (IntFloor != loc_id):
				values.append('values('+str(Room)+','+str(loc_id)+', "Batiment Balard > '+str(etage)+' > '+str(Str_bloc)+' > '+str(rec[0])+'", 4,\'{"1":1,"'+str(IntFloor)+'":'+str(IntFloor)+',"'+str(loc_id)+'":'+str(loc_id)+'}\',Now(),Now());')
			else:
				values.append('values('+str(Room)+','+str(loc_id)+', "Batiment Balard > '+str(etage)+' > '+str(Str_bloc)+' > '+str(rec[0])+'", 4,\'{"1":1,"'+str(loc_id)+'":'+str(loc_id)+'}\',Now(),Now());')
		done.append(rec[0])

	# SQL Formatting
	sql_pre='insert into glpi_locations (name,locations_id,completename , level,ancestors_cache,date_mod,date_creation) '
	Content=''
	for item in values:
		Content= Content + sql_pre + item + '\n'

	# Writing SQL into file my_glpi.sql
	f=open('my_glpi.sql','w')
	f.write(Content)
	f.close()

def Build_Room_dict():
	# Building the Room:Id Dictionnary since the Table.sql file (should be another name)
	Room_dict={}
	file_name='./Table.sql'
	f=open(file_name,'r')
	Lines=f.readlines()
	for line in Lines:
		tmp=line.split(',')[8]+','+line.split(',')[9]+','+line.split(',')[10]
		Room_dict[line.split(',')[3][1:-1]]=[line.split(',')[0][1:],line.split(',')[5][1:-1],tmp[1:-1]]
	return (Room_dict)

def Set_Sockets(dico):
	file_name='../Switchs.ods'
	column_id=2

	# Getting ods file as array
	records = p.get_array(file_name=file_name)
	id_list=[]

	for record in records:
		id_list.append(record[column_id])       # Getting Plug numbers (as example)

	sorting=shellSort(id_list)                  # Sorting Id List
	out_array=permutation(records,sorting[1])   # Apply permutation to full array

	done=[]
	values=[]
	records=out_array
	reg=re.compile(r'([A-Z]+[0-9]+)*')
	locations_id=0
	completename=''
	ancestors_cache=''
	for rec in records:
		if (not rec[2] in done) and (not 'CINES' in rec[2]):
			Room=reg.match(rec[2]).group(0)
			try:
				locations_id=int(dico[Room][0])
				completename=dico[Room][1]+' > '+rec[2]
				ancestors_cache=str(dico[Room][2][:-1]).replace('\\','')+',\"'+str(dico[Room][0])+'\":'+str(dico[Room][0])+'}'
			except:
				pass
			done.append(rec[2])
			values.append('values("'+str(rec[2])+'",'+str(locations_id)+',"'+completename+'",5,\''+str(ancestors_cache)+'\',Now(),Now());')

	# SQL Formatting
	sql_pre='insert into glpi_locations (name,locations_id,completename , level,ancestors_cache,date_mod,date_creation) '
	Content=''
	for item in values:
		Content= Content + sql_pre + item + '\n'


	# Writing SQL into file my_glpi.sql
	f=open('my_glpi2.sql','w')
	f.write(Content)
	f.close()
	os.system("sed -i '1d;$d' my_glpi2.sql ")

Set_Room()
Set_Sockets(Build_Room_dict())
quit()