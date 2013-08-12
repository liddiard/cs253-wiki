import webapp2, utils
from google.appengine.ext import db

class User(db.Model):
    username = db.StringProperty(required=True)
    password = db.StringProperty(required=True)
    email = db.StringProperty(required=False)

def addUser(username, pw_hash, email=None):
    u = User(username=username, password=pw_hash, email=email)
    u.put()

def userExists(username):
    q = User.all().filter('username =', username)
    user = q.get()
    if user is None:
        return False
    else:
        return user

def validCredentials(username, password):
    user = userExists(username)
    if user:
        h = user.password
        return utils.validPassword(username, password, h)
    else:
        return False

class Page(db.Model):
    slug = db.StringProperty()
    body = db.TextProperty()
    created = db.DateTimeProperty(auto_now_add=True)
    modified = db.DateTimeProperty(auto_now=True)
    last_modified_by = db.StringProperty()

def updatePage(slug, content, user):
    page = pageExists(slug)
    if page:
        page.body = content
        page.last_modified_by = user
    else:
        p = Page(slug=slug, body=content, last_modified_by=user)
        p.put()

def pageExists(slug):
    q = Page.all().filter('slug =', slug)
    page = q.get()
    if page is None:
        return False
    else: 
       return page

def getPageContent(slug):
    q = Page.all().filter('slug =', slug)
    page = q.get()
    if page is None:
        return ""
    else:
        return page.body