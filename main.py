from flask import Flask, render_template, request
from google.appengine.ext import ndb

app = Flask(__name__)

class Best(ndb.Model):
    text = ndb.StringProperty()
    url = ndb.StringProperty()
    time = ndb.DateTimeProperty()
    likes = ndb.IntegerProperty()
    sensitive = ndb.FloatProperty()

@app.route('/')
def home():
    q = Best.query()
    q = q.order(-Best.likes).order(-Best.sensitive)
    #q = q.fetch(15)
    d = []
    i = 0
    for tweet in q.iter():
        d.append(tweet.text)
        d.append(tweet.url)
        i += 1
        if i == 25:
            break
    return render_template('form.html', data = d)


@app.errorhandler(500)
def server_error(e):
    # Log the error and stacktrace.
    #logging.exception('An error occurred during a request.')
    return 'An internal error occurred.', 500

    sensitive = ndb.FloatProperty()




    


  