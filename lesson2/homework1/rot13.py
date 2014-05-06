"""
  Udacity CS253 - Lesson 2 - Homework 1
"""
import webapp2, jinja2, os

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape = True)

def render_temp(template, **params):
  t = jinja_env.get_template(template)
  return t.render(params)

class BaseHandler(webapp2.RequestHandler):
  def render(self, template, **params):
    self.response.out.write(render_temp(template, **params))

class Rot13Page(BaseHandler):
  def get(self):
    self.render('form.html')

  def post(self):
    r, text = '', self.request.get('text')
    if text:
      r = text.encode('rot13')
    self.render('form.html', text=r)

app = webapp2.WSGIApplication([('/', Rot13Page)], debug=True)