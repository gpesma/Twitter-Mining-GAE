from flask import Flask, request, abort, jsonify
from google.appengine.ext import ndb
import datetime
app = Flask(__name__)


class Tweet(ndb.Model):
	likes = ndb.IntegerProperty()
	text = ndb.StringProperty()
	url = ndb.StringProperty()
	time = ndb.DateTimeProperty()
	sensitive = ndb.FloatProperty()


@app.route('/task')
def trim_data():
    q = Tweet.query()
    q.filter(Tweet.time > datetime.datetime.now() - datetime.timedelta(days=1))

    for r_key in q.iter(keys_only=True):
    	print r_key	
    	r_key.delete()	
    	#results.append(r_key)
    #ndb.delete_multi(result)
    return 'ok'


