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
class CreateProductPage(webapp.RequestHandler):
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
        
        template_values = bene_util.urldecode(self.request.uri)
        template_values['factories'] = _producer.getFactories()
        template_values['workers'] = _producer.getWorkers()
        template_values['badges'] = entities.Badge.all()
        path = os.path.join(os.path.dirname(__file__), 'createproduct.html')
        self.response.out.write(template.render(path, template_values))
        return
    
    '''
    Exception handler
    '''
    def handle_exception(self, exception, debug_mode):
        if debug_mode:
            super(CreateProductPage, self).handle_exception(exception, debug_mode)
        else:
            template_values = {}
            path = os.path.join(os.path.dirname(__file__), 'not_found.html')
            self.response.out.write(template.render(path, template_values))
            return
            
      
"""
Page that stores Product in datastore
"""
class StoreProductPage(webapp.RequestHandler):
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
        
        _name = self.request.get('name')
        _factory = self.request.get_all('factory')
        _workers = self.request.get_all('workers')
        _badges = self.request.get_all('badges')
        _picture = self.request.get('picture')
        _unique = self.request.get('unique')
                            
        p = entities.Product(name=_name, 
                             unique=_unique,
                             owner=user)
        p.addPicture(_picture)
        if _factory:
            p.addFactory(db.get(_factory))       
        p.addProducer(_producer)
        for _badge in _badges:
            p.addBadge(_badge)
                    
        if bene_util.doesProductExist(p): # already exists
            self.redirect('/createproduct?%s' % urllib.urlencode({'repeat': True}))
            return
        
        p.put()
            
        # add product to workers
        if _workers:
            key = p.key()
            for _worker in _workers:
                if _worker:
                    worker = db.get(_worker)
                    worker.addProduct(key)
                    worker.put()
           
        if self.request.get('more'): # want to add more
            self.redirect('/createproduct?%s' % urllib.urlencode({'added': True}))
            return
        
        # otherwise redirect to product page
        self.redirect('/mobilepage?%s' % urllib.urlencode({'id' : p.key()}))
                   
            
    '''
    Exception handler
    '''
    def handle_exception(self, exception, debug_mode):
        if debug_mode:
            super(StoreProductPage, self).handle_exception(exception, debug_mode)
        else:
            template_values = {}
            path = os.path.join(os.path.dirname(__file__), 'not_found.html')
            self.response.out.write(template.render(path, template_values))
            return