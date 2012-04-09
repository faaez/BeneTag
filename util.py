from google.appengine.api import users
from google.appengine.ext import db, webapp
import entities
import urllib


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
def doesFactoryExist(factory_add):
    if getCurrentProducer().factories():
        factories = getCurrentProducer().factories().filter('name = ', factory_add.name).fetch(1)
        for factory in factories:
            if factory != None: return True
        factories = getCurrentProducer().factories().filter('address = ', factory_add.address).fetch(1)
        for factory in factories:
            if factory != None: return True
    return False

"""
Decode a url into a dictionary of arguments
Assumption: Only one value per argument
"""
def decodeURL(url):
    queries = url.split('?') 
    dictionary = {} 
    for query in queries:
        args = query.split('&') 
        for arg in args: 
            if '=' in arg: 
                key,val = arg.split('=') 
                dictionary[key] = [val] 
    return dictionary