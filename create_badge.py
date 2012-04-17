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
            if bene_util.getCurrentProducer() == None: # if producer page doesn't exist, need to create one
                self.redirect('/signup?%s' % urllib.urlencode({'redirect': 'createbadge', 'msg': True}))
            else:
                template_values = bene_util.decodeURL(self.request.uri)
                path = os.path.join(os.path.dirname(__file__), 'createbadge.html')
                self.response.out.write(template.render(path, template_values))
        else:
            self.redirect(users.create_login_url(self.request.uri))

"""
Page that stores Product in datastore
"""
class StoreBadgePage(webapp.RequestHandler):
    def post(self):
        user = users.get_current_user()
        if user: # if user has signed in
            if bene_util.getCurrentProducer() == None: # if producer page doesn't exist, need to create one
                self.redirect('/signup?%s' % urllib.urlencode({'redirect': 'storebadge', 'msg': True}))
            else: # if producer page does exist
                if users.is_current_user_admin(): # if admin, then add badge
                    _name = self.request.get('name')
                    _description = self.request.get('description')
                    _icon = self.request.get('icon')
                    if isinstance(_icon, unicode):
                        _icon = _icon.encode('utf-8', 'replace')
                    self.response.out.write("<html><body>2: %s: %s</body></html>" % (str(_icon), sys.getsizeof(_icon)))
                    return
                    
        
                    b = entities.Badge(name=_name, description=_description)
                    b.icon = db.Blob(_icon[0])
                    self.response.out.write("<html><body>2: %s: %s</body></html>" % (str(b.icon), sys.getsizeof(b.icon)))
                    return
                    
                    if bene_util.doesBadgeExist(b) == False: 
                        b.put()
                        self.redirect('/createbadge?%s' % urllib.urlencode({'added': True}))
                    else:
                        self.redirect('/createbadge?%s' % urllib.urlencode({'repeat': True}))
                    
                else: # otherwise, don't add badge
                    greeting = "You need admin privileges to create a badge"
                    self.response.out.write("<html><body>%s</body></html>" % greeting)
                    '''
                    TODO: Redirect to home
                    '''
        else: # otherwise, needs to sign in 
            self.redirect(users.create_login_url(self.request.uri))
            
