import os, webapp2, jinja2, hmac, re, random, string, hashlib
import models

# convenience functions from which handlers can inherit
class Handler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

# set the jinja2 template directory
template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
                                autoescape = True, 
                                extensions = ['jinja2.ext.autoescape'])

# cookies
DEV_SECRET = "5ugMk8yy12lMKMMGlRkV" ### IMPORTANT: do not use in production

def makeSecureVal(s):
    string = str(s)
    h = hmac.new(string, DEV_SECRET).hexdigest()
    return "%s|%s" % (string, h)

def checkSecureVal(cookie):
    decomp = cookie.split('|')
    val = decomp[0]
    if makeSecureVal(val) == cookie:
        return True
    else:
        return False

def validLogon(handler):
    u_cookie = handler.request.cookies.get('username')
    if u_cookie:
        return checkSecureVal(u_cookie)

def setCookie(handler, key, val):
    handler.response.headers.add_header(str('Set-Cookie'),
                                   str('%s=%s; Path=/' % (key, val)))

def getCookie(handler, key):
    return handler.request.cookies.get(key)

def getUsername(handler):
    u_cookie = handler.request.cookies.get('username')
    if u_cookie:
        return u_cookie.split('|')[0]
    else:
        return None

# field validation
def matchRegex(field, regex):
    return regex.match(field)

def usernameError(username):
    USER_RE = re.compile(r'^[a-zA-Z0-9_-]{3,20}$')
    if not matchRegex(username, USER_RE):
        return "invalid"
    elif models.userExists(username):
        return "taken"
    else:
        return False

def passwordsError(password, verify):
    PASS_RE = re.compile(r'^.{3,20}$')
    if not matchRegex(password, PASS_RE):
        return "invalid"
    elif password != verify:
        return "mismatch"
    else:
        return False

def emailError(email):
    EMAIL_RE = re.compile(r'^[\S]+@[\S]+\.[\S]+$')
    if email == "":
        return False
    elif not matchRegex(email, EMAIL_RE):
        return "invalid"
    else:
        return False

def createErrorArgs(username, passwords, email):
    errors = []
    if username == "invalid":
        errors.append("\"#username\"")
    elif username == "taken":
        errors.append("\"#username-taken\"")
    if passwords == "invalid":
        errors.append("\"#password\"")
    elif passwords == "mismatch":
        errors.append("\"#verify\"")
    if email == "invalid":
        errors.append("\"#email\"")
    
    if len(errors) == 0:
        return None
    else:
        return ', '.join(errors)

# password hashing
def makeSalt():
    return "".join([random.choice(string.ascii_letters)
            for letter in xrange(5)])

def makePasswordHash(username, password, salt=None):
    if not salt:
        salt = makeSalt()
    h = hashlib.sha256(username + password + salt).hexdigest()
    return "%s,%s" % (h, salt)

def validPassword(username, password, h):
    salt = h.split(',')[1]
    return h == makePasswordHash(username, password, salt)