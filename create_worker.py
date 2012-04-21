from google.appengine.api import users
from google.appengine.ext import db, webapp
from google.appengine.ext.webapp import template
import bene_query
import bene_util
import entities
import os
import urllib



"""
Creates a form to create a Worker
"""
class CreateWorkerPage(webapp.RequestHandler):
    def get(self):
        user = users.get_current_user() 
        if not user: # need to sign in
            self.redirect('/?signin=True')
            return
        
        if bene_query.getCurrentUser().isConsumer: # consumers can't access this
            self.redirect('/')
            return
            
        _producer = bene_query.getCurrentProducer()
        if _producer  == None: # no producer signed up, so ask to sign up
            self.redirect('/')
            return
        
        if not _producer.verified: # if producer is not verified
            self.redirect('/producerhome?%s' % urllib.urlencode({'verify': True}))
            return
        
        template_values = bene_util.urldecode(self.request.uri)
        template_values['factories'] = _producer.getFactories()
                
        path = os.path.join(os.path.dirname(__file__), 'createworker.html')
        self.response.out.write(template.render(path, template_values))
        return
    
    '''
    Exception handler
    '''
    def handle_exception(self, exception, debug_mode):
        if debug_mode:
            super(CreateWorkerPage, self).handle_exception(exception, debug_mode)
        else:
            template_values = {}
            path = os.path.join(os.path.dirname(__file__), 'not_found.html')
            self.response.out.write(template.render(path, template_values))
            return
        
        
"""
Puts a worker in the database
"""
class StoreWorkerPage(webapp.RequestHandler):
    def post(self):
        user = users.get_current_user() 
        if not user: # need to sign in
            self.redirect('/?signin=True')
            return
        
        if bene_query.getCurrentUser().isConsumer: # consumers can't access this
            self.redirect('/')
            return
            
        _producer = bene_query.getCurrentProducer()
        if _producer  == None: # no producer signed up, so ask to sign up
            self.redirect('/')
            return
        
        if not _producer.verified: # if producer is not verified
            self.redirect('/producerhome?%s' % urllib.urlencode({'verify': True}))
            return
        
        _name = self.request.get('name')
        _factory = self.request.get('factory')
        _picture = self.request.get('picture')
        _profile = self.request.get('profile')
        _unique = self.request.get('unique')
                            
        w = entities.Worker(name=_name,  
                            profile=_profile,
                            unique=_unique,
                            owner=user)
        w.addProducer(_producer)
        if _factory:
            w.addFactory(db.get(_factory))
        w.addPicture(_picture)
        
        
        if bene_util.doesWorkerExist(w): # already exists
            self.redirect('/createworker?%s' % urllib.urlencode({'repeat': True}))
            return
        
        w.put()
        if self.request.get('more'): # want to add more
            self.redirect('/createworker?%s' % urllib.urlencode({'added': True}))
            return
        
        # otherwise redirect to worker page
        self.redirect('/viewworker?%s' % urllib.urlencode({'id' : w.key()}))
            
    '''
    Exception handler
    '''
    def handle_exception(self, exception, debug_mode):
        if debug_mode:
            super(StoreWorkerPage, self).handle_exception(exception, debug_mode)
        else:
            template_values = {}
            path = os.path.join(os.path.dirname(__file__), 'not_found.html')
            self.response.out.write(template.render(path, template_values))
            return
            