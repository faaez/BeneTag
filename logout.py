from google.appengine.api import users
from google.appengine.ext import webapp



class Logout(webapp.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if user: # if signed in
            self.redirect(users.create_logout_url(self.request.uri))
            return
        else:
            self.redirect('/')
            return