#!/usr/bin/env python
from contextlib import closing
try:
    from urllib.parse import urlencode
    from urllib.request import urlopen
except ImportError: # Python 2
    from urllib import urlencode
    from urllib2 import urlopen

url = 'http://localhost:5000/post'
data = urlencode({"keys" : [], "models":["Static Volt-VAR (126)"]}).encode()
with closing(urlopen(url, data)) as response:
    print(response.read().decode())