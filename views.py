import utils, models

class ViewPage(utils.Handler):
    def get(self):
        logged_in = utils.validLogon(self)
        self.render("view.html", login=logged_in)

class EditPage(utils.Handler):
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
            models.addUser(username, password, email)
                # TODO IMPORTANT: passwords should not be stored in plaintext
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