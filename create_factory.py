from google.appengine.api import users
from google.appengine.ext import db, webapp
from google.appengine.ext.webapp import template
from pprint import pprint
import cgi
import entities
import logging
import os
import urllib
import bene_util



"""
Creates a form for Producers to enter information
about a Factory
"""
class CreateFactoryPage(webapp.RequestHandler):
    def get(self):
        user = users.get_current_user() 
        if user: # user signed in
            if bene_util.getCurrentProducer() == None: # no producer signed up, so ask to sign up
                self.redirect('/signup?%s' % urllib.urlencode({'redirect': 'createfactory', 'msg': True}))
            else: #if producer signed up
                template_values = bene_util.decodeURL(self.request.uri)
                path = os.path.join(os.path.dirname(__file__), 'createfactory.html')
                self.response.out.write(template.render(path, template_values))
        else: # ask to sign in
            self.redirect(users.create_login_url(self.request.uri))

"""
Page that stores Factory in datastore
"""
class StoreFactoryPage(webapp.RequestHandler):
    def post(self):
        user = users.get_current_user()
        
        if user: # user signed in
            if bene_util.getCurrentProducer() == None: # no producer signed up, so ask to sign up
                self.redirect('/signup?%s' % urllib.urlencode({'redirect': 'storefactory', 'msg': True}))
            else: # if producer signed up
                _name = self.request.get('name')
                _address = self.request.get('address')
                _location = self.request.get('location')
                
                fields = _location.split(',')
                if len(fields) == 2:
                    try:
                        lat = float(fields[0])
                        lon = float(fields[1])
                        gp = db.GeoPt(lat, lon)
                    except ValueError:
                        gp = None
                else:
                    gp = None
                f = entities.Factory(name=_name,
                                     producer=bene_util.getCurrentProducer(),
                                     address=_address,
                                     location=gp)
        
                if bene_util.doesFactoryExist(f) == False: 
                    f.put()
                    self.redirect('/createfactory?%s' % urllib.urlencode({'added': True}))
                else:
                    self.redirect('/createfactory?%s' % urllib.urlencode({'repeat': True}))
        else: # user not signed in
            self.redirect(users.create_login_url(self.request.uri))
