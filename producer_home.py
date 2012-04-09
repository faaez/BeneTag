from google.appengine.api import users
from google.appengine.ext import db, webapp
from google.appengine.ext.webapp import template
import bene_util
import entities
import os
import urllib



"""
Creates a page with links to each service
"""
class HomePage(webapp.RequestHandler):
    def get(self):
        user = users.get_current_user()
        
        if user:
            if bene_util.getCurrentProducer() == None: # if producer page doesn't exist, need to create one
                self.redirect('/signup?%s' % urllib.urlencode({'redirect': 'producerhome', 'msg': True}))
            else: # if setup done, then show home page
                template_values = {}
                path = os.path.join(os.path.dirname(__file__), 'producerhome.html')
                self.response.out.write(template.render(path, template_values))
        else:
            self.redirect(users.create_login_url(self.request.uri))
