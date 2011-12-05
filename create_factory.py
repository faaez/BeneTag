import os

from google.appengine.api import users
from google.appengine.ext import db
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template

import entities

"""
Creates a form for Producers to enter information
about a Factoru
"""
class CreateFactoryPage(webapp.RequestHandler):
    def get(self):
        user = users.get_current_user() 
        template_values = {}
        template_values['added'] = (self.request.get('added') == 'True')
        path = os.path.join(os.path.dirname(__file__), 'createfactory.html')
        self.response.out.write(template.render(path, template_values))

"""
Page that stores Factory in datastore
"""
class StoreFactoryPage(webapp.RequestHandler):
    def post(self):
        user = users.get_current_user()
        
        _name = self.request.get('name')
        _address = self.request.get('address')
        _location = self.request.get('location')
        
        fields = _location.split(',')
        if len(fields) == 2:
            try:
                lat = float(fields[0])
                lon = float(fields[1])
                gp = db.GeoPt(lat, lon)
            except ValueError:
                gp = None
        else:
            gp = None

        f = entities.Factory(name=_name, address=_address, location=gp)

        f.put()
        self.redirect('/')
