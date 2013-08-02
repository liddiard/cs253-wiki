import utils, models

class ViewPage(utils.Handler):
    def get(self):
        username = self.request.cookies.get('username')
        if utils.checkValidLogon(username):
            login = True
        self.render("edit.html", login=False)

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
            utils.setCookie(self, "username", username)
            self.redirect("/signup/success/")
            
        else: # registration unsuccessful
            self.render("register.html", username=username, password=password, 
                        verify=verify, email=email, errors=errors)
            
class RegisterSuccess(utils.Handler):
    def get(self):
        valid_cookie = utils.checkSecureVal(utils.getCookie('username'))
        if valid_cookie:
            self.render("register_success.html")
        else:
            self.redirect("/signup/")

class Login(utils.Handler):
    pass