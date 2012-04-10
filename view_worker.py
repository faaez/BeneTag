from google.appengine.ext import db, webapp
from google.appengine.ext.webapp import template
import os



"""
View a Worker Page
"""
class ViewWorker(webapp.RequestHandler):
    def get(self):
        ID = self.request.get('id')
        worker = db.get(ID)
        if not worker:
            '''
            TODO: if no id is sent, defaults to a page with all workers? 
            '''
            #workerlist = entities.Worker.all()
            template_values = {}
            path = os.path.join(os.path.dirname(__file__), 'not_found.html')
            self.response.out.write(template.render(path, template_values))
            return
        # Make a dictionary for template
        name = worker.name
        factory = worker.factory
        profile = worker.profile
        picture = worker.picture
        producer = worker.producer
        if worker.factory.location:
            latitude = worker.factory.location.lat
            longitude = worker.factory.location.lon
        else:
            latitude = None
            longitude = None
        template_values = {}
        template_values['id'] = ID
        template_values['name'] = name
        template_values['factory'] = factory
        template_values['picture'] = picture
        template_values['profile'] = profile
        template_values['latitude'] = latitude
        template_values['longitude'] = longitude
        template_values['url'] = self.request.url
        ''' TODO: display information about producer (employer) of worker: '''
        template_values['producer'] = producer  
        if worker.picture:
            template_values['has_image'] = True
        else:
            template_values['has_image'] = False
    
        path = os.path.join(os.path.dirname(__file__), 'viewworker.html')
        self.response.out.write(template.render(path, template_values))

class WorkerImage(webapp.RequestHandler):
    def get(self):
        # Get the id from the get parameter
        ID = self.request.get('id') 
        # Fetch the image for this worker
        worker = db.get(ID)
        self.response.headers['Content-Type'] = 'image'
        self.response.out.write(worker.picture)
