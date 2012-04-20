from google.appengine.api import users
from google.appengine.ext import db, webapp
from google.appengine.ext.webapp import template
import entities
import os
import bene_util

"""
Creates a form to sign up as a Producer
"""
class CreateConsumerPage(webapp.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if user: # user signed in
            if bene_util.getCurrentUser().isProducer:
                self.redirect('/')
                return
            if bene_util.getCurrentConsumer() == None: # no producer page, so create one 
                template_values = bene_util.decodeURL(self.request.uri)
                path = os.path.join(os.path.dirname(__file__), 'createconsumer.html')
                self.response.out.write(template.render(path, template_values))
                return
            else: # already has producer page, so redirect
                self.redirect('/consumerhome')
                return
        else: # user not signed in
            self.redirect(users.create_login_url(self.request.uri))
            return

"""
Puts a Producer in the database
"""
class StoreConsumerPage(webapp.RequestHandler):
    def post(self):
        user = users.get_current_user()
        if user:
            if bene_util.getCurrentUser().isProducer:
                self.redirect('/')
                return
            if bene_util.getCurrentConsumer() == None: # no producer, so add to store
                '''
                TODO: If for some reason user refreshes store producer page, then they should get a warning of some sort?
                Another way this could happen is if they store, and then press back to the signup page, and press store again.
                What to do in that case? Warning or just ignore? Currently, we're just ignoring
                Note that this could be deliberate attempt by user to change value
                '''
                _name = self.request.get('name')
                _picture = self.request.get('picture')
                _profile = self.request.get('profile')
                    
                p = entities.Consumer(name = _name, 
                                      email=user.nickname(), 
                                      owner=user,
                                      profile=_profile,                      
                                      verified=False)
                if _picture:
                    if isinstance(_picture, unicode):
                        _picture = _picture.encode('utf-8', 'replace')
                    p.logo=db.Blob(_picture),
                p.put()
                        
            self.redirect('/'+self.request.get('redirect'))
        else:
            self.redirect(users.create_login_url(self.request.uri))
