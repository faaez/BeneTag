from google.appengine.api import users
from google.appengine.ext import db, webapp
from google.appengine.ext.webapp import template
import bene_util
import os
import urllib


"""
Add to current consumer closet
"""
class RemFromCloset(webapp.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if not user: # not signed in
            self.redirect('/?signin=True')
            return
        if bene_util.getCurrentUser().isProducer: # producers don't have closets
            self.redirect('/')
            return
        _consumer = bene_util.getCurrentConsumer()
        if _consumer == None: # if consumer page doesn't exist, need to create one
            self.redirect('/createconsumer')
            return
        ID = self.request.get('id')
        if not ID:
            '''
            TODO: If no ID sent, default to ?
            '''
            self.redirect('/')
            return
        product = db.get(ID)
        if not product:
            '''
            TODO: if no id is sent, defaults to page with all factories?
            '''
            #factorylist = entities.Factory.all()
            template_values = {}
            path = os.path.join(os.path.dirname(__file__), 'not_found.html')
            self.response.out.write(template.render(path, template_values))
            return
        if _consumer.hasProduct(product.key()):
            _consumer.remProduct(product.key())
        self.redirect('/mobilepage?%s' % urllib.urlencode({'id': product.key()}))  
        return