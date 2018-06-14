import requests
import json
url = 'http://0.0.0.0:5000/writestatus'
control = [{'controlvwatt': [[100.0,100],[110.0,100],[90.0,100]]}, {'controlmaxp': '22'}, {'controlvfactor': [[100,0.02],[110,0.02],[90,0.02]]}, {'activate':[['qu','true'],['pu','true'],['maxp','false']]} ]
headers = {'content-type': 'application/json'}
r = requests.post(url, data=json.dumps(control), headers=headers)
print(r.text)

