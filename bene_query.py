from google.appengine.api import users
import entities

"""
Get the current User entity
"""
def getCurrentUser():
    ''' Get the current producer entity '''
    _user = users.get_current_user()
    _users = entities.User.all().filter('owner =', _user)
    for user in _users: 
        return user
    return None

"""
Get the current Consumer entity
"""
def getCurrentConsumer():
    ''' Get the current producer entity '''
    user = users.get_current_user()
    consumers = entities.Consumer.all().filter('owner =', user)
    for consumer in consumers: 
        return consumer
    return None

"""
Get the current Producer entity
"""
def getCurrentProducer():
    ''' Get the current producer entity '''
    user = users.get_current_user()
    producers = entities.Producer.all().filter('owner =', user)
    for producer in producers: 
        return producer
    return None