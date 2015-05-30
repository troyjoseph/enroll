#!/usr/bin/env python
# import requests
import unirest
import urllib2


class Helper():

    def testLogin(self, netid, password):
        if(netid == '' or password == ''):
            return False

        try:
            url = 'http://studentcenter.cornell.edu'
            headers = {'User-Agent': 'Mozilla/5.0'}
            payload = {
                'netid': netid,
                'password': password,
                'realm': 'CIT.CORNELL.EDU',
                'Submit': 'Login'
            }

            url = urllib2.urlopen(url).geturl()
            response = unirest.post(url, headers=headers, params=payload).body
            return 'Unable to log in' not in str(response)
        
        except:
            return False
