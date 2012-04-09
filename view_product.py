import os

from google.appengine.ext import db
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template

from entities import Product

"""
View a Product's Page
"""
class ViewProduct(webapp.RequestHandler):
    def get(self):
        # Get the id from the get parameter
        id = self.request.get('id')
        # Fetch the data for this product
        product = db.get(id)
        # Display error if product ID not found
        if not product:
          template_values = {}
          path = os.path.join(os.path.dirname(__file__), 'not_found.html')
          self.response.out.write(template.render(path, template_values))
          return
        
        if product.factoryMade and product.factoryMade.location:
            latitude = product.factoryMade.location.lat
            longitude = product.factoryMade.location.lon
        else:
            latitude = None
            longitude = None
        # Make a dictionary for template
        template_values = {}
        template_values['id'] = id
        template_values['name'] = product.name
        template_values['producer'] = product.producerName
        template_values['latitude'] = latitude
        template_values['longitude'] = longitude
        template_values['url'] = self.request.url
        template_values['qr_url'] = self.request.url.replace('view','qr')
        template_values['factory_id'] = product.factoryMade.key()
        if product.picture:
            template_values['has_image'] = True
        else:
            template_values['has_image'] = False
        path = os.path.join(os.path.dirname(__file__), 'viewproduct.html')
        self.response.out.write(template.render(path, template_values))

class ProductImage(webapp.RequestHandler):
    def get(self):
        # Get the id from the get parameter
        id = self.request.get('id')
        # Fetch the image for this product
        product = db.get(id)
        self.response.headers['Content-Type'] = 'image'
        self.response.out.write(product.picture)