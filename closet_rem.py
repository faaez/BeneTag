from google.appengine.api import users
from google.appengine.ext import db, webapp
from google.appengine.ext.webapp import template
import bene_query
import os
import urllib


"""
Add to current consumer closet
"""
class RemFromCloset(webapp.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if not user: # not signed in
            self.redirect('/?%s' % urllib.urlencode({'signin': True}))
            return
        if bene_query.getCurrentUser().isProducer: # producers don't have closets
            self.redirect('/')
            return
        _consumer = bene_query.getCurrentConsumer()
        if _consumer == None: # if consumer page doesn't exist, need to create one
            self.redirect('/createconsumer?%s' % urllib.urlencode({'msg': True}))
            return
        ID = self.request.get('id')
        if not ID: # if no ID sent, show entire closet
            '''
            TODO: If no ID sent, default to viewcloset
            '''
            self.redirect('/')
            return
        product = db.get(ID)
        if not product: # product not found
            template_values = {}
            path = os.path.join(os.path.dirname(__file__), 'not_found.html')
            self.response.out.write(template.render(path, template_values))
            return
        
        # if in closet, remove from closet and redirect to product page
        if _consumer.hasProduct(product.key()):
            _consumer.remProduct(product.key())
            _consumer.put()
        self.redirect('/mobilepage?%s' % urllib.urlencode({'id': product.key()}))  
        return
    
    '''
    Exception handler
    '''
    def handle_exception(self, exception, debug_mode):
        if debug_mode:
            super(RemFromCloset, self).handle_exception(exception, debug_mode)
        else:
            template_values = {}
            path = os.path.join(os.path.dirname(__file__), 'not_found.html')
            self.response.out.write(template.render(path, template_values))
            return