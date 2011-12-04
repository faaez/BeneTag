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
			template_values = {}
			path = os.path.join(os.path.dirname(__file__), 'createproduct.html')
			self.response.out.write(template.render(path, template_values))
		else:
			greeting = ("<a href=\"%s\">Sign in or register</a>." %
                        users.create_login_url("/createproduct"))
			self.response.out.write("<html><body>%s</body></html>" % greeting)

"""
Page that stores Product in datastore
"""
class StoreProductPage(webapp.RequestHandler):
    def post(self):
		user = users.get_current_user()
		if user:
			_id = self.request.get('id')
			_name = self.request.get('name')
			_producerName = self.request.get('producerName')
			_locationMade = self.request.get('locationMade')
        
			fields = _locationMade.split(',')
			if len(fields) == 2:
				try:
					lat = float(fields[0])
					lon = float(fields[1])
					gp = db.GeoPt(lat, lon)
				except ValueError:
					gp = None
			else:
				gp = None


			key = db.Key.from_path('Product', _id)
			p = entities.Product(parent=key, 
				id=_id, name=_name, producerName=_producerName, locationMade=gp)
			p.put()
			self.redirect('/view?id=' + str(_id))
		else:
			greeting = ("<a href=\"%s\">Sign in or register</a>." %
                        users.create_login_url("/storeproduct"))
			self.response.out.write("<html><body>%s</body></html>" % greeting)