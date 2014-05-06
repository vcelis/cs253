"""
  Udacity CS253 - Lesson 2 - Homework 2
"""
import webapp2, jinja2, os, re

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir), autoescape = True)
def render_temp(template, **params):
  t = jinja_env.get_template(template)
  return t.render(params)

RE_USER = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
RE_PASS = re.compile(r"^.{3,20}$")
RE_EMAIL = re.compile(r'^[\S]+@[\S]+\.[\S]+$')
def validate_username(username):
  return username and RE_USER.match(username)
def validate_password(password):
  return password and RE_PASS.match(password)
def validate_email(email):
  return not email or RE_EMAIL.match(email)

class BaseHandler(webapp2.RequestHandler):
  def render(self, template, **params):
    self.response.headers['Content-Type'] = "text/html; charset=utf-8"
    self.response.out.write(render_temp(template, **params))

class LoginPage(BaseHandler):
  def get(self):
    self.render('signup.html')
  def post(self):
    username, password, verify, email = self.request.get('username'), self.request.get('password'), self.request.get('verify'), self.request.get('email')
    params, error = {'username': username, 'email': email}, False
    if not validate_username(username):
      params['error_username'] = 'That\'s not a valid username.'
      error = True
    if not validate_password(password):
      params['error_password'] = 'That wasn\'t a valid password.'
      error = True
    elif password != verify:
      params['error_verify'] = 'Your passwords didn\'t match.'
      error = True
    if not validate_email(email):
      params['error_email'] =  'That\'s not a valid email.'
      error = True
    if error:
      self.render('signup.html', **params)
    else:
      self.redirect('/welcome?username=%s' % username)

class WelcomePage(BaseHandler):
  def get(self):
    username = self.request.get('username')
    if validate_username(username):
      self.render('welcome.html', username = username)
    else:
      self.redirect('/')

app = webapp2.WSGIApplication([('/', LoginPage), ('/welcome', WelcomePage)], debug=True)