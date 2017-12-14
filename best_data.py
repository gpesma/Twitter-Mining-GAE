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



class Best(ndb.Model):
    text = ndb.StringProperty()
    url = ndb.StringProperty()
    time = ndb.DateTimeProperty()
    likes = ndb.IntegerProperty()
    sensitive = ndb.FloatProperty()

@app.route('/best')
def update_table():

    q = Tweet.query()
    q = q.order(-Tweet.likes).order(-Tweet.sensitive)
    #q = q.fetch(100)
    new_tweets = []
    i = 0
    #print q
    for tweet in q.iter():
    	print tweet
        new_tweets.append(Best(text=tweet.text,
                            url = tweet.url,
                            time = tweet.time,
                            likes = tweet.likes,
                            sensitive = tweet.sensitive))
        i += 0
        if i == 100:
        	break
    ndb.put_multi(new_tweets)
    q = Best.query().order(Best.time).order(-Best.likes).order(-Best.sensitive)
    
    for r_key in q.iter(keys_only=True, offset=100):
        print r_key 
        r_key.delete()
    return 'sucess'