from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
import bene_util
import entities
import os



"""
Creates a page with links to each service
"""
class AboutPage(webapp.RequestHandler):
    def get(self):
        template_values = bene_util.initTemplate(self.request.uri)
        path = os.path.join(os.path.dirname(__file__), 'about.html')
        self.response.out.write(template.render(path, template_values))

