import urllib.request
import xmltodict
import json
import datetime

file = urllib.request.urlopen('http://73.130.117.239:1139/state.xml')
data = file.read()
file.close()

#data = xmltodict.parse(data)
print(data)
print(json.dumps(xmltodict.parse(data)))
data = xmltodict.parse(data)
print(data['datavalues']['time'])
print(datetime.datetime.fromtimestamp(int(data['datavalues']['time'])).strftime('%Y-%m-%d %H:%M:%S'))
