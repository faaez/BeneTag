import os

from google.appengine.api import users
from google.appengine.ext import db
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template

import entities

"""
Creates a form for Producers to enter information 
about a Product
"""
class CreateProductPage(webapp.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if user:
            factory_names = []
            factories = entities.Factory.all()
            for factory in factories:
                factory_names.append(factory.name)
            template_values = {
                'producerName' : user.nickname(),
                'badges' : entities.Badge.all(),
                'factory_names' : factory_names
            }
            path = os.path.join(os.path.dirname(__file__), 'createproduct.html')
            self.response.out.write(template.render(path, template_values))
        else:
            greeting = ("<a href=\"%s\">Sign in or register</a>." % users.create_login_url("/createproduct"))
            self.response.out.write("<html><body>%s</body></html>" % greeting)

"""
Page that stores Product in datastore
"""
class StoreProductPage(webapp.RequestHandler):
    def post(self):
        user = users.get_current_user()
        if user:
            _name = self.request.get('name')
            _producerName = self.request.get('producerName')
            _factoryName = self.request.get('factoryName')
            _badges = self.request.get_all('badges')
            _picture = self.request.get('picture')
            if isinstance(_picture, unicode):
                _picture = _picture.encode('utf-8', 'replace')
            _factoryMade = entities.Factory.gql("WHERE name = :1", _factoryName).get()

            p = entities.Product(name=_name, producerName=_producerName, factoryMade=_factoryMade.key())
            for _badge in _badges:
                p.badges.append(db.Key(_badge))
            p.picture = db.Blob(_picture)
            p.put()
            self.redirect('/view?id=' + str(p.key()))
        else:
            greeting = ("<a href=\"%s\">Sign in or register</a>." %
                        users.create_login_url("/storeproduct"))
            self.response.out.write("<html><body>%s</body></html>" % greeting)
