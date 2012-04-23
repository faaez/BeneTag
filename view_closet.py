from google.appengine.api import users
from google.appengine.ext import db, webapp
from google.appengine.ext.webapp import template
import bene_query
import bene_util
import os


"""
View all Products in a consumer's closet
"""
class ViewCloset(webapp.RequestHandler):
    def get(self):
        # Get the id from the get parameter
        ID = self.request.get('id')
        if not ID:
            ''' 
            TODO: If no ID sent, default to?
            '''
            self.redirect('/')
            return
        # Fetch the data for this consumer
        consumer = db.get(ID)
        ''' an error in getting the consumer will be redirected to exception handler'''
        
        # Make a dictionary for template
        template_values = bene_util.initTemplate(self.request.uri)
        template_values['id'] = ID
        template_values['consumer'] = consumer
        template_values['products'] = consumer.getProducts()
        
        template_values['can_edit'] = False
        user = users.get_current_user()
        if user:
            if consumer.owner == user:
                template_values['can_edit'] = True
            
        path = os.path.join(os.path.dirname(__file__), 'viewcloset.html')
        self.response.out.write(template.render(path, template_values))
        return
    
    '''
    Exception handler
    '''
    def handle_exception(self, exception, debug_mode):
        if debug_mode:
            super(ViewCloset, self).handle_exception(exception, debug_mode)
        else:
            template_values = bene_util.initTemplate(self.request.uri)
            path = os.path.join(os.path.dirname(__file__), 'not_found.html')
            self.response.out.write(template.render(path, template_values))
            return
     
'''
View my closet
'''   
class ViewMyCloset(webapp.RequestHandler):
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
        
        # Make a dictionary for template
        template_values = bene_util.initTemplate(self.request.uri)
        template_values['id'] = _consumer.key()
        template_values['consumer'] = _consumer
        template_values['products'] = _consumer.getProducts()
        
        template_values['can_edit'] = False
        user = users.get_current_user()
        if user:
            if _consumer.owner == user:
                template_values['can_edit'] = True
            
        path = os.path.join(os.path.dirname(__file__), 'viewcloset.html')
        self.response.out.write(template.render(path, template_values))
        return
    
    '''
    Exception handler
    '''
    def handle_exception(self, exception, debug_mode):
        if debug_mode:
            super(ViewMyCloset, self).handle_exception(exception, debug_mode)
        else:
            template_values = bene_util.initTemplate(self.request.uri)
            path = os.path.join(os.path.dirname(__file__), 'not_found.html')
            self.response.out.write(template.render(path, template_values))
            return