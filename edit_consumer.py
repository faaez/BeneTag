from google.appengine.api import users
from google.appengine.ext import db, webapp
from google.appengine.ext.webapp import template
import entities
import os
import bene_util



"""
Creates a form to edit Consumer
"""
class EditConsumerPage(webapp.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if user: # user signed in
            if bene_util.getCurrentUser().isProducer:
                self.redirect('/')
                return
            _consumer = bene_util.getCurrentConsumer();
            if _consumer == None: # no consumer page, so create one 
                self.redirect('/createconsumer')
                return
            else: # already has producer page, so edit
                template_values = bene_util.decodeURL(self.request.uri)
                template_values['name_old'] = _consumer.name
                template_values['profile_old'] = _consumer.profile
                #self.response.out.write('<html><body>%s</body></html>' % _consumer.profile)
                #return
                path = os.path.join(os.path.dirname(__file__), 'editconsumer.html')
                self.response.out.write(template.render(path, template_values))
                return
        else: # user not signed in
            self.redirect('/?signin=True')
            return

"""
Puts a Producer in the database
"""
class StoreEditedConsumerPage(webapp.RequestHandler):
    def post(self):
        user = users.get_current_user()
        if user:
            if bene_util.getCurrentUser().isProducer: # producer can't access consumer pages
                self.redirect('/')
                return
            _name = self.request.get('name')
            _profile = self.request.get('profile')
            _picture = self.request.get('picture')
            
            _consumer = bene_util.getCurrentConsumer()
        
            if _consumer == None: # no consumer page, so create one
                c = entities.Consumer(name = _name, 
                                    email=user.nickname(), 
                                    owner=user,
                                    profile=_profile,                      
                                    verified=False)
                if _picture:
                    if isinstance(_picture, unicode):
                        _picture = _picture.encode('utf-8', 'replace')
                    c.picture=db.Blob(_picture),
                c.put()
            else: # otherwise, edit                  
                _consumer.name = _name
                _consumer.profile = _profile
                if _picture:
                    if isinstance(_picture, unicode):
                        _picture = _picture.encode('utf-8', 'replace')
                    _consumer.picture=db.Blob(_picture),
                _consumer.put()
                        
            self.redirect('/'+self.request.get('redirect'))
            return
        else:
            self.redirect('/?signin=True')
            return
