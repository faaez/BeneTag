from google.appengine.api import users
from google.appengine.ext import db, webapp
from google.appengine.ext.webapp import template
import bene_util
import entities
import os
import urllib



"""
Creates a form for Producers to enter information
about a Factory
"""
class CreateFactoryPage(webapp.RequestHandler):
    def get(self):
        user = users.get_current_user() 
        if user: # user signed in
            _producer = bene_util.getCurrentProducer()
            if _producer  == None: # no producer signed up, so ask to sign up
                self.redirect('/signup?%s' % urllib.urlencode({'redirect': 'createfactory', 'msg': True}))
            else: #if producer signed up
                if _producer.verified: # if producer is verified
                    template_values = bene_util.decodeURL(self.request.uri)
                    path = os.path.join(os.path.dirname(__file__), 'createfactory.html')
                    self.response.out.write(template.render(path, template_values))
                else: # if producer is not verified
                    self.redirect('/producerhome?%s' % urllib.urlencode({'verify': True}))
        else: # ask to sign in
            self.redirect(users.create_login_url(self.request.uri))

"""
Page that stores Factory in datastore
"""
class StoreFactoryPage(webapp.RequestHandler):
    def post(self):
        user = users.get_current_user()
        
        if user: # user signed in
            _producer = bene_util.getCurrentProducer()
            if _producer == None: # no producer signed up, so ask to sign up
                self.redirect('/signup?%s' % urllib.urlencode({'redirect': 'storefactory', 'msg': True}))
            else: # if producer signed up
                if _producer.verified: # if producer is verified
                    _name = self.request.get('name')
                    _address = self.request.get('address')
                    _location = self.request.get('location')
                    _unique = self.request.get('unique')
                                                                               
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
                                         producer=_producer,
                                         address=_address,
                                         location=gp,
                                         unique=_unique,
                                         owner=user)
                    if bene_util.doesFactoryExist(f) == False: 
                        f.put()
                        self.redirect('/createfactory?%s' % urllib.urlencode({'added': True}))
                    else:
                        self.redirect('/createfactory?%s' % urllib.urlencode({'repeat': True}))
                else: # if not verified
                    self.redirect('/createfactory?%s' % urllib.urlencode({'verify': True}))
        else: # user not signed in
            self.redirect(users.create_login_url(self.request.uri))
