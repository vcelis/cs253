import random, hashlib, hmac, string, logging
from datetime import datetime, timedelta

from google.appengine.ext import db
from google.appengine.ext import ndb
from google.appengine.api import memcache

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

  @staticmethod
  def get_key(group = 'default'):
    return db.Key.from_path('posts', group)

  @classmethod
  def get_id(cls, idx, update=False):
    post, age = Post.get_cache(str(idx))
    if update or post is None:
      logging.error('-------------DB HIT------------')
      k = db.Key.from_path('Post', idx, parent=Post.get_key())
      post = db.get(k)
      Post.set_cache(str(idx), post)
    return [post], Post.age_to_str(age)
  @classmethod
  def get_last(cls, i, update=False):
    key = 'TOP_10'
    posts, age = Post.get_cache(key)
    if update or posts is None:
      logging.error('---------DB HIT------------')
      posts = list(Post.all().order('-last_modified').fetch(limit=10))
      Post.set_cache(key, posts)
    return posts, Post.age_to_str(age)
  @classmethod
  def get_all(cls):
    return db.GqlQuery('SELECT * FROM Post')
  @classmethod
  def create(cls, subject, content):
    p = cls(parent=Post.get_key(), subject=subject, content=content)
    return p


  @staticmethod
  def set_cache(key, val):
    now = datetime.utcnow()
    memcache.set(key, (val, now))
  @staticmethod
  def get_cache(key):
    r = memcache.get(key)
    return (r[0], (datetime.utcnow()-r[1]).total_seconds()) if r else (None, 0)

  @staticmethod
  def age_to_str(age):
    s = 'queried %s seconds ago'
    age = int(age)
    if age == 1:
      s = s.replace('seconds', 'second')
    return s % age
  @staticmethod
  def flush_cache():
    memcache.flush_all()