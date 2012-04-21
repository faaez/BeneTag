from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template 
import bene_util
import entities
import os
import urllib



"""
Form to create a Badge
"""
class CreateBadgePage(webapp.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if not user: # need to signin first
            self.redirect('/?signin=True')
            return
            
        if not users.is_current_user_admin(): # need to be admin to create badge
            self.redirect('/')
            return
            
        # display form to create badge
        template_values = bene_util.urldecode(self.request.uri)
        path = os.path.join(os.path.dirname(__file__), 'createbadge.html')
        self.response.out.write(template.render(path, template_values))
        return
    
    '''
    Exception handler
    '''
    def handle_exception(self, exception, debug_mode):
        if debug_mode:
            super(CreateBadgePage, self).handle_exception(exception, debug_mode)
        else:
            template_values = {}
            path = os.path.join(os.path.dirname(__file__), 'not_found.html')
            self.response.out.write(template.render(path, template_values))
            return
            

"""
Page that stores badge in datastore
"""
class StoreBadgePage(webapp.RequestHandler):
    def post(self):
        user = users.get_current_user()
        if not user: # need to signin first
            self.redirect('/?signin=True')
            return
        
        if not users.is_current_user_admin(): # need to be admin to create badge
            self.redirect('/')
            return
        
        # otherwise create badge
        _name = self.request.get('name')
        _description = self.request.get('description')
        _picture = self.request.get('picture')
                    
        b = entities.Badge(name=_name, description=_description)
        b.addPicture(_picture)
                    
        # add if doesn't already exist
        if bene_util.doesBadgeExist(b):
            self.redirect('/createbadge?%s' % urllib.urlencode({'repeat': True}))
            return 
        
        b.put()
        if self.request.get('more'): # want to add more
            self.redirect('/createbadge?%s' % urllib.urlencode({'added': True}))
            return
        
        # otherwise redirect to badge page
        self.redirect('/viewbadge?%s' % urllib.urlencode({'id' : b.key()}))
        return
            
            
    '''
    Exception handler
    '''
    def handle_exception(self, exception, debug_mode):
        if debug_mode:
            super(StoreBadgePage, self).handle_exception(exception, debug_mode)
        else:
            template_values = {}
            path = os.path.join(os.path.dirname(__file__), 'not_found.html')
            self.response.out.write(template.render(path, template_values))
            return
