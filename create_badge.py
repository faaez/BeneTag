import os

from google.appengine.api import users
from google.appengine.ext import db
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template

import entities

"""
Creates a form for Producers to enter information 
about a Badge
"""
class CreateBadgePage(webapp.RequestHandler):
    def get(self):
        user = users.get_current_user()
        template_values = {
            'producerName' : user.nickname()
        }
        path = os.path.join(os.path.dirname(__file__), 'createbadge.html')
        self.response.out.write(template.render(path, template_values))

"""
Page that stores Product in datastore
"""
class StoreBadgePage(webapp.RequestHandler):
    def post(self):
        if users.is_current_user_admin():
            _name = self.request.get('name')
            _description = self.request.get('description')
            _icon = self.request.get('icon')
            if isinstance(_icon,unicode):
                _icon = _icon.encode('utf-8', 'replace')

            b = entities.Badge(name=_name, icon=_icon, description=_description)
            
            b.put()
            self.redirect("/createbadge")
        else:
            greeting = "You need admin privileges to create a badge"
            self.response.out.write("<html><body>%s</body></html>" % greeting)
