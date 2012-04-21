from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
import bene_query
import bene_util
import os
import urllib



"""
Creates a form to edit Consumer
"""
class EditConsumerPage(webapp.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if not user: # need to sign in
            self.redirect('/?signin=True')
            return
        
        if bene_query.getCurrentUser().isProducer: # producers aren't allowed here
            self.redirect('/')
            return
            
        _consumer = bene_query.getCurrentConsumer();
        if _consumer == None: # no consumer page, so create one 
            self.redirect('/')
            return
        
        template_values = bene_util.urldecode(self.request.uri)
        template_values['name_old'] = _consumer.name
        template_values['profile_old'] = _consumer.profile
        
        path = os.path.join(os.path.dirname(__file__), 'editconsumer.html')
        self.response.out.write(template.render(path, template_values))
        return
    
        '''
    Exception handler
    '''
    def handle_exception(self, exception, debug_mode):
        if debug_mode:
            super(EditConsumerPage, self).handle_exception(exception, debug_mode)
        else:
            template_values = {}
            path = os.path.join(os.path.dirname(__file__), 'not_found.html')
            self.response.out.write(template.render(path, template_values))
            return
            

"""
Puts a Producer in the database
"""
class StoreEditedConsumerPage(webapp.RequestHandler):
    def post(self):
        user = users.get_current_user()
        if not user: # need to sign in
            self.redirect('/?signin=True')
            return
        
        if bene_query.getCurrentUser().isProducer: # producers aren't allowed here
            self.redirect('/')
            return
            
        _consumer = bene_query.getCurrentConsumer();
        if _consumer == None: # no consumer page, so create one 
            self.redirect('/')
            return
        
        _name = self.request.get('name')
        _profile = self.request.get('profile')
        _picture = self.request.get('picture')
                              
        _consumer.name = _name
        _consumer.profile = _profile
        _consumer.addPicture(_picture)
        _consumer.put()
                        
        self.redirect('/viewconsumer?%s' % urllib.urlencode({'id': _consumer.key()}))
        return
    
        '''
    Exception handler
    '''
    def handle_exception(self, exception, debug_mode):
        if debug_mode:
            super(StoreEditedConsumerPage, self).handle_exception(exception, debug_mode)
        else:
            template_values = {}
            path = os.path.join(os.path.dirname(__file__), 'not_found.html')
            self.response.out.write(template.render(path, template_values))
            return