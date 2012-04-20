from google.appengine.api import users
from google.appengine.ext import db, webapp
from google.appengine.ext.webapp import template
import bene_util
import entities
import os
import urllib



"""
Creates a form to sign up as a Producer
"""
class EditProducerPage(webapp.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if user: # user signed in
            if bene_util.getCurrentUser().isConsumer:
                self.redirect('/')
                return
            _producer = bene_util.getCurrentProducer();
            if _producer == None: # no producer page, so create one 
                self.redirect('/createproducer')
                return
            else: # already has producer page, so edit
                template_values = bene_util.decodeURL(self.request.uri)
                template_values['name_old'] = _producer.name
                template_values['description_old'] = _producer.description
                path = os.path.join(os.path.dirname(__file__), 'editproducer.html')
                self.response.out.write(template.render(path, template_values))
                return
        else: # user not signed in
            self.redirect('/?signin=True')
            return

"""
Puts a Producer in the database
"""
class StoreEditedProducerPage(webapp.RequestHandler):
    def post(self):
        user = users.get_current_user()
        if user:
            if bene_util.getCurrentUser().isConsumer:
                self.redirect('/')
                return
            _producer = bene_util.getCurrentProducer()
            _name = self.request.get('name')
            _description = self.request.get('description')
            _logo = self.request.get('logo')
            if _logo:
                if isinstance(_logo, unicode):
                    _logo = _logo.encode('utf-8', 'replace')
            if _producer == None: # no producer page, so create one
                p = entities.Producer(name = _name, 
                                      email=user.nickname(), 
                                      owner=user,
                                      description=_description,
                                      logo=db.Blob(_logo),
                                      verified=False)
                p.put()
            else: # otherwise, edit                  
                _producer.name = _name
                _producer.description = _description
                if not _logo:
                    _logo = _producer.logo
                _producer.logo = db.Blob(_logo)
                _producer.put()
                        
            self.redirect('/viewproducer?%s' % urllib.urlencode({'id': _producer.key()}))
            return
        else:
            self.redirect('/?signin=True')
            return
