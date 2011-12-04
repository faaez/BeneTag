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
        products = Product.gql("WHERE id = :1", id)
        # Display error if product ID not found
        if products.count() < 1:
          template_values = {}
          path = os.path.join(os.path.dirname(__file__), 'not_found.html')
          self.response.out.write(template.render(path, template_values))
          return
        # Make a dictionary for template
        product = products[0]
        name = product.name
        producer = product.producerName
        latitude = product.locationMade.lat
        longitude = product.locationMade.lon
        template_values = {}
        template_values['id'] = id
        template_values['name'] = name
        template_values['producer'] = producer
        template_values['latitude'] = latitude
        template_values['longitude'] = longitude
        path = os.path.join(os.path.dirname(__file__), 'viewproduct.html')
        self.response.out.write(template.render(path, template_values))
