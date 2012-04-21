from google.appengine.api import users
from google.appengine.ext import db, webapp
from google.appengine.ext.webapp import template
import bene_query
import os
import urllib


"""
Add to current consumer closet
"""
class AddToCloset(webapp.RequestHandler):
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
        if not ID:
            '''
            TODO: If no ID sent, default to viewcloset?
            '''
            self.redirect('/')
            return
        product = db.get(ID)
        if not product: # invalid product
            template_values = {}
            path = os.path.join(os.path.dirname(__file__), 'not_found.html')
            self.response.out.write(template.render(path, template_values))
            return
        
        # if not already in closet, add to closet, and redirect back to product page
        if not _consumer.hasProduct(product.key()): 
            _consumer.addProduct(product.key())
        self.redirect('/mobilepage?%s' % urllib.urlencode({'id': product.key()}))  
        return
    
    '''
    Exception handler
    '''
    def handle_exception(self, exception, debug_mode):
        if debug_mode:
            super(AddToCloset, self).handle_exception(exception, debug_mode)
        else:
            template_values = {}
            path = os.path.join(os.path.dirname(__file__), 'not_found.html')
            self.response.out.write(template.render(path, template_values))
            return
            