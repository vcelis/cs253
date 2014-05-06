"""
  Udacity CS253 - Lesson 2 - Homework 1
"""
import webapp2

class Rot13Page(webapp2.RequestHandler):
  base = """
  <!DOCTYPE>
  <html>
  <head>
  <title>ROT13</title>
  </head>
  <body>
  <h2>Enter some text to ROT13</h2>
  <form method="POST">
  <textarea name="text" style="height: 100px; width: 400px; display: block;">%(text)s</textarea>
  <input type="submit">
  </form>
  </body>
  </html>
  """
  
  def __draw_form(self, text=''):
    self.response.write(self.base % {'text': text})
  
  def __rot13(self, s):
    chars = [ord(c) for c in s]
    for i, c in enumerate(chars):
      if c >= 65 and c <= 90:
        chars[i] += 13
        if chars[i] > 90:
          chars[i] -= 26
      elif c >= 97 and c <= 122:
        chars[i] += 13
        if chars[i] > 122:
          chars[i] -= 26
    return "".join([chr(c) for c in chars])

  def get(self):
    self.__draw_form()

  def post(self):
    import cgi
    text = self.__rot13(self.request.get('text'))
    self.__draw_form(cgi.escape(text, quote = True))

app = webapp2.WSGIApplication([('/', Rot13Page)], debug=True)