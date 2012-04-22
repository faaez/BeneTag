from google.appengine.api import users
from google.appengine.ext import db, webapp
from google.appengine.ext.webapp import template
import bene_query
import bene_util
import os


"""
View a Consumer Page
"""
class ViewConsumer(webapp.RequestHandler):
    def get(self):
        ID = self.request.get('id')
        if not ID:
            '''
            TODO: if no id is sent, defaults to a page with all producers? 
            '''
            self.redirect('/')
            return
        consumer = db.get(ID)
        if not consumer:
            template_values = bene_util.initTemplate(self.request.uri)
            path = os.path.join(os.path.dirname(__file__), 'not_found.html')
            self.response.out.write(template.render(path, template_values))
            return
        # Make a dictionary for template
        name = consumer.name
        profile = consumer.profile
        
        template_values = bene_util.initTemplate(self.request.uri)
        template_values['id'] = ID
        template_values['consumer'] = consumer
        template_values['name'] = name
        template_values['profile'] = profile
        
        template_values['can_edit'] = False
        user = users.get_current_user()
        if user:
            if consumer.owner == user:
                template_values['can_edit'] = True           
        
        path = os.path.join(os.path.dirname(__file__), 'viewconsumer.html')
        self.response.out.write(template.render(path, template_values))
        return
    
"""
View my Consumer Page
"""
class ViewMyConsumer(webapp.RequestHandler):
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
        name = _consumer.name
        profile = _consumer.profile
        
        template_values = bene_util.initTemplate(self.request.uri)
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
            super(ViewMyConsumer, self).handle_exception(exception, debug_mode)
        else:
            template_values = bene_util.initTemplate(self.request.uri)
            path = os.path.join(os.path.dirname(__file__), 'not_found.html')
            self.response.out.write(template.render(path, template_values))
            return
        
class ConsumerImage(webapp.RequestHandler):
    def get(self):
        # Get the id from the get parameter
        ID = self.request.get('id') 
        if not ID:
            '''
            TODO: what to do here?
            '''
            return
        # Fetch the image for this worker
        consumer = db.get(ID)
        if not consumer:
            '''
            TODO: what to do here?
            '''
            return
        self.response.headers['Content-Type'] = 'image'
        self.response.out.write(consumer.getPicture()) 
        return
    
    '''
    Exception handler
    '''
    def handle_exception(self, exception, debug_mode):
        if debug_mode:
            super(ConsumerImage, self).handle_exception(exception, debug_mode)
        else:
            template_values = bene_util.initTemplate(self.request.uri)
            path = os.path.join(os.path.dirname(__file__), 'not_found.html')
            self.response.out.write(template.render(path, template_values))
            return
