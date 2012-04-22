from google.appengine.api import users
from google.appengine.ext import db, webapp
from google.appengine.ext.webapp import template
import bene_query
import bene_util
import os
import urllib



"""
Creates a form to create a Worker
"""
class EditWorkerPage(webapp.RequestHandler):
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
            TODO: If no ID sent, default to ?
            '''
            self.redirect('/')
            return
        _worker = db.get(ID)
        if not _worker: # doesn't exist
            template_values = {}
            path = os.path.join(os.path.dirname(__file__), 'not_found.html')
            self.response.out.write(template.render(path, template_values))
            return
        
        if _worker.owner != user: # not 'owner' of worker. I know it sounds very pre-emancipation
            self.redirect('/producerhome?%s' % urllib.urlencode({'not_owner': True}))
            return
        
        template_values = bene_util.urldecode(self.request.uri)
        template_values['name_old'] = _worker.name
        template_values['profile_old'] = _worker.profile
        template_values['unique_old'] = _worker.unique
                        
        _factories_old = [_worker.getFactory()]
        template_values['factories_old'] = _factories_old
        template_values['factories'] = []
        '''
        TODO: Make this more efficient. For some reason, 'factory not in _factories_old' doesn't work
        '''
        for factory in _producer.getFactories(): 
            add = True
            for factory_old in _factories_old:
                if factory_old.key() == factory.key():
                    add = False
            if add:
                template_values['factories'].append(factory)
                                            
        path = os.path.join(os.path.dirname(__file__), 'editworker.html')
        self.response.out.write(template.render(path, template_values))
        return
    
    '''
    Exception handler
    '''
    def handle_exception(self, exception, debug_mode):
        if debug_mode:
            super(EditWorkerPage, self).handle_exception(exception, debug_mode)
        else:
            template_values = {}
            path = os.path.join(os.path.dirname(__file__), 'not_found.html')
            self.response.out.write(template.render(path, template_values))
            return
                   
                   
"""
Puts a worker in the database
"""
class StoreEditedWorkerPage(webapp.RequestHandler):
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
            TODO: If no ID sent, default to ?
            '''
            self.redirect('/')
            return
        _worker = db.get(ID)
        if not _worker: # doesn't exist
            template_values = {}
            path = os.path.join(os.path.dirname(__file__), 'not_found.html')
            self.response.out.write(template.render(path, template_values))
            return
        
        if _worker.owner != user: # not 'owner' of worker. I know it sounds very pre-emancipation
            self.redirect('/producerhome?%s' % urllib.urlencode({'not_owner': True}))
            return
                            
        _worker.name = self.request.get('name')
        _worker.profile = self.request.get('profile')
        _unique_save = _worker.unique
        _worker.unique = self.request.get('unique')
        if bene_util.doesWorkerExist(_worker) and _unique_save != _worker.unique: # if worker already exists
            self.redirect('/editworker?%s' % (urllib.urlencode({'id' : ID, 'repeatedit' : True})))
            return

        _factory = self.request.get('factory')
        if _factory:
            _worker.factory = db.get(_factory)
                        
        _picture = self.request.get('picture')
        _worker.addPicture(_picture)
                
        _worker.put()
        self.redirect('/viewworker?%s' % urllib.urlencode({'id': ID}))
        return
    
    '''
    Exception handler
    '''
    def handle_exception(self, exception, debug_mode):
        if debug_mode:
            super(StoreEditedWorkerPage, self).handle_exception(exception, debug_mode)
        else:
            template_values = {}
            path = os.path.join(os.path.dirname(__file__), 'not_found.html')
            self.response.out.write(template.render(path, template_values))
            return  
        
        