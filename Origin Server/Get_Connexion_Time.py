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

def Build_Token_dict():

	# Building Timestamp Dictionnary to compute the connection time

	Done=False

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

	# Initialising Dictionnaries

	Token_Dict_IN=Init_dict(IN_Hostname,1)
	Token_Dict_OUT=Init_dict(OUT_Hostname,0)

	# Populate Dictionnaries

	for i in range(len(IN_Hostname)):
		if (int(IN_TIME[i])>Token_Dict_IN[IN_Hostname[i]]):
			Token_Dict_IN[IN_Hostname[i]]=int(IN_TIME[i])
	for i in range(len(OUT_Hostname)):		
		if (int(OUT_TIME[i])<Token_Dict_OUT[OUT_Hostname[i]]):
			Token_Dict_OUT[OUT_Hostname[i]]=int(OUT_TIME[i])

	return Token_Dict_IN,Token_Dict_OUT

def Get_Connection_Time(IN,OUT):

	# Computing the connection time since the first OUT token and the last IN token

	res={}
	for user in IN.keys():
		if user in OUT.keys():
			res[user]=abs((OUT[user]-IN[user])/60)
	return res
IN,OUT=Build_Token_dict()
Connection_Time=Get_Connection_Time(IN,OUT)
print(Connection_Time)