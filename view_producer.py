from google.appengine.api import users
from google.appengine.ext import db, webapp
from google.appengine.ext.webapp import template
import bene_util
import os



"""
View a Producer Page
"""
class ViewProducer(webapp.RequestHandler):
    def get(self):
        ID = self.request.get('id')
        if not ID:
            '''
            TODO: if no id is sent, defaults to a page with all producers? 
            '''
            self.redirect('/')
            return
        producer = db.get(ID)
        if not producer:
            '''
            TODO: if no id is sent, defaults to a page with all workers? 
            '''
            #workerlist = entities.Worker.all()
            template_values = {}
            path = os.path.join(os.path.dirname(__file__), 'not_found.html')
            self.response.out.write(template.render(path, template_values))
            return
        # Make a dictionary for template
        name = producer.name
        description = producer.description
        
        products = producer.products()
        workers = producer.workers()
        factories = producer.factories()
        
        template_values = {}
        template_values['id'] = ID
        template_values['name'] = name
        template_values['description'] = description
        template_values['factories'] = factories
        template_values['products'] = products 
        template_values['producer'] = producer
        template_values['workers'] = workers
        template_values['url'] = self.request.url  
        
        template_values['can_edit'] = False
        user = users.get_current_user()
        if user:
            if producer.owner == user:
                template_values['can_edit'] = True           
        
        if producer.logo:
            template_values['has_image'] = True
        else:
            template_values['has_image'] = False
    
        path = os.path.join(os.path.dirname(__file__), 'viewproducer.html')
        self.response.out.write(template.render(path, template_values))

class ProducerImage(webapp.RequestHandler):
    def get(self):
        # Get the id from the get parameter
        ID = self.request.get('id') 
        # Fetch the image for this worker
        producer = db.get(ID)
        self.response.headers['Content-Type'] = 'image'
        self.response.out.write(producer.logo) 
