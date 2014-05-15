"""
  Classes to handle the requests
"""
import webapp2, jinja2, os, re, json
from models import User, Post



import time, logging
"""
  Abstract handler classes
"""
class BaseHandler(webapp2.RequestHandler):
  template_dir = os.path.join(os.path.dirname(__file__), 'templates')
  jinja = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir), autoescape=True)
  def render(self, template, **params):
    self.response.headers['Content-Type'] = 'text/html; charset=utf-8'
    self.response.out.write(self.jinja.get_template(template).render(params))
  def set_cookie(self, name, value):
    self.response.headers.add_header('Set-Cookie', '%s=%s; Path=/' % (name, value))
  def del_cookie(self, name):
    self.response.headers.add_header('Set-Cookie', '%s=; Path=/' % name)
  def check_login(self):
    c = self.request.cookies.get('uid')
    if c and User.check_cookie(c):
      u = User.get_id(c.split('|')[0])
      return u

class FormHandler():
  RE_USERNAME = re.compile(r'^[a-zA-Z0-9_-]{3,20}$')
  RE_PASSWORD = re.compile(r'^.{3,20}$')
  RE_EMAIL = re.compile(r'^[\S]+@[\S]+\.[\S]+$')

  def validate_username(self, username):
    return username and self.RE_USERNAME.match(username)
  def validate_password(self, password):
    return password and self.RE_PASSWORD.match(password)
  def validate_email(self, email):
    return not email or self.RE_EMAIL.match(email)
  def validate_signup(self, **raw):
    error, params = False, {'username': raw['username'], 'email': raw['email']}
    if not self.validate_username(raw['username']):
      params['error_username'] = 'That\'s not a valid username.'
      error = True
    if not self.validate_password(raw['password']):
      params['error_password'] = 'That wasn\'t a valid password.'
      error = True
    elif raw['password'] != raw['verify']:
      params['error_verify'] = 'Your passwords didn\'t match.'
      error = True
    if not self.validate_email(raw['email']):
      params['error_email'] =  'That\'s not a valid email.'
      error = True
    return (error, params)
  def validate_login(self, **raw):
    error, params = False, {'username': raw['username'], 'password': raw['password']}
    if not self.validate_username(raw['username']):
      params['error_username'] = 'That\'s not a valid username.'
      error = True
    if not raw['password']:
      params['error_password'] = 'You didn\'t enter any password.'
      error = True
    return (error, params)
  def validate_post(self, **raw):
    error, params = False, {'subject': raw['subject'], 'content': raw['content'] }
    if not (params['subject'] and params['content']):
      params['error'] = 'Both subject and content are required!'
      error = True
    return (error, params)
"""
  Page handlers
"""
######### Blog #########
class HomePage(BaseHandler):
  def get(self, idx=''):
    # User
    user = self.check_login()
    params = { 'user': user }
    # Paramlink
    if idx and not Post.get_id(int(idx)):
      self.error(404)
      return
    if idx:
      params['posts'], params['age'] = Post.get_id(int(idx))
    else:
      params['posts'], params['age'] = Post.get_last(10)
    self.render('home.html', **params)

class NewPostPage(BaseHandler, FormHandler):
  def get(self):
    self.render('newpost.html')
  def post(self):
    raw = { field: self.request.get(field) for field in ['subject', 'content'] }
    error, params = self.validate_post(**raw)
    if error:
      self.render('newpost.html', **params)
    else:
      p = Post.create(raw['subject'], raw['content'])
      p.put()
      time.sleep(0.1)
      Post.get_last(10, update=True)
      self.redirect('/%s' % p.key().id())

### JSON ###
class JsonPage(BaseHandler):
  def get(self, idx=''):
    if idx:
      r = Post.get_id(int(idx)).as_dict()
    else:
      r = [x.as_dict() for x in Post.get_all()]
    p = Post.get_id(int(idx)) if idx else Post.get_all()
    self.response.headers['Content-Type'] = 'application/json; charset=utf-8'
    self.response.out.write(json.dumps(r))

######### User #########
class SignupPage(BaseHandler, FormHandler):
  def get(self):
    self.render('signup.html')
  def post(self):
    raw = { field: self.request.get(field) for field in ['username', 'password', 'verify', 'email'] }
    error, params = self.validate_signup(**raw)
    if error:
      self.render('signup.html', **params)
    else:
      if User.get_name(raw['username']):
        params['error_username'] = 'That username already exists.'
        self.render('signup.html', **params)
      else:
        u = User.register(raw['username'], raw['password'], raw['email'])
        u.put()
        self.set_cookie('uid', User.gen_cookie(u.key().id()))
        self.redirect('/welcome')

class LoginPage(BaseHandler, FormHandler):
  def get(self):
    self.render('login.html')
  def post(self):
    raw = { field: self.request.get(field) for field in ['username', 'password'] }
    error, params = self.validate_login(**raw)
    if error:
      self.render('login.html', **params)
    else:
      u = User.login(raw['username'], raw['password'])
      if u:
        self.set_cookie('uid', User.gen_cookie(u.key().id()))
        self.redirect('/welcome')
      else:
        params['error_login'] = 'Invalid username and/or password'
        self.render('login.html', **params)

class LogoutPage(BaseHandler):
  def get(self):
    self.del_cookie('uid')
    self.redirect('/signup')

class WelcomePage(BaseHandler):
  def get(self):
    u = self.check_login()
    if u:
      params = {'username': u.name}
      self.render('welcome.html', **params)
    else:
      self.del_cookie('uid')
      self.redirect('/login')

class FlushCachePage(webapp2.RequestHandler):
  def get(self):
    Post.flush_cache()
    self.redirect('/')
