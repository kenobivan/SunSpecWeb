# -*- coding: utf-8 -*-
"""
Created on Mon Jun 18 11:00:52 2018

@author: ac123687
"""

import requests
import time
import json
import os

import sys
import sunspec.core.client as client
import sunspec.core.suns as suns
from optparse import OptionParser

slaveid = 1#126
ipaddr = '127.0.1.1'#'192.168.0.111'
ipport = 502
timeout = 2.0
transtype = 'tcp'

try:
	sd = client.SunSpecClientDevice(client.TCP, slaveid, ipaddr=ipaddr, ipport=ipport, timeout=timeout)

except client.SunSpecClientError as e:
	print('Error: %s'%(e))
	sys.exit(1)

if sd is not None:
	print('\nTimestamp: %s' % (time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())))

def get_status():
	sd.read()
	with open("logs/modeldict.txt", mode='r') as jsonfile:
		modeldict = json.load(jsonfile)
	mdlnmbINV = modeldict['103']
	i = 0
	invvalues = []
	
	invmodel = sd.device.models_list[mdlnmbINV]
	
	try:
		for point in invmodel.blocks[0].points_list:
			if i > 18:
				break
			if point.value != None:
				invvalues.append((point.point_type.id, point.value, point.point_type.units))
			i += 1
	except:
		pass
	return invvalues
	
def writeAfterError(datapoints):
	#falls leeres doc wird liste erstellt
	if os.stat("logs/data.txt").st_size == 0:
		print("empty")
		with open("logs/data.txt", mode='w') as jsonfile:
			json.dump([], jsonfile)
			jsonfile.close()
	#altes JSON wird geladen
	with open("logs/data.txt", mode='r') as jsonfile:
		jsonlist = json.load(jsonfile)
	#und neue Werte hinzugeschrieben
	with open("logs/data.txt", mode='w') as jsonfile:
		jsonlist.append(datapoints[0])
		json.dump(jsonlist, jsonfile)
		jsonfile.close()
	return
	
#werte mit get_status() abfragen
invvalues = get_status()
#werte in dict packen 
livedict = {}
for value in invvalues:
	livedict.update({value[0]: float(value[1])})


# datapoints ist liste mit beliebig viequirlen Einträgen, die gespeichert werden sollen (mehr als 1000 würde ich nicht auf einmal schicken)
datapoints=[
        {'grid': 'testgrid',
           'measurement': 'pv_controller_prototype',
           'time': int(time.time()),
           'fields': {
                   'U1': float(200.0),
                   'U2': 1.324,
                   },
            'tags': {}
        }
]
datapoints[0]["fields"].update(livedict)
datapointsNew = datapoints
if os.stat("logs/data.txt").st_size != 0:
	with open("logs/data.txt", mode='r') as jsonfile:
		jsonlist = json.load(jsonfile)
		datapoints.append(jsonlist[0])
json_data={"grid":"testgrid","datapoints":datapoints}
try:
	r = requests.post('http://129.69.127.226:13333/api/writ', json=json_data)
	print(r.status_code)
	if r.status_code != 200:
		writeAfterError(datapointsNew)
	else:
		open('logs/data.txt', 'w').close()
	
#wenn fehler zB ConnectionError wird JSON in file geschrieben anstatt zu senden
except Exception as e:
	print(e)
	writeAfterError(datapointsNew)
	

