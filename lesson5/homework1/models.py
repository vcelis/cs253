import random, hashlib, hmac, string
from google.appengine.ext import db

COOKIE_SALT = r'Z}QKEA~Qe.f4&uz,t@XXbA.>(~RY>ZcYUPK45Udz<f.=;n3Gn)dFKf&M*.S2tqT}'

class User(db.Model):
  name = db.StringProperty(required=True)
  pw = db.StringProperty(required=True)
  email = db.StringProperty()

  @staticmethod
  def get_key(group = 'default'):
    return db.Key.from_path('users', group)
  
  @staticmethod
  def gen_cookie(uid):
    return '%s|%s' % (uid, hmac.new(COOKIE_SALT, str(uid)).hexdigest())
  @staticmethod
  def check_cookie(raw):
    uid = raw.split('|')[0]
    return uid if raw == User.gen_cookie(uid) else None

  @staticmethod
  def gen_salt(length = 5):
    return ''.join(random.choice(string.letters) for x in xrange(length))
  @staticmethod
  def gen_pw_hash(name, pw, salt = None):
    salt = salt if salt else User.gen_salt()
    return '%s|%s' % (salt, hashlib.sha256(name + pw + salt).hexdigest())
  
  @classmethod
  def get_id(cls, uid):
    return User.get_by_id(long(uid), parent = User.get_key())
  @classmethod
  def get_name(cls, name):
    return User.all().filter('name = ', name).get()
  @classmethod
  def register(cls, name, pw, email = None):
    pw = User.gen_pw_hash(name, pw)
    return cls(parent = User.get_key(), name = name, pw = pw, email = email)
  @classmethod
  def login(cls, name, pw):
    u = User.get_name(name)
    return u if u and u.pw == User.gen_pw_hash(name, pw, u.pw.split('|')[0]) else None

class Post(db.Model):
  subject = db.StringProperty(required=True)
  content = db.TextProperty(required=True)
  created = db.DateTimeProperty(auto_now_add=True)
  last_modified = db.DateTimeProperty(auto_now=True)

  def as_dict(self):
    return dict(
      subject=self.subject,
      content=self.content,
      created=self.created.strftime(r'%a %b %e %H:%M:%S %Y'),
      last_modified=self.last_modified.strftime(r'%a %b %e %H:%M:%S %Y')
      )

  @classmethod
  def get_id(cls, idx):
    return Post.get_by_id(idx)
  @classmethod
  def get_last(cls, i):
    return db.GqlQuery('SELECT * FROM Post ORDER BY last_modified DESC LIMIT %d' % i)
  @classmethod
  def get_all(cls):
    return db.GqlQuery('SELECT * FROM Post')
  @classmethod
  def create(cls, subject, content):
    return cls(subject=subject, content=content)