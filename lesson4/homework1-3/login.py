"""
  Udacity CS253 - Lesson 4 - Homework 1
"""
import webapp2, jinja2, os, handlers

app = webapp2.WSGIApplication([
  ('/signup', handlers.SignupPage),
  ('/welcome', handlers.WelcomePage),
  ('/login', handlers.LoginPage),
  ('/logout', handlers.LogoutPage)
  ], debug=True)