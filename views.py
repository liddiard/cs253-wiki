import utils, models
import logging # TODO: remove in production

class ViewPage(utils.Handler):
    def get(self, slug):
        logged_in = utils.validLogon(self)
        if not models.pageExists(slug) and logged_in:
            self.redirect('../_edit/%s' % slug)
        else:
            self.render("view.html", login=logged_in)
    
    def post(self):
        username = self.request.get('username')
        password = self.request.get('password')
        if models.validCredentials(username, password):
            user_cookie = utils.makeSecureVal(username)
            utils.setCookie(self, key="username", val=user_cookie)
            self.write("valid")
        else:
            self.write("invalid login credentials")

class EditPage(utils.Handler):
    def get(self, slug):
        logged_in = utils.validLogon(self)
        if logged_in:
            self.render("edit.html", login=logged_in)
        else:
            self.redirect('../../%s' % slug)
    
    def post(self):
        pass

class Register(utils.Handler):
    def get(self):
        self.render("register.html")
    
    def post(self):
        username = self.request.get('username')
        password = self.request.get('password')
        verify = self.request.get('verify')
        email = self.request.get('email')
        
        errors = utils.createErrorArgs(utils.usernameError(username),
                              utils.passwordsError(password, verify),
                              utils.emailError(email))
        
        if errors is None: # registration successful
            pw_hash = utils.makePasswordHash(username, password)
            models.addUser(username, pw_hash, email)
            user_cookie = utils.makeSecureVal(username)
            utils.setCookie(self, key="username", val=user_cookie)
            self.redirect("/signup/success/")
        
        else: # registration unsuccessful
            self.render("register.html", username=username, password=password, 
                        verify=verify, email=email, errors=errors)

class RegisterSuccess(utils.Handler):
    def get(self):
        if utils.validLogon(self):
            self.render("register_success.html",
                        username=utils.getUsername(self))
                # doesn't take into account browser disallowing cookies?
        else:
            self.redirect("/signup/")

class Login(utils.Handler):
    pass