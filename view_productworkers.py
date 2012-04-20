from google.appengine.ext import db, webapp
from google.appengine.ext.webapp import template

import os



"""
View workers who worked on a product
"""
class ViewProductWorkers(webapp.RequestHandler):
    def get(self):
        ID = self.request.get('id')
        if not ID:
            ''' 
            TODO: If no ID sent, default to page with all products?
            '''
            self.redirect('/')
            return
        _product = db.get(ID)
        if not _product:
            '''
            TODO: if no id is sent, defaults to page with all factories?
            '''
            #factorylist = entities.Factory.all()
            template_values = {}
            path = os.path.join(os.path.dirname(__file__), 'not_found.html')
            self.response.out.write(template.render(path, template_values))
            return
        # Make a dictionary for template
        name = _product.name
        producer = _product.producer
        workers = _product.workers()
        factory = _product.factory
        template_values = {}
        template_values['id'] = ID
        template_values['product'] = _product
        template_values['name'] = name
        template_values['producer'] = producer
        template_values['workers'] = workers
        template_values['url'] = self.request.url
        template_values['qr_url'] = self.request.url.replace('view','qr')
        path = os.path.join(os.path.dirname(__file__), 'viewproductworkers.html')
        self.response.out.write(template.render(path, template_values))
