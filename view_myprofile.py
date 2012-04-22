from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
import bene_query
import bene_util
import os

"""
View my Producer Page
"""
class ViewMyProfile(webapp.RequestHandler):
    def get(self):
        user = users.get_current_user() 
        if not user: # need to sign in
            self.redirect('/?signin=True')
            return
        
        '''
        PRODUCER PROFILE
        '''
        if bene_query.getCurrentUser().isProducer: 
            _producer = bene_query.getCurrentProducer()
            if _producer  == None: # no producer signed up, so ask to sign up
                self.redirect('/')
                return
            
            # Make a dictionary for template
            name = _producer.name
            description = _producer.description
            
            products = _producer.getProducts()
            workers = _producer.getWorkers()
            factories = _producer.getFactories()
            
            template_values = bene_util.urldecode(self.request.uri)
            template_values['id'] = _producer.key()
            template_values['name'] = name
            template_values['description'] = description
            template_values['factories'] = factories
            template_values['products'] = products 
            template_values['producer'] = _producer
            template_values['workers'] = workers
            template_values['url'] = self.request.url  
            
            template_values['can_edit'] = False
            user = users.get_current_user()
            if user:
                if _producer.owner == user:
                    template_values['can_edit'] = True           
            
            if _producer.getPicture():
                template_values['has_image'] = True
            else:
                template_values['has_image'] = False
        
            path = os.path.join(os.path.dirname(__file__), 'viewproducer.html')
            self.response.out.write(template.render(path, template_values))
            return
        
        '''
        CONSUMER PROFILE
        '''            
        _consumer = bene_query.getCurrentConsumer();
        if _consumer == None: # no consumer page, so create one 
            self.redirect('/')
            return
        
        # Make a dictionary for template
        name = _consumer.name
        profile = _consumer.profile
        
        template_values = bene_util.urldecode(self.request.uri)
        template_values['id'] = _consumer.key()
        template_values['consumer'] = _consumer
        template_values['name'] = name
        template_values['profile'] = profile
        
        template_values['can_edit'] = False
        user = users.get_current_user()
        if user:
            if _consumer.owner == user:
                template_values['can_edit'] = True           
        
        path = os.path.join(os.path.dirname(__file__), 'viewconsumer.html')
        self.response.out.write(template.render(path, template_values))
        return
    
    '''
    Exception handler
    '''
    def handle_exception(self, exception, debug_mode):
        if debug_mode:
            super(ViewMyProfile, self).handle_exception(exception, debug_mode)
        else:
            template_values = {}
            path = os.path.join(os.path.dirname(__file__), 'not_found.html')
            self.response.out.write(template.render(path, template_values))
            return