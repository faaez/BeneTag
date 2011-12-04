import os

from google.appengine.ext import db
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template

from entities import Worker

"""
View a Worker Page
"""
class ViewWorker(webapp.RequestHandler):
    def get(self):
        '''if no id is sent, defaults to last factory'''
        id = self.request.get('id')
        workerlist = Worker.all()
        worker = workerlist[workerlist.count() -1]
        if(id):
            worker = db.get(id)
        if not worker:
          template_values = {}
          path = os.path.join(os.path.dirname(__file__), 'not_found.html')
          self.response.out.write(template.render(path, template_values))
          return
        # Make a dictionary for template
        name = worker.name
        factory = worker.factory
        profile = worker.profile
        picture = worker.picture
        if worker.factory.location:
            latitude = worker.factory.location.lat
            longitude = worker.factory.location.lon
        else:
            latitude = None
            longitude = None
        template_values = {}
        template_values['id'] = id
        template_values['name'] = name
        template_values['factory'] = factory
        template_values['picture'] = picture
        template_values['profile'] = profile
        template_values['latitude'] = latitude
        template_values['longitude'] = longitude
        template_values['url'] = self.request.url
        if worker.picture:
            template_values['has_image'] = True
        else:
            template_values['has_image'] = False
    
        path = os.path.join(os.path.dirname(__file__), 'viewworker.html')
        self.response.out.write(template.render(path, template_values))

class WorkerImage(webapp.RequestHandler):
    def get(self):
        # Get the id from the get parameter
        id = self.request.get('id')
        # Fetch the image for this worker
        worker = db.get(id)
        self.response.headers['Content-Type'] = 'image'
        self.response.out.write(worker.picture)
