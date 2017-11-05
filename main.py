import webapp2
import jinja2
import os
import twitter_processing

class MainPage(webapp2.RequestHandler):
	def get(self):
		template = template_env.get_template('home.html')
		twitter_data = twitter_processing.do_stuff()
		context = { 'data': twitter_data}
		self.response.out.write(template.render(context))

application = webapp2.WSGIApplication([('/', MainPage)], debug=True)