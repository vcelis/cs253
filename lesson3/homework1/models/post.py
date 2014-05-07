"""
  Class to model the post object
"""
from google.appengine.ext import db
class Post(db.Model):
  title = db.StringProperty(required = True)
  content = db.TextProperty(required = True)
  time = db.DateTimeProperty(auto_now_add = True)