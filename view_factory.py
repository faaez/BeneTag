from google.appengine.api import users
from google.appengine.ext import db, webapp
from google.appengine.ext.webapp import template
import bene_util
import os




"""
View a Factory Page
"""
class ViewFactory(webapp.RequestHandler):
    def get(self):
        ID = self.request.get('id')
        if not ID:
            '''
            TODO: If no ID sent, default to page with all factories?
            '''
            self.redirect('/')
            return
        factory = db.get(ID)
        ''' an error in getting the factory will be redirected to exception handler'''
        
        # Make a dictionary for template
        name = factory.name
        producer = factory.getProducer()
        productlist = factory.getProducts()
        workers = factory.getWorkers()
        address = factory.address
        if factory.location:
            latitude = factory.location.lat
            longitude = factory.location.lon
        else:
            latitude = None
            longitude = None
        template_values = bene_util.initTemplate(self.request.uri)
        template_values['id'] = ID
        template_values['name'] = name
        template_values['producer'] = producer
        template_values['products'] = productlist
        template_values['workers'] = workers
        template_values['latitude'] = latitude
        template_values['longitude'] = longitude
        template_values['url'] = self.request.url
        template_values['address'] = address
        template_values['qr_url'] = self.request.url.replace('view','qr')
        
        template_values['can_edit'] = False
        user = users.get_current_user()
        if user:
            if factory.owner == user:
                template_values['can_edit'] = True
        
        path = os.path.join(os.path.dirname(__file__), 'viewfactory.html')
        self.response.out.write(template.render(path, template_values))
        return
    
    '''
    Exception handler
    '''
    def handle_exception(self, exception, debug_mode):
        if debug_mode:
            super(ViewFactory, self).handle_exception(exception, debug_mode)
        else:
            template_values = bene_util.initTemplate(self.request.uri)
            path = os.path.join(os.path.dirname(__file__), 'not_found.html')
            self.response.out.write(template.render(path, template_values))
            return
