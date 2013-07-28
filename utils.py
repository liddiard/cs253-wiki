import os, webapp2, jinja2, hmac
import utils

# convenience functions from which handlers inherit
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
                                autoescape = True)

# cookies

DEV_SECRET = "5ugMk8yy12lMKMMGlRkV" ### IMPORTANT: do not use in production

def makeSecureVal(s):
    hash = hmac.new(s, DEV_SECRET).hexdigest()
    return "%s|%s" % (s, hash)

def checkSecureVal(cookie):
    decomp = cookie.split('|')
    val = decomp[0]
    if makeSecureVal(val) == cookie:
        return val
    else:
        return None

