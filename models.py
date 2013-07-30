import webapp2, utils
from google.appengine.ext import db

class User(db.Model):
    username = db.StringProperty(required=True)
    password = db.StringProperty(required=True)
    email = db.StringProperty(required=False)

    def addUser(username, password, email=None):
        u = User(username, password, email)
        u.put()

class Page(db.Model):
    body = db.TextProperty()
    created = db.DateTimeProperty(auto_now_add=True)
    modified = db.DateTimeProperty(auto_now=True)
    last_modified_by = db.StringProperty()