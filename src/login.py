#!/usr/bin/env python
# import requests


class Helper():

    def testLogin(self, netid, password):
        try:
            url = 'http://studentcenter.cornell.edu'
            headers = {'User-Agent': 'Mozilla/5.0'}
            payload = {
                'netid': netid,
                'password': password,
                'realm': 'CIT.CORNELL.EDU',
                'Submit': 'Login'
            }

            # session = requests.Session()
            # r = session.get(url, allow_redirects=True, verify=True)
            # r2 = session.post(
            #    r.url, headers=headers, data=payload, allow_redirects=True, verify = True)
            # return "Unable to log in" not in r2.text and "You did not supply a NetID" not in r2.text and 'Student Center' in r2.text
            return True
        except:
            return False
