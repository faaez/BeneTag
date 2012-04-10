from google.appengine.api import users
from google.appengine.ext import db, webapp
from google.appengine.ext.webapp import template
import bene_util
import entities
import os
import urllib

'''
TODO: Add self loops to products. Too sleepy now to figure out why it's not showing

'''

"""
Creates a form for Producers to enter information 
about a Product
"""
class CreateProductPage(webapp.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if user: # if user signed in
            if bene_util.getCurrentProducer() == None: # if producer page doesn't exist, need to create one
                self.redirect('/signup?%s' % urllib.urlencode({'redirect': 'createproduct', 'msg': True}))
            else: # if producer page exists, create form to get new product        
                factory_names = []
                factories = bene_util.getCurrentProducer().factories()
                for factory in factories:
                    factory_names.append(factory.name)
                template_values = bene_util.decodeURL(self.request.uri)
                template_values['factory_names'] = factory_names
                template_values['badges'] = entities.Badge.all()
                path = os.path.join(os.path.dirname(__file__), 'createproduct.html')
                self.response.out.write(template.render(path, template_values))
        else: # otherwise, request sign in
            self.redirect(users.create_login_url(self.request.uri))
            
      
"""
Page that stores Product in datastore
"""
class StoreProductPage(webapp.RequestHandler):
    def post(self):
        user = users.get_current_user()
        if user: # if user not signed in
            if bene_util.getCurrentProducer() == None: # if producer page doesn't exist, need to create one
                self.redirect('/signup?%s' % urllib.urlencode({'redirect': 'storeproduct', 'msg': True}))
            else: # if producer page exists, store new product
                _name = self.request.get('name')
                _producer = entities.Producer.gql("WHERE name = :1", self.request.get('producerName')).get()
                _factoryName = self.request.get('factoryName')
                _badges = self.request.get_all('badges')
                _picture = self.request.get('picture')
                if isinstance(_picture, unicode):
                    _picture = _picture.encode('utf-8', 'replace')
                _factoryMade = entities.Factory.gql("WHERE name = :1", _factoryName).get()
                
                p = entities.Product(name=_name, producer=_producer, factory=_factoryMade)
                for _badge in _badges:
                    p.badges.append(db.Key(_badge))
                p.picture = db.Blob(_picture)
                
                if bene_util.doesProductExist(p) == False: 
                    p.put()
                    self.redirect('/createproduct?%s' % urllib.urlencode({'added': True}))
                else:
                    self.redirect('/createproduct?%s' % urllib.urlencode({'repeat': True}))
                #self.redirect('/mobilepage?id=' + str(p.key()))
        else:
            self.redirect(users.create_login_url(self.request.uri))
