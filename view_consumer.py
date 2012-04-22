from google.appengine.api import users
from google.appengine.ext import db, webapp
from google.appengine.ext.webapp import template
import os


"""
View a Consumer Page
"""
class ViewConsumer(webapp.RequestHandler):
    def get(self):
        ID = self.request.get('id')
        if not ID:
            '''
            TODO: if no id is sent, defaults to a page with all producers? 
            '''
            self.redirect('/')
            return
        consumer = db.get(ID)
        if not consumer:
            '''
            TODO: if no id is sent, defaults to a page with all workers? 
            '''
            #workerlist = entities.Worker.all()
            template_values = {}
            path = os.path.join(os.path.dirname(__file__), 'not_found.html')
            self.response.out.write(template.render(path, template_values))
            return
        # Make a dictionary for template
        name = consumer.name
        profile = consumer.profile
        
        template_values = {}
        template_values['id'] = ID
        template_values['consumer'] = consumer
        template_values['name'] = name
        template_values['profile'] = profile
        
        template_values['can_edit'] = False
        user = users.get_current_user()
        if user:
            if consumer.owner == user:
                template_values['can_edit'] = True           
        
        path = os.path.join(os.path.dirname(__file__), 'viewconsumer.html')
        self.response.out.write(template.render(path, template_values))
        return
    
    '''
    Exception handler
    '''
    def handle_exception(self, exception, debug_mode):
        if debug_mode:
            super(ViewConsumer, self).handle_exception(exception, debug_mode)
        else:
            template_values = {}
            path = os.path.join(os.path.dirname(__file__), 'not_found.html')
            self.response.out.write(template.render(path, template_values))
            return
        
class ConsumerImage(webapp.RequestHandler):
    def get(self):
        # Get the id from the get parameter
        ID = self.request.get('id') 
        if not ID:
            '''
            TODO: what to do here?
            '''
            return
        # Fetch the image for this worker
        consumer = db.get(ID)
        if not consumer:
            '''
            TODO: what to do here?
            '''
            return
        self.response.headers['Content-Type'] = 'image'
        self.response.out.write(consumer.getPicture()) 
        return
    
    '''
    Exception handler
    '''
    def handle_exception(self, exception, debug_mode):
        if debug_mode:
            super(ConsumerImage, self).handle_exception(exception, debug_mode)
        else:
            template_values = {}
            path = os.path.join(os.path.dirname(__file__), 'not_found.html')
            self.response.out.write(template.render(path, template_values))
            return
