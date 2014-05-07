"""
  Class that handles the homepage requests
"""
import basehandler, sys
sys.path.insert(0, './models')
import post
from google.appengine.ext import db

class HomePage(basehandler.BaseHandler):
  def get(self, idx=''):
    if idx and not post.Post.get_by_id(int(idx)):
      self.error(404)
      return
    posts = [post.Post.get_by_id(int(idx))] if idx else db.GqlQuery('SELECT * FROM Post ORDER BY time DESC LIMIT 10')
    self.render('home.html', posts=posts)