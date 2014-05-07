"""
  Abstract base class to be inherited by the page handler classes
"""
import webapp2, jinja2, os
class BaseHandler(webapp2.RequestHandler):
  template_dir = os.path.join(os.path.dirname(__file__), '../templates')
  jinja = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir), autoescape=True)
  def render(self, template, **params):
    self.response.headers['Content-Type'] = 'text/html; charset=utf-8'
    self.response.out.write(self.jinja.get_template(template).render(params))