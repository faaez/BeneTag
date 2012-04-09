from google.appengine.api import users
from google.appengine.ext import db, webapp
from google.appengine.ext.webapp import template
import entities
import os
import util



"""
Creates a form to sign up as a Producer
"""
class CreateProducerPage(webapp.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if user: # user signed in
            if util.getCurrentProducer() == None: # no producer page, so create one 
                template_values = {}
                path = os.path.join(os.path.dirname(__file__), 'signup.html')
                self.response.out.write(template.render(path, template_values))
            else: # already has producer page, so redirect
                ''' 
                TODO: Redirect to producer page here.
                If another redirect is specified, e.g. from createfactory, it wouldn't come into this else statement
                (since redirect is specified only if producer page doesn't exist) 
                '''
                self.redirect('/')
        else:
            self.redirect(users.create_login_url(self.request.uri))

"""
Puts a Producer in the database
"""
class StoreProducerPage(webapp.RequestHandler):
    def post(self):
        user = users.get_current_user()
        if user:
            _name = self.request.get('name')
            _logo = self.request.get('logo')
            _description = self.request.get('description')
            if isinstance(_logo, unicode):
                _logo = _logo.encode('utf-8', 'replace')
                
            p = entities.Producer(name = _name, 
                                  email=user.nickname(), 
                                  owner=user,
                                  description=_description,
                                  logo=db.Blob(_logo),
                                  verified=True)
            p.put()

            
            self.redirect('/'+self.request.get('redirect'))
        else:
            self.redirect(users.create_login_url(self.request.uri))
