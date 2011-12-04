import os

from google.appengine.ext import webapp
from google.appengine.ext.webapp import template

import entities

"""
Creates a page with links to each service
"""
class AboutPage(webapp.RequestHandler):
    def get(self):
        template_values = {}
        path = os.path.join(os.path.dirname(__file__), 'about.html')
        self.response.out.write(template.render(path, template_values))

