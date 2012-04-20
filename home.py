from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
import bene_util
import os
import urllib



"""
Home page to sign in
"""
class HomePage(webapp.RequestHandler):
    def get(self):
        user = users.get_current_user()
        
        if user: # if user signed in
            signed_in_user = bene_util.getCurrentUser()
            if signed_in_user.isProducer:
                if not bene_util.getCurrentProducer(): # if producer page doesn't exist, need to create one
                    self.redirect('/createproducer?%s' % urllib.urlencode({'redirect': 'producerhome', 'msg': True}))
                else: # if setup done, then go to home page
                    self.redirect('/producerhome')
            else:
                if not bene_util.getCurrentConsumer():
                    self.redirect('/createconsumer?%s' % urllib.urlencode({'redirect': 'consumerhome', 'msg': True}))
                else:
                    self.redirect('/consumerhome')
        else: # otherwise, show button for signing in and searching
            template_values = {}
            path = os.path.join(os.path.dirname(__file__), 'home.html')
            self.response.out.write(template.render(path, template_values))

