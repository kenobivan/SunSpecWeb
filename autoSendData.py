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

slaveid = 1
ipaddr = '127.0.1.1'
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
	i = 0
	invvalues = []
	for model in sd.device.models_list:
			if model.model_type.label == "Inverter (Single Phase)":
				invmodel = model
				break
	for point in invmodel.blocks[0].points_list:
		if i > 18:
			break
		if point.value != None:
			invvalues.append((point.point_type.id, point.value, point.point_type.units))
		i += 1
	return invvalues

invvalues = get_status()
print (type(invvalues[10][1]))

livedict = {}

for value in invvalues:
	livedict.update({value[0]: float(value[1])})


# datapoints ist liste mit beliebig viequirlen Einträgen, die gespeichert werden sollen (mehr als 1000 würde ich nicht auf einmal schicken)
datapoints=[
        {'grid': 'testgrid',
           'measurement': 'pv_controller_prototype',
           'time': int(time.time()),
           'fields': {
                   'U1': float(invvalues[10][1]),
                   'U2': 1.324,
                   },
            'tags': {}
        }
]
datapoints[0]["fields"].update(livedict)
print(datapoints)
json_data={"grid":"testgrid","datapoints":datapoints}
try:
	r = requests.post('http://129.69.127.226:13333/api/write', json=json_data)
	print(r.status_code)
except requests.exceptions.RequestException as e:
	print(e)
	if os.stat("data.txt").st_size == 0:
		with open("data.txt", mode='w') as jsonfile:
			json.dump([], jsonfile)
	with open("data.txt", mode='r') as jsonfile:
		jsonlist = json.load(jsonfile)
	with open("data.txt", mode='w') as jsonfile:
		jsonlist.append(datapoints[0])
		json.dump(jsonlist, jsonfile)
		print(jsonlist)

