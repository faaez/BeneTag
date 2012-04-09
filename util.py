from google.appengine.api import users, users
from google.appengine.ext import db, webapp
import entities


"""
Get the current producer entity
"""
def getCurrentProducer():
    user = users.get_current_user()
    producers = entities.Producer.all().filter('email =', user.nickname()).fetch(1)
    for producer in producers: 
        return producer
    return None

"""
Does the factory already exist under the current producer?
"""
def doesFactoryExist(factory):
    factories = getCurrentProducer().factories().filter('name like ', factory.name).filter('location like ', factory.location).fetch(1)
    if factories == None: return True
    return False