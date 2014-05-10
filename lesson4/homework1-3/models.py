"""
  Models the User entity for the datastore
"""
import random, hashlib, hmac, string
from google.appengine.ext import db

class User(db.Model):
  name = db.StringProperty(required = True)
  pw = db.StringProperty(required = True)
  email = db.StringProperty()

  @staticmethod
  def get_key(group = 'default'):
    """ Returns the key to the parent - For future grouping of users """
    return db.Key.from_path('users', group)

  """ Cookies static methods """
  __COOKIE_SALT = r'Z}QKEA~Qe.f4&uz,t@XXbA.>(~RY>ZcYUPK45Udz<f.=;n3Gn)dFKf&M*.S2tqT}'
  @staticmethod
  def gen_cookie(uid):
    return '%s|%s' % (uid, hmac.new(User.__COOKIE_SALT, str(uid)).hexdigest())
  @staticmethod
  def check_cookie(raw):
    uid = raw.split('|')[0]
    return uid if raw == User.gen_cookie(uid) else None

  """ PW """
  @staticmethod
  def gen_salt(length = 5):
    """ Returns a salt of a given length """
    return ''.join(random.choice(string.letters) for x in xrange(length))
  @staticmethod
  def gen_pw_hash(name, pw, salt = None):
    """ Returns a string of the form 'salt|HASH(name + pw +salt)' to store """
    salt = salt if salt else User.gen_salt()
    return '%s|%s' % (salt, hashlib.sha256(name + pw + salt).hexdigest())
  
  @classmethod
  def get_id(cls, uid):
    """ Get's a entity by id """
    return User.get_by_id(long(uid), parent = User.get_key())
  @classmethod
  def get_name(cls, name):
    """ Get's a entity by name """
    return User.all().filter('name = ', name).get()
  @classmethod
  def register(cls, name, pw, email = None):
    """ Returns an instance of this entity - DOES NOT COMMIT (PUT) """
    pw = User.gen_pw_hash(name, pw)
    return cls(parent = User.get_key(), name = name, pw = pw, email = email)
  @classmethod
  def login(cls, name, pw):
    """ Returns the instance of the entity if it exists and pw is correct """
    u = User.get_name(name)
    return u if u and u.pw == User.gen_pw_hash(name, pw, u.pw.split('|')[0]) else None