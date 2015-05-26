import requests, json

class Nbr():
	
	def get(semester, nbr):
		url="http://ajax.googleapis.com/ajax/services/search/web?v=1.0&q=site:classes.cornell.edu+"
		try:
			r=requests.get(url+nbr)
		except:
			print "No internet connection!"
			break
		dict = json.loads(r.text)

		index = -1
		try:
			for i in range(len(dict['responseData']['results'])):
				if (semester in dict['responseData']['results'][i]['url']):
					index = i
					break
		finally:
			if (index == -1):
				print "Could not find class!"
				print r.text

			else:
				url = dict['responseData']['results'][index]['url']
				print url[53:-5]+" "+ url[-4:]

