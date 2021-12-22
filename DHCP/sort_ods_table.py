from sys import *
import random as r
import pyexcel as p

# A script for sorting list using the BEST ALGORITHM EVER FOUND
# This script sort big data arrays (for example a routing table...)

__author__="CABOS Matthieu"
# __date__=09_09_2021

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

# Main as example

if (len(argv)<=1):
	print("Usage : python3 sort_routing_table.py <ODS file name> <ODS destination file name> <N° column as reference>")
	print("Exemple : python3 sort_routing_table.py Switchs.ods MyNewFile.ods 2")
	print("This command open the Switchs.ods file and sort from column 2 order.")
	quit()
file_name=argv[1]
try:
	dest_file_name=argv[2]
except:
 dest_file_name="MyNewFile.ods"
try:
	column_id=int(argv[3])
except:
	column_id=0

records = p.get_array(file_name=file_name)
id_list=[]
for record in records:
	id_list.append(record[column_id])               # Getting Plug numbers (as example)

sorting=shellSort(id_list)                  # Sorting Id List
out_array=permutation(records,sorting[1])   # Apply permutation to full array
# out_array=Del_duplicate(out_array)

p.isave_as(array=out_array,dest_file_name=dest_file_name)
print("Your file have been saved as "+str(dest_file_name))