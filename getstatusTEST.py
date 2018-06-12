import urllib.request, json
#link anpassen
with urllib.request.urlopen("http://localhost:5000/getstatus") as url:
    data = json.loads(url.read().decode())
    print(data)
