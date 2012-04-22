from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
import bene_query
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
            signed_in_user = bene_query.getCurrentUser()
            if signed_in_user.isProducer:
                if not bene_query.getCurrentProducer(): # if producer page doesn't exist, need to create one
                    self.redirect('/createproducer?%s' % urllib.urlencode({'redirect': 'producerhome', 'msg': True}))
                else: # if setup done, then go to home page
                    self.redirect('/producerhome')
                    return
            else:
                if not bene_query.getCurrentConsumer():
                    self.redirect('/createconsumer?%s' % urllib.urlencode({'redirect': 'consumerhome', 'msg': True}))
                    return
                else:
                    self.redirect('/consumerhome')
                    return
        else: # otherwise, show button for signing in and searching
            template_values = bene_util.initTemplate(self.request.uri)
            path = os.path.join(os.path.dirname(__file__), 'home.html')
            self.response.out.write(template.render(path, template_values))
            return
        
    '''
    Exception handler
    '''
    def handle_exception(self, exception, debug_mode):
        if debug_mode:
            super(HomePage, self).handle_exception(exception, debug_mode)
        else:
            template_values = bene_util.initTemplate(self.request.uri)
            path = os.path.join(os.path.dirname(__file__), 'not_found.html')
            self.response.out.write(template.render(path, template_values))
            return
            

