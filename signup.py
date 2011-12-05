import os

from google.appengine.api import users
from google.appengine.ext import db
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template

import entities

"""
Creates a form to sign up as a Producer
"""
class CreateProducerPage(webapp.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if user:
            template_values = {
                'producerEmail' : user.nickname()
            }
            path = os.path.join(os.path.dirname(__file__), 'signup.html')
            self.response.out.write(template.render(path, template_values))
        else:
            greeting = ("<a href=\"%s\">Sign up with your Google accountr</a>." % users.create_login_url("/signup"))
            self.response.out.write("<html><body>%s</body></html>" % greeting)

"""
Puts a producer in the database
"""
class StoreProducerPage(webapp.RequestHandler):
    def post(self):
        user = users.get_current_user()
        if user:
            _name = self.request.get('name')
            _email = self.request.get('email')
            _logo = self.request.get('logo')
            _description = self.request.get('description')
            if isinstance(_logo, unicode):
                _logo = _logo.encode('utf-8', 'replace')
                
            p = entities.Producer(name = _name,profileOwner=user,email=_email,companyLogo=db.Blob(_logo),description=_description)
            p.put()

            self.redirect('/')
        else:
            greeting = ("<a href=\"%s\">Sign up with your Google account</a>." %
                        users.create_login_url("/storeproducer"))
            self.response.out.write("<html><body>%s</body></html>" % greeting)
