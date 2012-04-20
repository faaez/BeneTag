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
class EditFactoryPage(webapp.RequestHandler):
    def get(self):
        user = users.get_current_user() 
        if user: # user signed in
            if bene_util.getCurrentUser().isConsumer:
                self.redirect('/')
                return
            _producer = bene_util.getCurrentProducer()
            if _producer  == None: # no producer signed up, so ask to sign up
                self.redirect('/createproducer')
                return
            else: #if producer signed up
                if _producer.verified: # if producer is verified
                    ID = self.request.get('id')
                    _factory = db.get(ID)
                    if not _factory:
                        self.redirect('/producerhome?%s' % urllib.urlencode({'not_exist': True}))
                        return
                    if _factory.owner == user: # if owner of factory
                        template_values = bene_util.decodeURL(self.request.uri)
                        template_values['id'] = ID
                        template_values['name_old'] = _factory.name
                        template_values['address_old'] = _factory.address
                        template_values['unique_old'] = _factory.unique
                        
                        path = os.path.join(os.path.dirname(__file__), 'editfactory.html')
                        self.response.out.write(template.render(path, template_values))
                        return
                    else: # if user doesn't own factory
                        self.redirect('/producerhome?%s' % urllib.urlencode({'not_owner': True}))
                        return
                else: # if producer is not verified
                    self.redirect('/producerhome?%s' % urllib.urlencode({'verify': True}))
                    return
        else: # ask to sign in
            self.redirect('/?signin=True')
            return

"""
Page that stores Factory in datastore
"""
class StoreEditedFactoryPage(webapp.RequestHandler):
    def post(self):
        user = users.get_current_user()
        
        if user: # user signed in
            if bene_util.getCurrentUser().isConsumer:
                self.redirect('/')
                return
            _producer = bene_util.getCurrentProducer()
            if _producer == None: # no producer signed up, so ask to sign up
                self.redirect('/createproducer')
                return
            else: # if producer signed up
                if _producer.verified: # if producer is verified
                    ID = self.request.get('id')
                    _factory = db.get(ID)
                    if not _factory: # factory doesn't exist
                        self.redirect('/producerhome?%s' % urllib.urlencode({'not_exist': True}))
                        return
                    if _factory.owner == user: # factory is owned by current user
                        _factory.name = self.request.get('name')
                        _factory.address = self.request.get('address')
                        _unique_save = _factory.unique
                        _factory.unique = self.request.get('unique')
                        _picture = self.request.get('picture')
                                                                      
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
                        _factory.location = gp
                                                                 
                        if _picture:
                            if isinstance(_picture, unicode):
                                _picture = _picture.encode('utf-8', 'replace')
                            _factory.picture = db.Blob(_picture.value)
                        if bene_util.doesFactoryExist(_factory) and _unique_save != _factory.unique : # if factory with same unique exists
                            self.redirect('/editfactory?%s' % (urllib.urlencode({'id' : ID, 'repeatedit' : True})))
                            return 
                        else:
                            _factory.put()
                            self.redirect('/viewfactory?%s' % urllib.urlencode({'id': ID}))
                            return
                    else: # if user doesn't own factory
                        self.redirect('/producerhome?%s' % urllib.urlencode({'not_owner': True}))
                        return
                else: # if not verified
                    self.redirect('/producerhome?%s' % urllib.urlencode({'verify': True}))
                    return
        else: # user not signed in
            self.redirect('/?signin=True')
            return
