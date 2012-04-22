from google.appengine.api import users
from google.appengine.ext import db, webapp
from google.appengine.ext.webapp import template
import bene_query
import bene_util
import os


"""
    View mobile page for the product
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
            template_values = bene_util.initTemplate(self.request.uri)
            path = os.path.join(os.path.dirname(__file__), 'not_found.html')
            self.response.out.write(template.render(path, template_values))
            return
        # Make a dictionary for template
        _factory = product.getFactory()
        if _factory and _factory.location:
            latitude = _factory.location.lat
            longitude = _factory.location.lon
        else:
            latitude = None
            longitude = None
        template_values = bene_util.initTemplate(self.request.uri)
        template_values['id'] = ID
        template_values['name'] = product.name
        template_values['producer'] = product.getProducer()
        template_values['latitude'] = latitude
        template_values['longitude'] = longitude
        template_values['url'] = self.request.url
        template_values['qr_url'] = self.request.url.replace('view','qr')
        template_values['factory'] = product.getFactory()
        template_values['rating'] = product.rating
        template_values['workers'] = product.getWorkers()
        _badges = product.getBadges()
        if _badges:
            template_values['badges'] = _badges
            template_values['has_badges'] = True
        else:
            template_values['has_badges'] = False
        if product.getPicture():
            template_values['has_image'] = True
        else:
            template_values['has_image'] = False
            
        template_values['can_edit'] = False
        user = users.get_current_user()
        if user:
            if product.owner == user:
                template_values['can_edit'] = True
                
        template_values['in_closet'] = False
        template_values['add_closet'] = False
        if user:
            if bene_query.getCurrentUser().isConsumer:
                consumer = bene_query.getCurrentConsumer()
                if consumer:
                    if consumer.hasProduct(product.key()):
                        template_values['in_closet'] = True
                    else:
                        template_values['add_closet'] = True
            
        path = os.path.join(os.path.dirname(__file__), 'mobilepage.html')
        self.response.out.write(template.render(path, template_values))
        return
    '''
    Exception handler
    '''
    def handle_exception(self, exception, debug_mode):
        if debug_mode:
            super(ViewProduct, self).handle_exception(exception, debug_mode)
        else:
            template_values = bene_util.initTemplate(self.request.uri)
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
            template_values = bene_util.initTemplate(self.request.uri)
            path = os.path.join(os.path.dirname(__file__), 'not_found.html')
            self.response.out.write(template.render(path, template_values))
            return

class BadgeImage(webapp.RequestHandler):
    def get(self):
        key = self.request.get('key')
        if not key:
            '''
            TODO: what to do here?
            '''
            return
        badge = db.get(key)
        if not badge:
            '''
            TODO: what to do here?
            '''
            return
        self.response.headers['Content-Type'] = 'image'
        self.response.out.write(badge.getPicture())
        return
    
    '''
    Exception handler
    '''
    def handle_exception(self, exception, debug_mode):
        if debug_mode:
            super(BadgeImage, self).handle_exception(exception, debug_mode)
        else:
            template_values = bene_util.initTemplate(self.request.uri)
            path = os.path.join(os.path.dirname(__file__), 'not_found.html')
            self.response.out.write(template.render(path, template_values))
            return