from google.appengine.api import users
from google.appengine.ext import db, webapp
from google.appengine.ext.webapp import template
import bene_util
import os
import urllib


"""
View a Product's Page
"""
class ViewProduct(webapp.RequestHandler):
    def get(self):
        # Get the id from the get parameter
        ID = self.request.get('id')
        if not ID:
            ''' 
            TODO: If no ID sent, default to page with all products?
            '''
            self.redirect('/')
            return
        # Fetch the data for this product
        product = db.get(ID)
        # Display error if product ID not found
        if not product:
            template_values = {}
            path = os.path.join(os.path.dirname(__file__), 'not_found.html')
            self.response.out.write(template.render(path, template_values))
            return
        
        _factory = product.getFactory()
        if _factory and _factory.location:
            latitude = _factory.location.lat
            longitude = _factory.location.lon
        else:
            latitude = None
            longitude = None
        # Make a dictionary for template
        template_values = bene_util.urldecode(self.request.uri)
        template_values['id'] = ID
        template_values['name'] = product.name
        template_values['producer'] = product.getProducer()
        template_values['latitude'] = latitude
        template_values['longitude'] = longitude
        template_values['url'] = self.request.url
        template_values['qr_url'] = self.request.url.replace('view','qr')
        template_values['factory'] = _factory
        template_values['badges'] = product.getBadges()
        template_values['rating'] = product.rating
        template_values['workers'] = product.getWorkers()
        if product.picture:
            template_values['has_image'] = True
        else:
            template_values['has_image'] = False
            
        template_values['can_edit'] = False
        user = users.get_current_user()
        if user:
            if product.owner == user:
                template_values['can_edit'] = True
            
        path = os.path.join(os.path.dirname(__file__), 'viewproduct.html')
        self.response.out.write(template.render(path, template_values))
        return
    
    '''
    Exception handler
    '''
    def handle_exception(self, exception, debug_mode):
        if debug_mode:
            super(ViewProduct, self).handle_exception(exception, debug_mode)
        else:
            template_values = {}
            path = os.path.join(os.path.dirname(__file__), 'not_found.html')
            self.response.out.write(template.render(path, template_values))
            return
        

class ProductImage(webapp.RequestHandler):
    def get(self):
        # Get the id from the get parameter
        ID = self.request.get('id') 
        if not ID:
            '''
            TODO: what to do here?
            '''
            return
        # Fetch the image for this product
        product = db.get(ID)
        if not product:
            '''
            TODO: what to do here?
            '''
            return
        self.response.headers['Content-Type'] = 'image'
        self.response.out.write(product.getPicture())
        return
    
    '''
    Exception handler
    '''
    def handle_exception(self, exception, debug_mode):
        if debug_mode:
            super(ProductImage, self).handle_exception(exception, debug_mode)
        else:
            template_values = {}
            path = os.path.join(os.path.dirname(__file__), 'not_found.html')
            self.response.out.write(template.render(path, template_values))
            return
        