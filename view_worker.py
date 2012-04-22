from google.appengine.api import users
from google.appengine.ext import db, webapp
from google.appengine.ext.webapp import template
import bene_util
import os



"""
View a Worker Page
"""
class ViewWorker(webapp.RequestHandler):
    def get(self):
        ID = self.request.get('id')
        if not ID:
            '''
            TODO: if no id is sent, defaults to a page with all workers? 
            '''
            self.redirect('/')
        worker = db.get(ID)
        if not worker:
            template_values = bene_util.initTemplate(self.request.uri)
            path = os.path.join(os.path.dirname(__file__), 'not_found.html')
            self.response.out.write(template.render(path, template_values))
            return
        # Make a dictionary for template
        name = worker.name
        factory = worker.getFactory()
        profile = worker.profile
        picture = worker.getPicture()
        producer = worker.getProducer()
        products = worker.getProducts()
        if factory.location:
            latitude = factory.location.lat
            longitude = factory.location.lon
        else:
            latitude = None
            longitude = None
        template_values = bene_util.initTemplate(self.request.uri)
        template_values['id'] = ID
        template_values['name'] = name
        template_values['picture'] = picture
        template_values['profile'] = profile
        template_values['factory'] = factory
        template_values['producer'] = producer 
        template_values['products'] = products 
        template_values['latitude'] = latitude
        template_values['longitude'] = longitude
        template_values['url'] = self.request.url  
        
        if worker.getPicture():
            template_values['has_image'] = True
        else:
            template_values['has_image'] = False
    
        template_values['can_edit'] = False
        user = users.get_current_user()
        if user:
            if worker.owner == user:
                template_values['can_edit'] = True
    
        path = os.path.join(os.path.dirname(__file__), 'viewworker.html')
        self.response.out.write(template.render(path, template_values))
        return
    
    '''
    Exception handler
    '''
    def handle_exception(self, exception, debug_mode):
        if debug_mode:
            super(ViewWorker, self).handle_exception(exception, debug_mode)
        else:
            template_values = bene_util.initTemplate(self.request.uri)
            path = os.path.join(os.path.dirname(__file__), 'not_found.html')
            self.response.out.write(template.render(path, template_values))
            return
        

class WorkerImage(webapp.RequestHandler):
    def get(self):
        # Get the id from the get parameter
        ID = self.request.get('id') 
        if not ID:
            '''
            TODO: what to do here?
            '''
            return
        # Fetch the image for this worker
        worker = db.get(ID)
        if not worker:
            '''
            TODO: what to do here?
            '''
            return
        self.response.headers['Content-Type'] = 'image'
        self.response.out.write(worker.getPicture())
        return
    
    '''
    Exception handler
    '''
    def handle_exception(self, exception, debug_mode):
        if debug_mode:
            super(WorkerImage, self).handle_exception(exception, debug_mode)
        else:
            template_values = bene_util.initTemplate(self.request.uri)
            path = os.path.join(os.path.dirname(__file__), 'not_found.html')
            self.response.out.write(template.render(path, template_values))
            return