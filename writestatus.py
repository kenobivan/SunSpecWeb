import requests
import json
url = 'http://141.58.49.168/writestatus'
control = [{'controlvwatt': [[100.0,67],[110.0,100],[90.0,100]]}]
headers = {'content-type': 'application/json'}
r = requests.post(url, data=json.dumps(control), headers=headers)
print(r.text)

