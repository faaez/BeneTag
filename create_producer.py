from google.appengine.api import users
from google.appengine.ext import db, webapp
from google.appengine.ext.webapp import template
import entities
import os
import bene_util

"""
Creates a form to sign up as a Producer
"""
class CreateProducerPage(webapp.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if user: # user signed in
            if bene_util.getCurrentUser().isConsumer:
                self.redirect('/')
                return
            if bene_util.getCurrentProducer() == None: # no producer page, so create one 
                template_values = bene_util.decodeURL(self.request.uri)
                path = os.path.join(os.path.dirname(__file__), 'createproducer.html')
                self.response.out.write(template.render(path, template_values))
                return
            else: # already has producer page, so redirect
                self.redirect('/producerhome')
                return
        else: # user not signed in
            self.redirect('/?signin=True')
            return
        
"""
Puts a Producer in the database
"""
class StoreProducerPage(webapp.RequestHandler):
    def post(self):
        user = users.get_current_user()
        if user:
            if bene_util.getCurrentUser().isConsumer:
                self.redirect('/')
                return
            if bene_util.getCurrentProducer() == None: # no producer, so add to store
                '''
                TODO: If for some reason user refreshes store producer page, then they should get a warning of some sort?
                Another way this could happen is if they store, and then press back to the signup page, and press store again.
                What to do in that case? Warning or just ignore? Currently, we're just ignoring
                Note that this could be deliberate attempt by user to change value
                '''
                _name = self.request.get('name')
                _logo = self.request.get('logo')
                _description = self.request.get('description')
                
                    
                p = entities.Producer(name = _name, 
                                      email=user.nickname(), 
                                      owner=user,
                                      description=_description,
                                      verified=False)
                if _logo:
                    if isinstance(_logo, unicode):
                        _logo = _logo.encode('utf-8', 'replace')
                    p.logo=db.Blob(_logo),
                p.put()
                        
            self.redirect('/'+self.request.get('redirect'))
            return
        else:
            self.redirect('/?signin=True')
            return
