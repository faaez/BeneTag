from google.appengine.api import users
from google.appengine.ext import db, webapp
from google.appengine.ext.webapp import template
import bene_query
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
        if not user: # need to sign in
            self.redirect('/?signin=True')
            return
        
        if bene_query.getCurrentUser().isConsumer: # consumers can't access this
            self.redirect('/')
            return
            
        _producer = bene_query.getCurrentProducer()
        if _producer  == None: # no producer signed up, so ask to sign up
            self.redirect('/')
            return
        
        if not _producer.verified: # if producer is not verified
            self.redirect('/producerhome?%s' % urllib.urlencode({'verify': True}))
            return
                    
        ID = self.request.get('id')
        if not ID:
            '''
            TODO: If no ID sent?
            '''
            self.redirect('/')
            return
        _product = db.get(ID)
        if not _product: # product doesn't exist
            template_values = bene_util.initTemplate(self.request.uri)
            path = os.path.join(os.path.dirname(__file__), 'not_found.html')
            self.response.out.write(template.render(path, template_values))
            return
        
        if _product.owner != user: # if current user doesn't own product
            self.redirect('/producerhome?%s' % urllib.urlencode({'not_owner': True}))
            return
                        
        _factories_old = _product.getFactories()
        _workers_old = _product.getWorkers()
        _badges_old = _product.getBadges()
        template_values = bene_util.initTemplate(self.request.uri)
        template_values['id'] = ID
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
        _factories = _producer.getFactories()
        if _factories:
            for factory in _factories:
                if factory:
                    add = True
                    if _factories_old:
                        for factory_old in _factories_old:
                            if factory_old:
                                if factory_old.key() == factory.key():
                                    add = False
                    if add:
                        template_values['factories'].append(factory)
                        
        template_values['workers'] = []
        _workers = _producer.getWorkers()
        if _workers:
            for worker in _workers:
                if worker:
                    add = True
                    if _workers_old:
                        for worker_old in _workers_old:
                            if worker_old:
                                if worker_old.key() == worker.key():
                                    add = False
                    if add:
                        template_values['workers'].append(worker)
                                
        template_values['badges'] = []
        _badges = entities.Badge.all()
        if _badges:
            for badge in _badges:
                if badge:
                    add = True
                    if _badges_old:
                        for badge_old in _badges_old:
                            if badge_old.key() == badge.key():
                                add = False
                    if add:
                        template_values['badges'].append(badge)
                    
        path = os.path.join(os.path.dirname(__file__), 'editproduct.html')
        self.response.out.write(template.render(path, template_values))
        return
    
    '''
    Exception handler
    '''
    def handle_exception(self, exception, debug_mode):
        if debug_mode:
            super(EditProductPage, self).handle_exception(exception, debug_mode)
        else:
            template_values = bene_util.initTemplate(self.request.uri)
            path = os.path.join(os.path.dirname(__file__), 'not_found.html')
            self.response.out.write(template.render(path, template_values))
            return
                             
"""
Page that stores Product in datastore
"""
class StoreEditedProductPage(webapp.RequestHandler):
    def post(self):
        user = users.get_current_user() 
        if not user: # need to sign in
            self.redirect('/?signin=True')
            return
        
        if bene_query.getCurrentUser().isConsumer: # consumers can't access this
            self.redirect('/')
            return
            
        _producer = bene_query.getCurrentProducer()
        if _producer  == None: # no producer signed up, so ask to sign up
            self.redirect('/')
            return
        
        if not _producer.verified: # if producer is not verified
            self.redirect('/producerhome?%s' % urllib.urlencode({'verify': True}))
            return
                    
        ID = self.request.get('id')
        if not ID:
            '''
            TODO: If no ID sent?
            '''
            self.redirect('/')
            return
        _product = db.get(ID)
        if not _product: # product doesn't exist
            template_values = bene_util.initTemplate(self.request.uri)
            path = os.path.join(os.path.dirname(__file__), 'not_found.html')
            self.response.out.write(template.render(path, template_values))
            return
        
        if _product.owner != user: # if current user doesn't own product
            self.redirect('/producerhome?%s' % urllib.urlencode({'not_owner': True}))
            return
        
        _product.name = self.request.get('name')
        _unique_save = _product.unique
        _product.unique = self.request.get('unique')
        if bene_util.doesProductExist(_product) and _unique_save != _product.unique: # if product already exists
            self.redirect('/editproduct?%s' % (urllib.urlencode({'id' : ID, 'repeatedit' : True})))
            return
        
        _factory = self.request.get('factory')
        if _factory:
            _product.addFactory(db.get(_factory))      
        
        _picture = self.request.get('picture')
        _product.addPicture(_picture)
        
        # badges
        _badges = self.request.get_all('badges')
        _badges_old = _product.getBadges()
        if _badges_old:
            for badge in _badges_old:
                if not _badges: # convert None to empty array
                    _badges = []
                if badge not in _badges:
                    _product.remBadge(badge)
        if _badges:
            for badge in _badges:
                if not _badges_old: # convert None to empty array
                    _badges_old = []
                if badge not in _badges_old:
                    _product.addBadge(badge)
            
        _product.put()                                 
        
        # workers
        '''
        TODO: FIX THIS. Make it more efficient
        '''
        _workers = self.request.get_all('workers')
        _workers_old = _product.getWorkers()
        key = _product.key()
        if _workers_old:
            for worker in _workers_old:
                    worker.remProduct(key)
                    worker.put()
        if _workers:
            for _worker in _workers:
                if _worker:
                    worker = db.get(_worker)
                    worker.addProduct(key)
                    worker.put()
                            
        self.redirect('/mobilepage?%s' % urllib.urlencode({'id': ID}))
        return
    
    '''
    Exception handler
    '''
    def handle_exception(self, exception, debug_mode):
        if debug_mode:
            super(StoreEditedProductPage, self).handle_exception(exception, debug_mode)
        else:
            template_values = bene_util.initTemplate(self.request.uri)
            path = os.path.join(os.path.dirname(__file__), 'not_found.html')
            self.response.out.write(template.render(path, template_values))
            return