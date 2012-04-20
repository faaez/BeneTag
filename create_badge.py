from google.appengine.api import users
from google.appengine.ext import webapp, db
from google.appengine.ext.webapp import template, blobstore_handlers
import bene_util
import entities
import os
import sys
import urllib



"""
Creates a form for Producers to enter information 
about a Badge
"""
class CreateBadgePage(webapp.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if user:
            if not users.is_current_user_admin():
                self.redirect('/')
                return
            template_values = bene_util.decodeURL(self.request.uri)
            path = os.path.join(os.path.dirname(__file__), 'createbadge.html')
            self.response.out.write(template.render(path, template_values))
            return
        else:
            self.redirect('/?signin=True')
            return

"""
Page that stores badge in datastore
"""
class StoreBadgePage(webapp.RequestHandler):
    def post(self):
        user = users.get_current_user()
        if user: # if user has signed in
            if not users.is_current_user_admin():
                self.redirect('/')
                return
            _name = self.request.get('name')
            _description = self.request.get('description')
            _icon = self.request.POST["icon"]
                    
            b = entities.Badge(name=_name, description=_description)
                    
            if _icon:
                if isinstance(_icon,unicode):
                    _icon = _icon.encode('utf-8', 'replace')
                b.icon = db.Blob(_icon.value)
            
            if bene_util.doesBadgeExist(b) == False: 
                b.put()
                self.redirect('/createbadge?%s' % urllib.urlencode({'added': True}))
            else:
                self.redirect('/createbadge?%s' % urllib.urlencode({'repeat': True}))
                    
        else: # otherwise, needs to sign in 
            self.redirect('/?signin=True')
            
