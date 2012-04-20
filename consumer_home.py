from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
import bene_util
import os
import urllib



"""
Creates a page with links to each service
"""
class HomePage(webapp.RequestHandler):
    def get(self):
        user = users.get_current_user()
        
        if user:
            if bene_util.getCurrentUser().isProducer:
                self.redirect('/')
                return
            if bene_util.getCurrentConsumer() == None: # if producer page doesn't exist, need to create one
                self.redirect('/createconsumer?%s' % urllib.urlencode({'redirect': 'consumerhome', 'msg': True}))
                return
            else: # if setup done, then show home page
                template_values = bene_util.decodeURL(self.request.uri)
                path = os.path.join(os.path.dirname(__file__), 'consumerhome.html')
                self.response.out.write(template.render(path, template_values))
                return
        else:
            self.redirect(users.create_login_url(self.request.uri))
            return