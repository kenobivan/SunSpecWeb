import sunspec.core.client as client
d = client.SunSpecClientDevice(client.RTU, 1 , "com6")
print (d.models)