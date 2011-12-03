import os

from google.appengine.ext import webapp
from google.appengine.ext.webapp import template

import entities

"""
Creates a form for Producers to enter information 
about a Product
"""
class CreateProductPage(webapp.RequestHandler):
    def get(self):
        template_values = {}
        path = os.path.join(os.path.dirname(__file__), 'createProduct.html')
        self.response.out.write(template.render(path, template_values))

"""
Page that stores Product in datastore
"""
class StoreProductPage(webapp.RequestHandler):
    def post(self):
        _id = self.request.get('id')
        _name = self.request.get('name')
        key = db.Key.from_path('Product', 'product')
        p = entities.Product(parent=key, id=_id, name=_name)
        p.put()
        self.response.out.write('Created a product!')