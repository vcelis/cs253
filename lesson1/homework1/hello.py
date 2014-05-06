"""
  Udacity CS253 - Lessen 1 - Homework 1
"""
import webapp2

class MainPage(webapp2.RequestHandler):
  def get(self):
    self.response.headers['Content-Type'] = 'text/plain'
    self.response.write('Hello, Udacity!')

application = webapp2.WSGIApplication([('/', MainPage),], debug=True)