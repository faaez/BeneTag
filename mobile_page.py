import os

from google.appengine.ext import db
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template

"""
    View mobile page for the product
"""

class ViewProduct(webapp.RequestHandler):
    def get(self):
        # Get the id from the get parameter
        ID = self.request.get('id')
        # Fetch the data for this product
        product = db.get(ID)
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
        if product.picture:
            template_values['has_image'] = True
        else:
            template_values['has_image'] = False
        path = os.path.join(os.path.dirname(__file__), 'mobilepage.html')
        self.response.out.write(template.render(path, template_values))

class ProductImage(webapp.RequestHandler):
    def get(self):
        # Get the id from the get parameter
        ID = self.request.get('id')
        # Fetch the image for this product
        product = db.get(ID)
        self.response.headers['Content-Type'] = 'image'
        self.response.out.write(product.picture)

class BadgeImage(webapp.RequestHandler):
    def get(self):
        badge = db.get(self.request.get('key'))
        self.response.headers['Content-Type'] = 'image'
        self.response.out.write(badge.icon)
