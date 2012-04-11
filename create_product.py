from google.appengine.api import users
from google.appengine.ext import db, webapp
from google.appengine.ext.webapp import template
import bene_util
import entities
import os
import urllib
import logging

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
            _producer = bene_util.getCurrentProducer()
            if _producer == None: # if producer page doesn't exist, need to create one
                self.redirect('/signup?%s' % urllib.urlencode({'redirect': 'createproduct', 'msg': True}))
            else: # if producer page exists
                if _producer.verified: # if verified, create form to get new product        
                    template_values = bene_util.decodeURL(self.request.uri)
                    template_values['factories'] = bene_util.getCurrentProducer().factories()
                    template_values['workers'] = bene_util.getCurrentProducer().workers()
                    template_values['badges'] = entities.Badge.all()
                    path = os.path.join(os.path.dirname(__file__), 'createproduct.html')
                    self.response.out.write(template.render(path, template_values))
                else: # if not verified
                    self.redirect('/producerhome?%s' % urllib.urlencode({'verify': True}))
        else: # otherwise, request sign in
            self.redirect(users.create_login_url(self.request.uri))
            
      
"""
Page that stores Product in datastore
"""
class StoreProductPage(webapp.RequestHandler):
    def post(self):
        user = users.get_current_user()
        if user: # if user signed in
            _producer = bene_util.getCurrentProducer()
            if _producer == None: # if producer page doesn't exist, need to create one
                self.redirect('/signup?%s' % urllib.urlencode({'redirect': 'storeproduct', 'msg': True}))
            else: # if producer page exists
                if _producer.verified: # if producer is verified, then store
                    _name = self.request.get('name')
                    _factory = self.request.get('factory')
                    _workers = self.request.get_all('workers')
                    _badges = self.request.get_all('badges')
                    _picture = self.request.get('picture')
                    _unique = self.request.get('unique')
                    if isinstance(_picture, unicode):
                        _picture = _picture.encode('utf-8', 'replace')
                    _factoryMade = db.get(_factory)
                    '''
                    XXX: Assumes factory name is unique for a producer. This is enforced when creating factories
                    '''                   
                    p = entities.Product(name=_name, 
                                         producer=_producer, 
                                         factory=_factoryMade,
                                         unique=_unique,
                                         owner=user)
                    for _badge in _badges:
                        p.badges.append(db.Key(_badge))
                    p.picture = db.Blob(_picture)
                    
                    if bene_util.doesProductExist(p) == False:
                        p.put()
                        ''' add product key to workers who worked on it '''
                        if _workers:
                            key = p.key()
                            for _worker in _workers:
                                worker = db.get(_worker)
                                worker.product.append(key)
                                worker.put()
                        self.redirect('/createproduct?%s' % urllib.urlencode({'added': True}))
                    else:
                        self.redirect('/createproduct?%s' % urllib.urlencode({'repeat': True}))
                    #self.redirect('/mobilepage?id=' + str(p.key()))
                else: # if not verified
                    self.redirect('/createproduct?%s' % urllib.urlencode({'verify': True}))
        else: # if not logged in
            self.redirect(users.create_login_url(self.request.uri))
