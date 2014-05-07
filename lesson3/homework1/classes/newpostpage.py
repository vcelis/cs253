"""
  Class that handles the newpost page requests
"""
import basehandler, sys
sys.path.insert(0, './models')
import post

class NewPostPage(basehandler.BaseHandler):
  def get(self):
    self.render('newpost.html')
  def post(self):
    subject, content = self.request.get('subject'), self.request.get('content')
    args = { 'subject': subject, 'content': content }
    if subject and content:
      # do the db magic here
      p = post.Post(title=subject, content=content)
      key = p.put()
      self.redirect('/%d' % key.id())
    else:
      args['error'] = 'Both subject and content are required!'
      self.render('newpost.html', **args)