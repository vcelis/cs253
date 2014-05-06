"""
  Udacity CS253 - Lesson 2 - Homework 2
"""
import webapp2

class LoginPage(webapp2.RequestHandler):
  base = """
  <!DOCTYPE html>
  <html>
  <head>
  <title>Login</title>
  <style type="text/css">
  .label {text-align: right;}
  .error {color: red;}
  </style>
  </head>
  <body>
  <h2>Signup</h2>
  <form method="POST">
  <table>
  <tr>
  <td class="label">Username</td>
  <td><input type="text" name="username" value="%(username)s"></td>
  <td class="error">%(username_error)s</td>
  </tr>
  <tr>
  <td class="label">Password</td>
  <td><input type="password" name="password" value=""></td>
  <td class="error">%(password_error)s</td>
  </tr>
  <tr>
  <td class="label">Verify Password</td>
  <td><input type="password" name="verify" value=""></td>
  <td class="error">%(verify_error)s</td>
  </tr>
  <tr>
  <td class="label">Email (optional)</td>
  <td><input type="text" name="email" value="%(email)s"></td>
  <td class="error">%(email_error)s</td>
  </tr>
  </table>
  <input type="submit">
  </form>
  </body>
  </html>
  """
  def __check_username(usrname):
    
  def __draw_form(self, username='', email='', username_error='', password_error='', verify_error='', email_error=''):
    self.response.write(self.base % {'username': username, 'email': email, 'username_error': username_error, 'password_error': password_error, 'verify_error': verify_error, 'email_error': email_error})
  def get(self):
    self.__draw_form()
  def post(self):
    self.redirect('/welcome')

class WelcomePage(webapp2.RequestHandler):
  base = """
  <!DOCTYPE html>
  <html>
  <head>
  <title>Welcome</title>
  </head>
  <body>
  <h2>Welcome %(username)s</h2>
  </body>
  </html>
  """
  def get(self):
    self.response.write(self.base % {'username': self.request.get('username')})

app = webapp2.WSGIApplication([('/', LoginPage), ('/welcome', WelcomePage)], debug=True)