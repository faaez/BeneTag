from google.appengine.api import users
from google.appengine.ext import db, webapp
from google.appengine.ext.webapp import template
import bene_query
import bene_util
import os



"""
View a Producer Page
"""
class ViewProducer(webapp.RequestHandler):
    def get(self):
        ID = self.request.get('id')
        if not ID:
            '''
            TODO: if no id is sent, defaults to a page with all producers? 
            '''
            self.redirect('/')
            return
        producer = db.get(ID)
        if not producer:
            template_values = bene_util.initTemplate(self.request.uri)
            path = os.path.join(os.path.dirname(__file__), 'not_found.html')
            self.response.out.write(template.render(path, template_values))
            return
        # Make a dictionary for template
        name = producer.name
        description = producer.description
        
        products = producer.getProducts()
        workers = producer.getWorkers()
        factories = producer.getFactories()
        
        template_values = bene_util.initTemplate(self.request.uri)
        template_values['id'] = ID
        template_values['name'] = name
        template_values['description'] = description
        template_values['factories'] = factories
        template_values['products'] = products 
        template_values['producer'] = producer
        template_values['workers'] = workers
        template_values['url'] = self.request.url  
        
        template_values['can_edit'] = False
        user = users.get_current_user()
        if user:
            if producer.owner == user:
                template_values['can_edit'] = True           
        
        if producer.getPicture():
            template_values['has_image'] = True
        else:
            template_values['has_image'] = False
    
        path = os.path.join(os.path.dirname(__file__), 'viewproducer.html')
        self.response.out.write(template.render(path, template_values))
        return
    
    '''
    Exception handler
    '''
    def handle_exception(self, exception, debug_mode):
        if debug_mode:
            super(ViewProducer, self).handle_exception(exception, debug_mode)
        else:
            template_values = bene_util.initTemplate(self.request.uri)
            path = os.path.join(os.path.dirname(__file__), 'not_found.html')
            self.response.out.write(template.render(path, template_values))
            return
    
    
"""
View my Producer Page
"""
class ViewMyProducer(webapp.RequestHandler):
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
        
        # Make a dictionary for template
        name = _producer.name
        description = _producer.description
        
        products = _producer.getProducts()
        workers = _producer.getWorkers()
        factories = _producer.getFactories()
        
        template_values = bene_util.initTemplate(self.request.uri)
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
    Exception handler
    '''
    def handle_exception(self, exception, debug_mode):
        if debug_mode:
            super(ViewMyProducer, self).handle_exception(exception, debug_mode)
        else:
            template_values = bene_util.initTemplate(self.request.uri)
            path = os.path.join(os.path.dirname(__file__), 'not_found.html')
            self.response.out.write(template.render(path, template_values))
            return

class ProducerImage(webapp.RequestHandler):
    def get(self):
        # Get the id from the get parameter
        ID = self.request.get('id') 
        if not ID:
            '''
            TODO: what to do here?
            '''
            return
        # Fetch the image for this worker
        producer = db.get(ID)
        if not producer:
            '''
            TODO: what to do here?
            '''
            return
        self.response.headers['Content-Type'] = 'image'
        self.response.out.write(producer.getPicture()) 
        return
    '''
    Exception handler
    '''
    def handle_exception(self, exception, debug_mode):
        if debug_mode:
            super(ProducerImage, self).handle_exception(exception, debug_mode)
        else:
            template_values = bene_util.initTemplate(self.request.uri)
            path = os.path.join(os.path.dirname(__file__), 'not_found.html')
            self.response.out.write(template.render(path, template_values))
            return
