import requests 

url = 'http://studentcenter.cornell.edu'
headers = {'User-Agent': 'Mozilla/5.0'}
payload = {
		'netid':'tcj29',
		'password':'tc2013j@cony',
		'realm' : 'CIT.CORNELL.EDU',
		'Submit' : 'Login'
}

session = requests.Session()
r = session.get(url, allow_redirects = True)
r2 = session.post(r.url, headers= headers, data = payload, allow_redirects=True)
print( r2.text )

#curl -L --data "netid=tcj29&password=tc2013j@cony&realm=CIT.CORNELL.EDU&=Submit=Login" 'http://studentcenter.cornell.edu'