from google.appengine.api import users
from google.appengine.ext import db, webapp
from google.appengine.ext.webapp import template
import bene_util
import entities
import os
import sys
import urllib



"""
Creates a form to create a Worker
"""
class EditWorkerPage(webapp.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if user: # if user not signed in
            if bene_util.getCurrentUser().isConsumer:
                self.redirect('/')
                return
            _producer = bene_util.getCurrentProducer()
            if _producer == None: # if producer page doesn't exist, need to create one
                self.redirect('/createproducer')
                return
            else: # if producer page exists
                if _producer.verified: # if producer is verified 
                    ID = self.request.get('id')
                    if not ID:
                        '''
                        TODO: If no ID sent, default to page with all factories?
                        '''
                        self.redirect('/')
                        return
                    _worker = db.get(ID)
                    if not _worker: # doesn't exist
                        self.redirect('/producerhome?%s' % urllib.urlencode({'not_exist': True}))
                        return
                    if _worker.owner == user: #'owner' of worker. I know it sounds very pre-emancipation
                        template_values = bene_util.decodeURL(self.request.uri)
                        template_values['name_old'] = _worker.name
                        template_values['profile_old'] = _worker.profile
                        template_values['unique_old'] = _worker.unique
                        
                        _factories_old = [_worker.factory]
                        template_values['factories_old'] = _factories_old
                        template_values['factories'] = []
                        for factory in bene_util.getCurrentProducer().factories():
                            add = True
                            for factory_old in _factories_old:
                                if factory.key() == factory_old.key():
                                    add = False
                            if add:
                                template_values['factories'].append(factory)
                                            
                        path = os.path.join(os.path.dirname(__file__), 'editworker.html')
                        self.response.out.write(template.render(path, template_values))
                        return
                    else: # if user doesn't own worker
                        self.redirect('/producerhome?%s' % urllib.urlencode({'not_owner': True}))
                        return
                else: # if not verified
                    self.redirect('/producerhome?%s' % urllib.urlencode({'verify': True}))
                    return
        else: # otherwise, request sign in
            self.redirect('/?signin=True')
            return
"""
Puts a worker in the database
"""
class StoreEditedWorkerPage(webapp.RequestHandler):
    def post(self):
        user = users.get_current_user()
        if user: # if user signed in
            if bene_util.getCurrentUser().isConsumer:
                self.redirect('/')
                return
            _producer = bene_util.getCurrentProducer()
            if _producer == None: # if producer page doesn't exist, need to create one
                self.redirect('/createproducer')
                return
            else: # if producer page exists
                if _producer.verified: # if producer is verified, then store
                    ID = self.request.get('id')
                    if not ID:
                        '''
                        TODO: If no ID sent, default to page with all factories?
                        '''
                        self.redirect('/')
                        return
                    _worker = db.get(ID)
                    if not _worker:
                        self.redirect('/producerhome?%s' % urllib.urlencode({'not_exist': True}))
                        return
                    if _worker.owner == user: # if user owns worker
                            
                        _worker.name = self.request.get('name')
                        _worker.profile = self.request.get('profile')

                        _factory = self.request.get('factory')
                        if _factory:
                            _worker.factory = db.get(_factory)
                        
                        _unique_save = _worker.unique
                        _worker.unique = self.request.get('unique')
                        
                        _picture = self.request.get('picture')
                        if _picture:
                            if isinstance(_picture, unicode):
                                _worker.picture = _picture.encode('utf-8', 'replace')
                            else:
                                _worker.picture = _picture
                        if bene_util.doesProductExist(_worker) and _unique_save != _worker.unique: # if product already exists
                            self.redirect('/editworker?%s' % (urllib.urlencode({'id' : ID, 'repeatedit' : True})))
                            return
                        else:
                            _worker.put()
                            self.redirect('/viewworker?%s' % urllib.urlencode({'id': ID}))
                            return  
                        #self.redirect('/')
                    else: # if not owned
                        self.redirect('/producerhome?%s' % urllib.urlencode({'not_owner': True}))
                        return
                        
                else: # if not verified, then redirect to page with message saying they need to verify 
                    self.redirect('/producerhome?%s' % urllib.urlencode({'verify': True}))
                    return
                    
        else: # otherwise, request sign in
            self.redirect('/?signin=True')
            return