"""
  Udacity CS253 - Lesson 5 - Homework 1
"""
import webapp2, handlers

app = webapp2.WSGIApplication([
  ('/', handlers.HomePage),
  ('/newpost', handlers.NewPostPage),
  ('/signup', handlers.SignupPage),
  ('/login', handlers.LoginPage),
  ('/logout', handlers.LogoutPage),
  ('/welcome', handlers.WelcomePage)
  ], debug=True)