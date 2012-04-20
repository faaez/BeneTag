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
        if user: # if user signed in
            if bene_util.getCurrentUser().isConsumer:
                self.redirect('/')
                return
            _producer = bene_util.getCurrentProducer()
            if _producer == None: # if producer page doesn't exist, need to create one
                self.redirect('/createproducer?%s' % urllib.urlencode({'redirect': 'createworker', 'msg': True}))
                return
            else: # if producer page exists
                if _producer.verified: # if producer is verified, display form to create new worker
                    template_values = bene_util.decodeURL(self.request.uri)
                    template_values['factories'] = bene_util.getCurrentProducer().factories()
                
                    path = os.path.join(os.path.dirname(__file__), 'createworker.html')
                    self.response.out.write(template.render(path, template_values))
                    return
                else: # if not verified
                    self.redirect('/producerhome?%s' % urllib.urlencode({'verify': True}))
                    return
        else: # otherwise, request sign in
            self.redirect(users.create_login_url(self.request.uri))
            return
"""
Puts a worker in the database
"""
class StoreWorkerPage(webapp.RequestHandler):
    def post(self):
        user = users.get_current_user()
        if user: # if user signed in
            if bene_util.getCurrentUser().isConsumer:
                self.redirect('/')
                return
            _producer = bene_util.getCurrentProducer()
            if _producer == None: # if producer page doesn't exist, need to create one
                self.redirect('/createproducer?%s' % urllib.urlencode({'redirect': 'storeworker', 'msg': True}))
                return
            else: # if producer page exists
                if _producer.verified: # if producer is verified, then store
                    _name = self.request.get('name')
                    _factory = self.request.get('factory')
                    _picture = self.request.get('picture')
                    _profile = self.request.get('profile')
                    _unique = self.request.get('unique')
                    
                    if _factory:
                        _factoryMade = db.get(_factory)
        
                    f = entities.Worker(name=_name, 
                                        producer = _producer, 
                                        factory=_factoryMade, 
                                        profile=_profile,
                                        unique=_unique,
                                        owner=user)
                    if _picture:
                        if isinstance(_picture, unicode):
                            _picture = _picture.encode('utf-8', 'replace')
                        f.picture = db.Blob(_picture)
                    if bene_util.doesWorkerExist(f) == False: 
                        f.put()
                        self.redirect('/createworker?%s' % urllib.urlencode({'added': True}))
                        return
                    else:
                        self.redirect('/createworker?%s' % urllib.urlencode({'repeat': True}))
                        return
                    #self.redirect('/')
                else: # if not verified, then redirect to page with message saying they need to verify 
                    self.redirect('/createworker?%s' % urllib.urlencode({'verify': True}))
                    return
                    
        else: # otherwise, request sign in
            self.redirect(users.create_login_url(self.request.uri))
            return