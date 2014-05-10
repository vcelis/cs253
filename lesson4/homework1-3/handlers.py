"""
  Classes to handle the requests
"""
import webapp2, jinja2, os, re
from google.appengine.ext import db
from models import User

class BaseHandler(webapp2.RequestHandler):
  """
    Base handler with comon functions
  """
  template_dir = os.path.join(os.path.dirname(__file__), 'templates')
  jinja = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir), autoescape=True)
  def render(self, template, **params):
    self.response.headers['Content-Type'] = 'text/html; charset=utf-8'
    self.response.out.write(self.jinja.get_template(template).render(params))
class LoginHandler(BaseHandler):
  """
    Abstract class to handle login 
  """
  def set_cookie(self, value):
    self.response.headers.add_header('Set-Cookie', 'uid=%s; Path=/' % (value))
  def delete_cookie(self):
    self.response.headers.add_header('Set-Cookie', 'uid=; Path=/')

  # Form handling
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

class SignupPage(LoginHandler):
  def get(self):
    self.render('signup.html')
  def post(self):
    raw = { field: self.request.get(field) for field in ['username', 'password', 'verify', 'email'] }
    error, params = self.validate_signup(**raw)
    if error:
      self.render('signup.html', **params)
    else:
      # Check if a user with that username already exists
      if User.get_name(raw['username']):
        params['error_username'] = 'That username already exists.'
        self.render('signup.html', **params)
      else:
        u = User.register(raw['username'], raw['password'], raw['email'])
        u.put()
        self.set_cookie(User.gen_cookie(u.key().id()))
        self.redirect('/welcome')

class LoginPage(LoginHandler):
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
        self.set_cookie(User.gen_cookie(u.key().id()))
        self.redirect('/welcome')
      else:
        params['error_login'] = 'Invalid username and/or password'
        self.render('login.html', **params)

class LogoutPage(LoginHandler):
  def get(self):
    self.delete_cookie()
    self.redirect('/signup')

class WelcomePage(BaseHandler):
  def get(self):
    cookie = self.request.cookies.get('uid')
    if cookie and User.check_cookie(cookie):
      u = User.get_id(cookie.split('|')[0])
      params = {'username': u.name}
      self.render('welcome.html', **params)
    else:
      params = {'error_login': 'A security error occured. Please login again.'}
      self.render('login.html', **params)