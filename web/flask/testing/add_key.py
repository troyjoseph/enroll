# -*- coding: utf-8 -*-
import requests, json

url = 'http://localhost:5000'
payload = {'password': 'abc','key': '1234'}
headers = {'Content-type': 'application/json'}
r = requests.post(url + '/add_key',
              data=json.dumps(payload), headers=headers)
print r.text
