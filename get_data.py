from flask import Flask, render_template, request
from google.appengine.ext import ndb
import json

app = Flask(__name__)

class Best(ndb.Model):
    text = ndb.StringProperty()
    url = ndb.StringProperty()
    time = ndb.DateTimeProperty()
    likes = ndb.IntegerProperty()
    sensitive = ndb.FloatProperty()


@app.route('/get_data', methods=['GET'])
def put_data():
    q = Best.query()
    q = q.order(-Best.likes).order(-Best.sensitive)
    q = q.fetch(10)

    result = ''
    for tweet in q:
    	result = str(result) + '\n' + str(tweet.text) +', ' + str(tweet.url)
    #print result
    return result