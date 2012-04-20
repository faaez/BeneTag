from google.appengine.api import users
from google.appengine.ext import db, webapp
from google.appengine.ext.webapp import template
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
        if not product:
            '''
            TODO: if no id is sent, defaults to page with all factories?
            '''
            #factorylist = entities.Factory.all()
            template_values = {}
            path = os.path.join(os.path.dirname(__file__), 'not_found.html')
            self.response.out.write(template.render(path, template_values))
            return
        # Display error if product ID not found
        if not product:
            template_values = {}
            path = os.path.join(os.path.dirname(__file__), 'not_found.html')
            self.response.out.write(template.render(path, template_values))
            return
        # Make a dictionary for template
        if product.factory and product.factory.location:
            latitude = product.factory.location.lat
            longitude = product.factory.location.lon
        else:
            latitude = None
            longitude = None
        template_values = {}
        template_values['id'] = ID
        template_values['name'] = product.name
        template_values['producer'] = product.producer
        template_values['latitude'] = latitude
        template_values['longitude'] = longitude
        template_values['url'] = self.request.url
        template_values['qr_url'] = self.request.url.replace('view','qr')
        template_values['factory'] = product.factory
        template_values['badges'] = product.badges
        template_values['rating'] = product.rating
        template_values['workers'] = product.workers()
        if product.badges:
            template_values['badges'] = product.badges
            template_values['has_badges'] = True
        if product.picture:
            template_values['has_image'] = True
        else:
            template_values['has_image'] = False
            
        template_values['can_edit'] = False
        user = users.get_current_user()
        if user:
            if product.owner == user:
                template_values['can_edit'] = True
            
        path = os.path.join(os.path.dirname(__file__), 'mobilepage.html')
        self.response.out.write(template.render(path, template_values))

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
        self.response.out.write(product.picture)

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
        self.response.out.write(badge.icon)
