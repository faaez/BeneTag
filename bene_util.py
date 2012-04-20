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
    producers = entities.Producer.all().filter('owner =', user)
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
        if producer:
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
    if factory_add.unique:
        producer = getCurrentProducer()
        if producer:
            # if two have same unique ID
            factories = producer.factories().filter('unique = ', factory_add.unique)
            for factory in factories:
                if factory: return True
            # if other factory has no unique ID but same name
            factories = producer.factories().filter('name = ', factory_add.name)
            for factory in factories:
                if factory : 
                    if not factory.unique: return True
    return False

"""
Does a similar factory already exist under the current producer?
"""
def doesSimilarFactoryExist(factory_add):
    ''' DON'T USE THIS. Use doesFactoryExist() '''
    # checks for same factory name
    producer = getCurrentProducer()
    if producer:
        factories = producer.factories().filter('name = ', factory_add.name)
        for factory in factories:
            if factory : return True
    return False

"""
Does the factory exist under the current producer? 
"""
def doesFactoryExist(factory_add):
    ''' Does the factory exist under the current producer? Use to warn user. '''
    if factory_add.unique: # if no unique ID, then need factory name to be unique
        return doesExactFactoryExist(factory_add)
    return doesSimilarFactoryExist(factory_add) 

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
        if badge: return True    
    return False

#---------------------------------
#---------- WORKER ---------------
#---------------------------------

"""
Does the exact worker already exist under the current producer?
"""
def doesExactWorkerExist(worker_add):
    ''' DON'T USE THIS. Use doesWorkerExist() '''
    if worker_add.unique: 
        producer = getCurrentProducer()
        if producer:
            # if two workers have same unique ID
            workers = producer.workers().filter('unique =', worker_add.unique)
            for worker in workers:
                if worker: return True
            # if other worker has no unique ID but same name
            workers = producer.workers().filter('name =', worker_add.name)
            for worker in workers:
                if worker: 
                    if not worker.unique: return True   
    return False

"""
Does a similar worker already exist under the current producer?
"""
def doesSimilarWorkerExist(worker_add):
    ''' DON'T USE THIS. Use doesWorkerExist() '''
    # checks for same worker name
    producer = getCurrentProducer()
    if producer:
        workers = producer.workers().filter('name =', worker_add.name)
        for worker in workers:
            if worker: return True    
    return False

""" 
Does the worker exist under the current producer?
"""
def doesWorkerExist(worker_add):
    ''' Does the worker exist under the current producer? Use to warn user. ''' 
    if worker_add.unique: # if no unique ID, then need unique names in factory
        return doesExactWorkerExist(worker_add)
    return doesSimilarWorkerExist(worker_add) 

#---------------------------------
#---------- PRODUCT --------------
#---------------------------------

"""
Does the exact product already exist under the current producer?
"""
def doesExactProductExist(product_add):
    ''' DON'T USE THIS. Use doesProductExist() '''
    if product_add.unique:
        producer = getCurrentProducer()
        if producer:
            products = producer.products().filter('unique =', product_add.unique)
            for product in products:
                if product: return True
    return False   

"""
Does a similar product already exist?
"""
def doesSimilarProductExist(product_add):
    ''' DON'T USE THIS. Use doesProductExist() '''
    # checks for same product name 
    producer = getCurrentProducer()
    if producer:
        products = getCurrentProducer().products().filter('name =', product_add.name)
        for product in products:
            if product: return True    
    return False

""" 
Does the product already exist under the current producer?
"""
def doesProductExist(product_add):
    '''Does the product already exist under the current producer? Use to warn user.'''
    if product_add.unique: # if no unique ID, then need products to have different names
        return doesExactProductExist(product_add)
    return doesSimilarProductExist(product_add)
    # XXX: note that here we don't use doesSimilarProductExist() because lots of product units can be similar to each other.
    # However, doesSimilarProductExist() can be used to figure out repeated product lines (since lines should have unique names)


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