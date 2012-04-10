from google.appengine.api import users
from google.appengine.ext import db, webapp
from google.appengine.ext.webapp import template
import bene_util
import entities
import os
import urllib



"""
Creates a form to create a Worker
"""
class CreateWorkerPage(webapp.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if user: # if user not signed in
            _producer = bene_util.getCurrentProducer()
            if _producer == None: # if producer page doesn't exist, need to create one
                self.redirect('/signup?%s' % urllib.urlencode({'redirect': 'createworker', 'msg': True}))
            else: # if producer page exists
                if _producer.verified: # if producer is verified, display form to create new worker
                    factory_names = []
                    factories = bene_util.getCurrentProducer().factories()
                    for factory in factories:
                        factory_names.append(factory.name)
                    template_values = bene_util.decodeURL(self.request.uri)
                    template_values['factory_names'] = factory_names
                
                    path = os.path.join(os.path.dirname(__file__), 'createworker.html')
                    self.response.out.write(template.render(path, template_values))
                else: # if not verified
                    self.redirect('/producerhome?%s' % urllib.urlencode({'verify': True}))
        else: # otherwise, request sign in
            self.redirect(users.create_login_url(self.request.uri))
"""
Puts a worker in the database
"""
class StoreWorkerPage(webapp.RequestHandler):
    def post(self):
        user = users.get_current_user()
        if user: # if user signed in
            _producer = bene_util.getCurrentProducer()
            if _producer == None: # if producer page doesn't exist, need to create one
                self.redirect('/signup?%s' % urllib.urlencode({'redirect': 'storeworker', 'msg': True}))
            else: # if producer page exists
                if _producer.verified: # if producer is verified, then store
                    _name = self.request.get('name')
                    _factoryName = self.request.get('factoryName')
                    _picture = self.request.get('picture')
                    _profile = self.request.get('profile')
                    _unique = self.request.get('unique')
                    if isinstance(_picture, unicode):
                        _picture = _picture.encode('utf-8', 'replace')
                    _factoryMade = _producer.factories().filter("name = ", _factoryName).get()
        
                    f = entities.Worker(name=_name, 
                                        producer = _producer, 
                                        factory=_factoryMade, 
                                        profile=_profile,
                                        unique=_unique,
                                        owner=user)
                    f.picture = db.Blob(_picture)
                    if bene_util.doesWorkerExist(f) == False: 
                        f.put()
                        self.redirect('/createworker?%s' % urllib.urlencode({'added': True}))
                    else:
                        self.redirect('/createworker?%s' % urllib.urlencode({'repeat': True}))
                    #self.redirect('/')
                else: # if not verified, then redirect to page with message saying they need to verify 
                    self.redirect('/createworker?%s' % urllib.urlencode({'verify': True}))
                    
        else: # otherwise, request sign in
            self.redirect(users.create_login_url(self.request.uri))