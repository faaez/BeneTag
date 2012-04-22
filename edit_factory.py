from google.appengine.api import users
from google.appengine.ext import db, webapp
from google.appengine.ext.webapp import template
import bene_query
import bene_util
import os
import urllib

"""
Creates a form for Producers to enter information
about a Factory
"""
class EditFactoryPage(webapp.RequestHandler):
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
            TODO: If no ID sent, default to page with all factories?
            '''
            self.redirect('/')
            return
        _factory = db.get(ID)
        if not _factory:
            template_values = bene_util.initTemplate(self.request.uri)
            path = os.path.join(os.path.dirname(__file__), 'not_found.html')
            self.response.out.write(template.render(path, template_values))
            return
        
        if _factory.owner != user: # if not owner of factory
            self.redirect('/producerhome?%s' % urllib.urlencode({'not_owner': True}))
            return
        
        template_values = bene_util.initTemplate(self.request.uri)
        template_values['id'] = ID
        template_values['name_old'] = _factory.name
        template_values['address_old'] = _factory.address
        template_values['unique_old'] = _factory.unique
                        
        path = os.path.join(os.path.dirname(__file__), 'editfactory.html')
        self.response.out.write(template.render(path, template_values))
        return
    
    '''
    Exception handler
    '''
    def handle_exception(self, exception, debug_mode):
        if debug_mode:
            super(EditFactoryPage, self).handle_exception(exception, debug_mode)
        else:
            template_values = bene_util.initTemplate(self.request.uri)
            path = os.path.join(os.path.dirname(__file__), 'not_found.html')
            self.response.out.write(template.render(path, template_values))
            return
                        


"""
Page that stores Factory in datastore
"""
class StoreEditedFactoryPage(webapp.RequestHandler):
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
            TODO: If no ID sent, default to page with all factories?
            '''
            self.redirect('/')
            return
        _factory = db.get(ID)
        if not _factory:
            template_values = bene_util.initTemplate(self.request.uri)
            path = os.path.join(os.path.dirname(__file__), 'not_found.html')
            self.response.out.write(template.render(path, template_values))
            return
        
        if _factory.owner != user: # if not owner of factory
            self.redirect('/producerhome?%s' % urllib.urlencode({'not_owner': True}))
            return
        
        _factory.name = self.request.get('name')
        _factory.address = self.request.get('address')
        _unique_save = _factory.unique
        _factory.unique = self.request.get('unique')
        if bene_util.doesFactoryExist(_factory) and _unique_save != _factory.unique : # if factory with same unique exists
            self.redirect('/editfactory?%s' % (urllib.urlencode({'id' : ID, 'repeatedit' : True})))
            return 
                  
        _picture = self.request.get('picture')
        _factory.addPicture(_picture)
                                                                      
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
                    
        _factory.put()
        self.redirect('/viewfactory?%s' % urllib.urlencode({'id': ID}))
        return
    
    '''
    Exception handler
    '''
    def handle_exception(self, exception, debug_mode):
        if debug_mode:
            super(StoreEditedFactoryPage, self).handle_exception(exception, debug_mode)
        else:
            template_values = bene_util.initTemplate(self.request.uri)
            path = os.path.join(os.path.dirname(__file__), 'not_found.html')
            self.response.out.write(template.render(path, template_values))
            return
        