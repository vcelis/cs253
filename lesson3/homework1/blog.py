"""
  Udacity CS253 - Lesson 3 - Homework 1
"""
import webapp2, sys
sys.path.insert(0, './classes')
import homepage, newpostpage

app = webapp2.WSGIApplication([
    ('/', homepage.HomePage),
    ('/newpost', newpostpage.NewPostPage),
    (r'/(\d+)', homepage.HomePage)
    ], debug=True)