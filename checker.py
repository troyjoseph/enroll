import requests, json

class Nbr():
	

	def get(self, semester, nbr):
		url="http://ajax.googleapis.com/ajax/services/search/web?v=1.0&q=site:classes.cornell.edu/browse/roster/SP15/class/+"
		try:
			r=requests.get(url+str(nbr))
			print url+str(nbr)
		except:
			print "No internet connection!"
			return
		dict = json.loads(r.text)

		index = -1
		try:
			for i in range(len(dict['responseData']['results'])):
				url = dict['responseData']['results'][i]['url']
				if (semester in url):
					if (str(url[-4:]) != str(nbr)):
						print url[-4:]
						print nbr
						index = i
						break
		finally:
			if (index == -1):
				print "Could not find class!"
				print r.text
				print url

			else:
				url = dict['responseData']['results'][index]['url']
				return url[53:-5]+" "+ url[-4:]

