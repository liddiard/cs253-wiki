import utils

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

class Login(utils.Handler):
    pass