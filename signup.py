from google.appengine.api import users
from google.appengine.ext import db, webapp
from google.appengine.ext.webapp import template
import entities
import os
import bene_util


class Signup(webapp.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if user: # signed in
            if not bene_util.getCurrentUser(): # no user exists
                producer = self.request.get('producer')
                consumer = self.request.get('consumer')
                if producer and not consumer: # make person a producer only in most restricted case
                    u = entities.User(email=user.nickname(),
                                      owner=user,
                                      isConsumer=False,
                                      isProducer=True)
                    u.put()
                    self.redirect('/createproducer')
                    return
                else: # all other cases, make consumer
                    u = entities.User(email=user.nickname(),
                                      owner=user,
                                      isConsumer=True,
                                      isProducer=False)
                    u.put()
                    self.redirect('/createconsumer')
                    return
                
            
            if bene_util.getCurrentUser().isProducer: # signed in producer
                if bene_util.getCurrentProducer() == None: # no producer page, so create one 
                    self.redirect('/createproducer')
                    return
                else: # already has producer page, so redirect
                    self.redirect('/producerhome')
                    return
            else: # signed in consumer
                if bene_util.getCurrentConsumer() == None: # no consumer page, so create on
                    self.redirect('/createconsumer')
                    return
                else: # already has consumer page, so redirect
                    self.redirect('/consumerhome')
                    return
        else: # need to sign in
            self.redirect(users.create_login_url(self.request.uri))
            return

