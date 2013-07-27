import webapp2, utils
from google.appengine.ext import db

class Page(db.Model):
    body = db.TextProperty()
    created = db.DateTimeProperty(auto_now_add=True)
    modified = db.DateTimeProperty(auto_now=True)
    last_modified_by = db.StringProperty()