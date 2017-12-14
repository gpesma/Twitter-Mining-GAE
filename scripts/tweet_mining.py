#! /usr/bin/python
# From "A simple unix/linux daemon in Python" by Sander Marechal 
# See http://stackoverflow.com/a/473702/1422096
#
# Modified to add quit() that allows to run some code before closing the daemon
# See http://stackoverflow.com/a/40423758/1422096
#
# Joseph Ernest, 2016/11/12

import six
import sys, os, time, atexit
from signal import signal, SIGTERM 
import tweepy
import os
import json
import re
from google.cloud import datastore
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from google.cloud import language
import re


client = datastore.Client("comp150-confluence")

access_token = "925901916512641026-IMcQ5hTUfyfZp0hAWxBjKDPQxhmfdHE"
access_token_secret = "FYLFqjWgxvcycDhQl9I16bhwz4Hk7iHyuvxOgIq76QH7W"
consumer_key = "HY3HknvpInVkE1ZvYkJKrbuXL"
consumer_secret = "cik2gh2BKduNfbk1hE3eOe2HfAW3gdkniGtitmTYZvPive6ViR"


class StdOutListener(StreamListener):

    def on_data(self, data):
	

		emoji_pattern = re.compile("["
        		u"\U0001F600-\U0001F64F"  # emoticons
      			  u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        		u"\U0001F680-\U0001F6FF"  # transport & map symbols
        		u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                           "]+", flags=re.UNICODE)
		

		def extract_link(text):
			regex = r'https?://[^\s<>"]+|www\.[^\s<>"]+'
			match = re.search(regex, text)
			if match:
				return match.group()
			return 'no link'

		def classify_text(text):
	        	c = language.LanguageServiceClient()
	        	if isinstance(text, six.binary_type):
	                	text = text.decode('utf-8')
                
			document = language.types.Document(
          		content=text,
           		type=language.enums.Document.Type.PLAIN_TEXT,
				language='en')

	        	categories = c.classify_text(document).categories
			sens_conf = None
	        	news_conf = None

		  	for category in categories:
				if 'ensitive' in category.name:
					sens_conf = category.confidence
			return sens_conf

		tweet = json.loads(data)['text']

		cur_link = extract_link(tweet)
		if cur_link == 'no link':
			return True
		tweet = tweet.strip(cur_link)
		tweet = emoji_pattern.sub(r'', unicode(tweet))
		tweet_cat = tweet
		if len(tweet_cat.split()) >= 5:
			while len(tweet_cat.split()) < 20:
				tweet_cat = tweet_cat + " " + tweet_cat
			c1 = classify_text(tweet_cat)		
		else:
			c1 = None	
		if c1 is not None and c1 > 0.5:	

			key = client.key('Tweet')
			new_tweet = datastore.Entity(key)
		      	new_tweet.update({
			        'text': tweet,
				'url': cur_link,
				'time': json.loads(data)['created_at'],
				'sensitive': c1,
				'likes': json.loads(data)['favorite_count'] + json.loads(data)['retweet_count']
			})

			client.put(new_tweet)                     
			print tweet		
		
		return True
		def on_error(self, status):
			print "error"
		    

l = StdOutListener()
auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)
stream = Stream(auth, l)
counter = 0
stream.filter(track=['disaster', 'tragic', 'killed'], languages = ['en'], async=True)
