# -*- coding: utf-8 -*-
from flask import Flask, request
import sql as sqlLib

# configuration
DATABASE = '/tmp/flaskr.db'
DEBUG = True
SECRET_KEY = '\x9e\xb7\x8cM\x178Z\x10\x04\x13\x04v\xd7\xa9_\xb1\xd1\\\x8eJv\x04\xe1\t',
PASSWORD = '3k54ylsZXJ5ozxxmfEbvJe4oz4oTA5uur1vbxZQbMWH9NySK4Q1fBl3wH9Z4wnqhEPLaCSeHXaRc1UalCFYUJVFRGxkJgbdwQE6oa1fZoelQMfbCUJGHJQWXCL4LNUll5Wo1KCPONmqVq3d2d0440UZtrkkrfHB4nxaElnMIz32qp8m14Wc6qVrzqRhHAwc8vSVAEa0aVWJG5s5Y8FSE82DR4TJyQC7BEby3SUaM0Q3RV3l0XhgjjQLlCOUjulsdzLKHtw1TZOb3Mkq38XlSvpcaNg46epgrEGOVVJPWLftvSrwZuWwfIH7bo7w1WwqWGaxcO14KTfyg3m9oL6mzC5g'
MASTERPASSWORD = '3k54ylsZXJ5ozxxmfEbvJe4oz4oTA5uur1vbxZQbMWH9NySK4Q1fBl3wH9Z4wnqhEPLaCSeHXaRc1UalWHqwxkJgbdwQE6oa1fZoelQMfb3deL4LNUll5Wo1KCPONmqVq3d2d0440UZtrkkrfHB4nxaElnMIz32qp8m14Wc6qVrzqRhHAwc8vSVAEa0aVWJG5s5Y8FSE82DR4TJyQC7BEby3SUaM0Q3RV3l0XhgjjQLlCOUjulsdzLKHtw1TZOb3Mkq38XlSvpcaNg46epgrEGOVVJPWLftvSrwZuWwfIH7bo7w1WwqWGaxcO14KTfyg3m9oL6mzC5g'

# create our little application :)
app = Flask(__name__)
app.config.from_object(__name__)
app.config.from_envvar('FLASKR_SETTINGS', silent=True)


def authenticatedMaster(password):
    return password == MASTERPASSWORD


def authenticated(password):
    return password == PASSWORD


def validateKey(key):
    return isinstance(key, (int)) and len(key) == 10


def validateUser(user):
    return True


@app.route('/view')
def view():

    db = sqlLib.get_db()
    cur = db.execute('select usermachine, productkey from entries order by id desc')
    entries = cur.fetchall()
    s = ''
    for entry in entries:
        s += '<br>User {0}\tKey{1}'.format(entry[0], entry[1])
    return s


# JSON {'password': password, 'key': key}
@app.route('/add_key', methods=['POST'])
def add_key():
    json = request.get_json()
    try:
        key = str(json['key'])
        password = str(json['password'])
        if not authenticatedMaster(password):
            return 'Incorrect password'
        else:
            if validateKey(key):
                sql = 'insert into entries (productkey) values ("{0}")'.format(key)
                sqlLib.executeSQL(sql)
                return 'New key was successfully added'
            else:
                return 'invalid key'

    except:
        return 'Incorrect POST format'


# JSON {'user': usermachine, 'key': key, 'password': password}
@app.route('/checkin', methods=['POST'])
def checkIn():
    json = request.get_json()
    try:
        user = str(json['user'])
        key = str(json['key'])
        password = str(json['password'])
        if not authenticated(password):
            return 'Incorrect password'
        else:
            entries = sqlLib.getEntries()
            if key not in entries:
                return 'Invalid Key'
            if entries[key] is None:  # No user for this key yet
                sql = 'UPDATE entries SET user="{0}" WHERE productkey="{1}"'.format(user, key)
                sqlLib.executeSQL(sql)
                return 'Added New User'
            if entries[key] == user:
                return 'Valid User'
            else:
                return 'Invalid User'
    except:
        return 'Incorrect POST format'


if __name__ == '__main__':
    sqlLib.init_db()
    app.run()
