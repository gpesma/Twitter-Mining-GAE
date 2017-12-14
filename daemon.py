#! /usr/bin/python
# From "A simple unix/linux daemon in Python" by Sander Marechal 
# See http://stackoverflow.com/a/473702/1422096
#
# Modified to add quit() that allows to run some code before closing the daemon
# See http://stackoverflow.com/a/40423758/1422096
#
# Joseph Ernest, 2016/11/12
# Edit George Pesmazoglou 2017/12/10

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

class Daemon:
	"""
	A generic daemon class.
	
	Usage: subclass the Daemon class and override the run() method
	"""
	def __init__(self, pidfile='_.pid', stdin='/dev/null', stdout='/dev/null', stderr='/dev/null'):
		self.stdin = stdin
		self.stdout = stdout
		self.stderr = stderr
		self.pidfile = pidfile
	
	def daemonize(self):
		"""
		do the UNIX double-fork magic, see Stevens' "Advanced 
		Programming in the UNIX Environment" for details (ISBN 0201563177)
		http://www.erlenstar.demon.co.uk/unix/faq_2.html#SEC16
		"""
		count = 0

		try: 
			pid = os.fork() 
			if pid > 0:
				# exit first parent
				sys.exit(0) 
		except OSError, e: 
			sys.stderr.write("fork #1 failed: %d (%s)\n" % (e.errno, e.strerror))
			sys.exit(1)
	
		# decouple from parent environment
		os.setsid() 
		os.umask(0) 
	
		# do second fork
		try: 
			pid = os.fork() 
			if pid > 0:
				# exit from second parent
				sys.exit(0) 
		except OSError, e: 
			sys.stderr.write("fork #2 failed: %d (%s)\n" % (e.errno, e.strerror))
			sys.exit(1) 
	
		# redirect standard file descriptors
		sys.stdout.flush()
		sys.stderr.flush()
	
		si = file(self.stdin, 'r')
		so = file(self.stdout, 'a+')
		se = file(self.stderr, 'a+', 0)

		atexit.register(self.onstop)
		signal(SIGTERM, lambda signum, stack_frame: exit())
        	
		# write pidfile        
		pid = str(os.getpid())
		file(self.pidfile,'w+').write("%s\n" % pid)

		
		access_token = "925901916512641026-IMcQ5hTUfyfZp0hAWxBjKDPQxhmfdHE"
        access_token_secret = "FYLFqjWgxvcycDhQl9I16bhwz4Hk7iHyuvxOgIq76QH7W"
        consumer_key = "HY3HknvpInVkE1ZvYkJKrbuXL"
        consumer_secret = "cik2gh2BKduNfbk1hE3eOe2HfAW3gdkniGtitmTYZvPive6ViR"
        client = datastore.Client("comp150-confluence")
		
		
		class StdOutListener(StreamListener):

		    def on_data(self, data):
				
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
			    return True
		                
		

        l = StdOutListener()
        auth = OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        api = tweepy.API(auth)
        stream = Stream(auth, l)
        #fill in the keywords
        stream.filter(track=["disaster"], languages = ['en'], async=True)


	
	def onstop(self):
		self.quit()
		os.remove(self.pidfile)

	def run(self):
		
		'''
		#Variables that contains the user credentials to access Twitter API 
		access_token = "925901916512641026-IMcQ5hTUfyfZp0hAWxBjKDPQxhmfdHE"
		access_token_secret = "FYLFqjWgxvcycDhQl9I16bhwz4Hk7iHyuvxOgIq76QH7W"
		consumer_key = "HY3HknvpInVkE1ZvYkJKrbuXL"
		consumer_secret = "cik2gh2BKduNfbk1hE3eOe2HfAW3gdkniGtitmTYZvPive6ViR"
		client = create_client("comp150-confluence")
		class StdOutListener(StreamListener):
		    def on_data(self, data):
		        tweet = json.loads(data)['text']
		        key = client.key('Tweet')
		        new_tweet = datastore.Entity(key)
		        new_tweet.update({
		        	'text': tweet
		        	})
		        client.put(new_tweet)
		        print new_tweet['text']
		        return True
		    def on_error(self, status):
		        print status

		l = StdOutListener()
		auth = OAuthHandler(consumer_key, consumer_secret)
		auth.set_access_token(access_token, access_token_secret)
		api = tweepy.API(auth)
		stream = Stream(auth, l)
		stream.filter(track=['hello'])
		'''

	def start(self):
		"""
		Start the daemon
		"""
		# Check for a pidfile to see if the daemon already runs
		try:
			pf = file(self.pidfile,'r')
			pid = int(pf.read().strip())
			pf.close()
		except IOError:
			pid = None
	
		if pid:
			message = "pidfile %s already exist. Daemon already running?\n"
			sys.stderr.write(message % self.pidfile)
			sys.exit(1)
		
		# Start the daemon
		self.daemonize()
		self.run()

	def stop(self):
		"""
		Stop the daemon
		"""
		# Get the pid from the pidfile
		try:
			pf = file(self.pidfile,'r')
			pid = int(pf.read().strip())
			pf.close()
		except IOError:
			pid = None
	
		if not pid:
			message = "pidfile %s does not exist. Daemon not running?\n"
			sys.stderr.write(message % self.pidfile)
			return # not an error in a restart

		# Try killing the daemon process	
		try:
			while 1:
				os.kill(pid, SIGTERM)
				time.sleep(0.1)
		except OSError, err:
			err = str(err)
			if err.find("No such process") > 0:
				if os.path.exists(self.pidfile):
					os.remove(self.pidfile)
			else:
				print str(err)
				sys.exit(1)

	def restart(self):
		"""
		Restart the daemon
		"""
		self.stop()
		self.start()

	def quit(self):
		
