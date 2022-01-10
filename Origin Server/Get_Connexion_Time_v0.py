import os

__author__="CABOS Matthieu"
__date__=22/12/2021

def Init_dict(Hostname,flag):

	# Intialisation of Dictionnaries with default values

	res={}
	for i in range(len(Hostname)):
		if not flag:
			res[Hostname[i]]=999999999999
		else:
			res[Hostname[i]]=0
	return res 

def Get_Max(liste):
	maxi=0
	for item in liste:
		if item>maxi:
			maxi=item 
	return maxi

def Get_Min(liste):
	mini=99999999999999999999999
	for item in liste:
		if item<mini:
			mini=item
	return mini

def build_dict():

	time_dict_in={}
	time_dict_out={}

	# I first read the results of the Treat_tokens.sh script

	IN_Hostname=os.popen('./Treat_tokens.sh 3').readlines()
	OUT_Hostname=os.popen('./Treat_tokens.sh 4').readlines()
	IN_TIME=os.popen('./Treat_tokens.sh 5').readlines()
	OUT_TIME=os.popen('./Treat_tokens.sh 6').readlines()

	# Sort and Store them into lists

	IN_Hostname=[item.replace('\n','') for item in IN_Hostname]
	OUT_Hostname=[item.replace('\n','') for item in OUT_Hostname]
	IN_TIME=[item.replace('\n','') for item in IN_TIME]
	OUT_TIME=[item.replace('\n','') for item in OUT_TIME]

	for i in range(len(IN_Hostname)):
		if not IN_Hostname[i] in time_dict_in:
			time_dict_in[IN_Hostname[i]]=int(IN_TIME[i])
		elif (IN_Hostname[i] in time_dict_in) and (int(IN_TIME[i])<time_dict_in[IN_Hostname[i]]):
			time_dict_in[IN_Hostname[i]]=int(IN_TIME[i])
		else:
			pass
	for i in range(len(OUT_Hostname)):
		if not OUT_Hostname[i] in time_dict_out:
			time_dict_out[OUT_Hostname[i]]=int(OUT_TIME[i])
		elif (OUT_Hostname[i] in time_dict_out) and (int(OUT_TIME[i])>time_dict_out[OUT_Hostname[i]]):
			time_dict_out[OUT_Hostname[i]]=int(OUT_TIME[i])
		else:
			pass
	return time_dict_in,time_dict_out

def Get_Connection_Time():

	# Computing the connection time since the first OUT token and the last IN token

	IN,OUT=build_dict()
	res={}
	for user in IN.keys():
		if user in OUT.keys():
			res[user]=abs((OUT[user]-IN[user])/60)
	return res

build_dict()
Connection_Time=Get_Connection_Time()
print(Connection_Time)