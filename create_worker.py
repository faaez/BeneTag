import os

from google.appengine.api import users
from google.appengine.ext import db
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template

import entities

"""
Creates a form to create a Worker
"""
class CreateWorkerPage(webapp.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if user:
            factory_names = []
            factories = entities.Factory.all()
            for factory in factories:
                factory_names.append(factory.name)
            template_values = {
                'producerName' : user.nickname(),
                'factory_names' : factory_names
            }
            path = os.path.join(os.path.dirname(__file__), 'createworker.html')
            self.response.out.write(template.render(path, template_values))
        else:
            greeting = ("<a href=\"%s\">Sign in or register</a>." % users.create_login_url("/createworker"))
            self.response.out.write("<html><body>%s</body></html>" % greeting)

"""
Puts a worker in the database
"""
class StoreWorkerPage(webapp.RequestHandler):
    def post(self):
        user = users.get_current_user()
        if user:
            _name = self.request.get('name')
            _factoryName = self.request.get('factoryName')
            _picture = self.request.get('picture')
            _profile = self.request.get('profile')
            if isinstance(_picture, unicode):
                _picture = _picture.encode('utf-8', 'replace')
            _factoryMade = entities.Factory.gql("WHERE name = :1", _factoryName).get()

            f = entities.Worker(name=_name, factory=_factoryMade.key(), profile=_profile)
            f.picture = db.Blob(_picture)
            f.put()
            self.redirect('/')
        else:
            greeting = ("<a href=\"%s\">Sign in or register</a>." %
                        users.create_login_url("/storeworker"))
            self.response.out.write("<html><body>%s</body></html>" % greeting)
