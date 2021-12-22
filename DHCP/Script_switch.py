from sys import *
import os

liste_switch=['Balard-1C-1','Balard-1D-1','Balard-1D-1','Balard-1G-1','Balard-1H-1','Balard-2C-1','Balard-2D-1','Balard-2G-1','Balard-2H-1','Balard-3C-1','Balard-3D-1','Balard-3G-1','Balard-3G-2','Balard-3H-1','Balard-4C-1','Balard-4D-1','Balard-4G-1','Balard-4H-1']
# name_switch=argv[1]
for name_switch in liste_switch:
	stream=os.popen('./config-switch.py ' + str(name_switch))
	Instructions=stream.read()
	os.system(Instructions)
