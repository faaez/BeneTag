from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
import bene_query
import bene_util
import entities
import os



class Signup(webapp.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if not user: # need to sign in
            self.redirect(users.create_login_url(self.request.uri))
            return
        
        if not bene_query.getCurrentUser(): # no user exists
            producer = self.request.get('producer')
            consumer = self.request.get('consumer')
            if producer and not consumer: # make person a producer only in most restricted case
                u = entities.User(email=user.nickname(),
                                  owner=user,
                                  isConsumer=False,
                                  isProducer=True)
                u.put()
                self.redirect('/createproducer')
                return
            else: # all other cases, make consumer
                u = entities.User(email=user.nickname(),
                                  owner=user,
                                  isConsumer=True,
                                  isProducer=False)
                u.put()
                self.redirect('/createconsumer')
                return
                
            
        if bene_query.getCurrentUser().isProducer: # signed in producer
            if bene_query.getCurrentProducer() == None: # no producer page, so create one 
                self.redirect('/createproducer')
                return
            else: # already has producer page, so redirect
                self.redirect('/producerhome')
                return
        else: # signed in consumer
            if bene_query.getCurrentConsumer() == None: # no consumer page, so create on
                self.redirect('/createconsumer')
                return
            else: # already has consumer page, so redirect
                self.redirect('/consumerhome')
                return
            
    '''
    Exception handler
    '''
    def handle_exception(self, exception, debug_mode):
        if debug_mode:
            super(Signup, self).handle_exception(exception, debug_mode)
        else:
            template_values = bene_util.initTemplate(self.request.uri)
            path = os.path.join(os.path.dirname(__file__), 'not_found.html')
            self.response.out.write(template.render(path, template_values))
            return
