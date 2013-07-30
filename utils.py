import os, webapp2, jinja2, hmac, re

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
    h = hmac.new(s, DEV_SECRET).hexdigest()
    return "%s|%s" % (s, h)

def checkSecureVal(cookie):
    decomp = cookie.split('|')
    val = decomp[0]
    if makeSecureVal(val) == cookie:
        return val

def checkValidLogon(username):
    if username:
        return checkSecureVal(username)
    
def setUserCookie(obj, username):
    '''"obj" should always be the "self" attribute from a request handler'''
    obj.response.header.add_header(str('Set-Cookie'),
                                   str('username='+username+'; Path=/'))

# field validation
def matchRegex(field, regex):
    if regex.match(field):
        return True
    else:
        return False

def usernameError(username):
    USER_RE = re.compile(r'^[a-zA-Z0-9_-]{3,20}$')
    if not matchRegex(username, USER_RE):
        return "invalid"
    elif False: # check if username already in datastore
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
    
    return ', '.join(errors)