from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
import bene_query
import bene_util
import os
import urllib


"""
Consumer home page
"""
class ConsumerHomePage(webapp.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if not user: # if not signed in
            self.redirect('/?signin=True')
            return
        if bene_query.getCurrentUser().isProducer: # producer can't get to consumer home page
            self.redirect('/')
            return
        
        _consumer = bene_query.getCurrentConsumer()
        if _consumer == None: # if consumer page doesn't exist, need to create one
            self.redirect('/createconsumer?%s' % urllib.urlencode({'redirect': 'consumerhome', 'msg': True}))
            return
        
        # if setup done, then show home page
        template_values = bene_util.initTemplate(self.request.uri)
        path = os.path.join(os.path.dirname(__file__), 'consumerhome.html')
        self.response.out.write(template.render(path, template_values))
        return
    
    '''
    Exception handler
    '''
    def handle_exception(self, exception, debug_mode):
        if debug_mode:
            super(ConsumerHomePage, self).handle_exception(exception, debug_mode)
        else:
            template_values = bene_util.initTemplate(self.request.uri)
            path = os.path.join(os.path.dirname(__file__), 'not_found.html')
            self.response.out.write(template.render(path, template_values))
            return
            
            