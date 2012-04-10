from google.appengine.api import users
import entities

#---------------------------------
#---------- PRODUCER -------------
#---------------------------------

"""
Get the current producer entity
"""
def getCurrentProducer():
    ''' Get the current producer entity '''
    user = users.get_current_user()
    producers = entities.Producer.all().filter('email =', user.nickname())
    for producer in producers: 
        return producer
    return None

""" 
Does a similar producer already exist?
"""
def doesSimilarProducerExist(producer_add):
    ''' Does a similar producer already exist? Use to warn the user. '''
    producers = entities.Producer.all().filter('name =', producer_add.name)
    for producer in producers:
        if producer != None:
            return True
    return False   

#---------------------------------
#---------- FACTORY  -------------
#---------------------------------

"""
Does the factory already exist under the current producer? 
"""
def doesExactFactoryExist(factory_add):
    ''' DON'T USE THIS. Use doesFactoryExist() '''
    if factory_add.unique == None: return False
    producer = getCurrentProducer()
    if producer:
        factories = producer.factories().filter('unique = ', factory_add.unique)
        for factory in factories:
            if factory != None: return True
    return False

"""
Does a similar factory already exist under the current producer?
"""
def doesSimilarFactoryExist(factory_add):
    ''' DON'T USE THIS. Use doesFactoryExist() '''
    producer = getCurrentProducer()
    if producer:
        factories = producer.factories().filter('name = ', factory_add.name)
        for factory in factories:
            if factory != None: return True
        factories = producer.factories().filter('address = ', factory_add.address)
        for factory in factories:
            if factory != None: return True
    return False

"""
Does the factory exist under the current producer? 
"""
def doesFactoryExist(factory_add):
    ''' Does the factory exist under the current producer? Use to warn user. '''
    return doesExactFactoryExist(factory_add) or doesSimilarFactoryExist(factory_add)

#---------------------------------
#---------- BADGES ---------------
#---------------------------------

"""
Does the badge already exist?
"""
def doesBadgeExist(badge_add):
    ''' Does the badge already exist? '''
    # checks for same badge name
    badges = entities.Badge.all().filter('name =', badge_add.name)
    for badge in badges:
        if badge != None: return True    
    return False

#---------------------------------
#---------- WORKER ---------------
#---------------------------------

"""
Does the exact worker already exist under the current producer?
"""
def doesExactWorkerExist(worker_add):
    ''' DON'T USE THIS. Use doesWorkerExist() '''
    if worker_add.unique == None: return False
    producer = getCurrentProducer()
    if producer:
        workers = producer.workers().filter('unique =', worker_add.unique)
        for worker in workers:
            if worker != None: return True
    return False

"""
Does a similar worker already exist under the current producer?
"""
def doesSimilarWorkerExist(worker_add):
    ''' DON'T USE THIS. Use doesWorkerExist() '''
    # checks for same woif factory_add.unique == None: return Falserker name AND factory
    producer = getCurrentProducer()
    if producer:
        workers = producer.workers().filter('name =', worker_add.name).filter('factory =', worker_add.factory)
        for worker in workers:
            if worker != None: return True    
    return False

""" 
Does the worker exist under the current producer?
"""
def doesWorkerExist(worker_add):
    ''' Does the worker exist under the current producer? Use to warn user. ''' 
    return doesExactWorkerExist(worker_add) or doesSimilarWorkerExist(worker_add)

#---------------------------------
#---------- PRODUCT --------------
#---------------------------------

"""
Does the exact product already exist under the current producer?
"""
def doesExactProductExist(product_add):
    ''' DON'T USE THIS. Use doesProductExist() '''
    if product_add.unique == None: return False
    producer = getCurrentProducer()
    if producer:
        products = producer.products().filter('unique =', product_add.unique)
        for product in products:
            if product != None: return True
    return False   

"""
Does a similar product already exist?
"""
def doesSimilarProductExist(product_add):
    ''' DON'T USE THIS. Use doesProductExist() '''
    # checks for same product name AND same factory
    producer = getCurrentProducer()
    if producer:
        products = getCurrentProducer().products().filter('name =', product_add.name).filter('factory =', product_add.factory)
        for product in products:
            if product != None: return True    
    return False

""" 
Does the product already exist under the current producer?
"""
def doesProductExist(product_add):
    '''Does the product already exist under the current producer? Use to warn user.'''
    return doesExactProductExist(product_add) or doesSimilarProductExist(product_add)


#---------------------------------
#-------------- MISC -------------
#---------------------------------

"""
Decode a url into a dictionary of arguments
Assumption: Only one value per argument
"""
def decodeURL(url):
    ''' Decode a url into a dictionary of arguments. Assumption: Only one value per argument '''
    queries = url.split('?') 
    dictionary = {} 
    for query in queries:
        args = query.split('&') 
        for arg in args: 
            if '=' in arg: 
                key,val = arg.split('=') 
                dictionary[key] = val
    return dictionary