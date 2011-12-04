import os

from google.appengine.api import users
from google.appengine.ext import db
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template

import entities

"""
Creates a page with links to each service
"""
class HomePage(webapp.RequestHandler):
    def get(self):
        user = users.get_current_user() 
        if user:
            template_values = {}
            path = os.path.join(os.path.dirname(__file__), 'home.html')
            self.response.out.write(template.render(path, template_values))
        else:
            greeting = ("<a href=\"%s\">Sign in or register</a>." %
                        users.create_login_url("/"))
            self.response.out.write("<html><body>%s</body></html>" % greeting)

