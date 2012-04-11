from google.appengine.ext import db, webapp
from google.appengine.ext.webapp import template

import os



"""
View a Factory Page
"""
class ViewFactory(webapp.RequestHandler):
    def get(self):
        ID = self.request.get('id')
        factory = db.get(ID)
        if not factory:
            '''
            TODO: if no id is sent, defaults to page with all factories?
            '''
            #factorylist = entities.Factory.all()
            template_values = {}
            path = os.path.join(os.path.dirname(__file__), 'not_found.html')
            self.response.out.write(template.render(path, template_values))
            return
        # Make a dictionary for template
        name = factory.name
        producer = factory.producer
        productlist = factory.products()
        workers = factory.workers()
        address = factory.address
        if factory.location:
            latitude = factory.location.lat
            longitude = factory.location.lon
        else:
            latitude = None
            longitude = None
        template_values = {}
        template_values['id'] = ID
        template_values['name'] = name
        template_values['producer'] = producer
        template_values['products'] = productlist
        template_values['workers'] = workers
        template_values['latitude'] = latitude
        template_values['longitude'] = longitude
        template_values['url'] = self.request.url
        template_values['address'] = address
        template_values['qr_url'] = self.request.url.replace('view','qr')
        path = os.path.join(os.path.dirname(__file__), 'viewfactory.html')
        self.response.out.write(template.render(path, template_values))
