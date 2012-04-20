from google.appengine.api import users
from google.appengine.ext import db, webapp
from google.appengine.ext.webapp import template
import bene_util
import entities
import os
import urllib


"""
Creates a form for Producers to enter information 
about a Product
"""
class EditProductPage(webapp.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if user: # if user signed in
            _producer = bene_util.getCurrentProducer()
            if _producer == None: # if producer page doesn't exist, need to create one
                self.redirect('/signup')
                return
            else: # if producer page exists
                if _producer.verified: # if verified
                    ID = self.request.get('id')
                    _product = db.get(ID)
                    if not _product: # product doesn't exist
                        self.redirect('/producerhome?%s' % urllib.urlencode({'not_exist': True}))
                        return
                    if _product.owner == user: # if current user owns product
                        template_values = bene_util.decodeURL(self.request.uri)
                        template_values['id'] = ID 
                        _factories_old = [_product.factory]
                        _workers_old = _product.workers()
                        _badges_old = _product.badges
                        template_values['factories_old'] = _factories_old
                        template_values['workers_old'] = _workers_old
                        template_values['badges_old'] = _badges_old
                        template_values['unique_old'] = _product.unique
                        template_values['name_old'] = _product.name
                        
                        '''
                        TODO: Find better way to do below. For some reason equality doesn't work implicitly. 
                        Need to explicitly check equality of key()
                        '''
                        template_values['factories'] = []
                        for factory in _producer.factories():
                            add = True
                            for factory_old in _factories_old:
                                if factory.key() == factory_old.key():
                                    add = False
                            if add:
                                template_values['factories'].append(factory)
                        
                        template_values['workers'] = []
                        for worker in _producer.workers():
                            add = True
                            for worker_old in _workers_old:
                                if worker.key() == worker_old.key():
                                    add = False
                            if add:
                                template_values['workers'].append(worker)
                                
                        template_values['badges'] = []
                        for badge in entities.Badge.all():
                            add = True
                            for badge_old in _badges_old:
                                if badge.key() == badge_old.key():
                                    add = False
                            if add:
                                template_values['workers'].append(badge)
                                
                        path = os.path.join(os.path.dirname(__file__), 'editproduct.html')
                        self.response.out.write(template.render(path, template_values))
                        return
                    else: # if user doesn't own product
                        self.redirect('/producerhome?%s' % urllib.urlencode({'not_owner': True}))
                        return
                else: # if not verified
                    self.redirect('/producerhome?%s' % urllib.urlencode({'verify': True}))
                    return
        else: # otherwise, request sign in
            self.redirect(users.create_login_url(self.request.uri))
            
      
"""
Page that stores Product in datastore
"""
class StoreEditedProductPage(webapp.RequestHandler):
    def post(self):
        user = users.get_current_user()
        if user: # if user signed in
            _producer = bene_util.getCurrentProducer()
            if _producer == None: # if producer page doesn't exist, need to create one
                self.redirect('/signup')
                return
            else: # if producer page exists
                if _producer.verified: # if producer is verified, then store
                    ID = self.request.get('id')
                    _product = db.get(ID)
                    if not _product: # product doesn't exist
                        self.redirect('/producerhome?%s' % urllib.urlencode({'not_exist': True}))
                        return
                    if _product.owner == user: # if current user owns product
                        _product.name = self.request.get('name')
                        _factory = self.request.get('factory')
                        _product.factory = db.get(_factory)
                        _unique_save = _product.unique
                        _product.unique = self.request.get('unique')
                        
                        # picture
                        _picture = self.request.POST["picture"]
                        if _picture:
                            if isinstance(_picture, unicode):
                                _product.picture = _picture.encode('utf-8', 'replace')
                            else:
                                _product.picture = _picture
                                
                        # badges
                        _badges = self.request.get_all('badges')
                        _badges_add = []
                        for _badge in _badges:
                            _badges_add.append(db.Key(_badge))
                        _product.badges = _badges_add
                        
                        if bene_util.doesProductExist(_product) and _unique_save != _product.unique: # if product already exists
                            self.redirect('/editproduct?%s' % (urllib.urlencode({'id' : ID, 'repeatedit' : True})))
                            return
                        else:
                            _product.put()                                 
                            # workers
                            ''' 
                            TODO: Find better way to do below. Shouldn't need to delete product from all old workers
                            and then re-add
                            '''
                            _workers = self.request.get_all('workers')
                            _workers_old = _product.workers()
                            key = _product.key()
                            if _workers_old:
                                for worker in _workers_old:
                                    worker.product.remove(key)
                                    worker.put()
                            if _workers:
                                for _worker in _workers:
                                    worker = db.get(_worker)
                                    worker.product.append(key)
                                    worker.put()
                            
                            self.redirect('/mobilepage?%s' % urllib.urlencode({'id': ID}))
                            return
                                                
                    else: # if user doesn't own product
                        self.redirect('/producerhome?%s' % urllib.urlencode({'not_owner': True}))
                        return
                    #self.redirect('/mobilepage?id=' + str(p.key()))
                else: # if not verified
                    self.redirect('/producerhome?%s' % urllib.urlencode({'verify': True}))
                    return
        else: # if not logged in
            self.redirect(users.create_login_url(self.request.uri))
            return
