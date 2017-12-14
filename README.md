Twitter Mining on Google Platform for Disaster News

Stack
	Google Cloud Platform
	Google API's
	Twitter API
	Flask

Suggested to work on a virtual environment.
Create a Google cloud platform account, and create a project.

On the console create a Compute Engine Instance, Debian 8.
Create a service account and get the credentials in a json file,
and export them in your environment. You will need those api's for
the API's.

In the compute engine install the following API's through pip:
Google Datastore API
Google Natural Language API
Tweepy

Enable the Google API's through the console.

Create a script, as the one found under '/scripts' to stream data,
and save them in your database.  Make sure stream is async.

Alternativaly, and possibly better, use Google API for pub/sub and
create a second script to process the data and store it.

Another option is creating a background process by extending the Daemon class:
https://gist.github.com/josephernest/77fdb0012b72ebdf4c9d19d6256a1119
Pick up to 25 words to track with twitter.

Cron jobs clear old data, and update table with best data, to deploy:
gcloud app deploy cron.yaml

Install dependencies contaned under 'lib'of App Engine with pip.
App engine contains a simlpe get endpoint, and serves a static html,to deploy:
gcloud app deploy

Also run: gcloud app deploy index.yaml

File words.txt contains words that signify 'actions' found in disaster tweets
