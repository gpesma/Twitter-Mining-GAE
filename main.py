import datetime
import webapp2

class MainPage(webapp2.RequestHandler):
	def get(self):
		message = 'ola kala'
		self.response.out.write(message)

application = webapp2.WSGIApplication([('/', MainPage)], debug=True)