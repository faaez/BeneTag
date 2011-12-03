from google.appengine.ext import db

"""
Data type representing a product with a BeneTag
"""
class Product(db.Model):
    id = db.StringProperty(required=True)
    name = db.StringProperty(required=True)
    producerName = db.StringProperty()
    locationMade = db.GeoPtProperty()
    badgeName = db.StringProperty()

"""
Data type representing a producer
"""
class Producer(db.Model):
    name = db.StringProperty(required=True)

"""
Data type representing a badge
"""
class Badge(db.Model):
    name = db.StringProperty(required=True)
    iconUrl = db.StringProperty()
    description = db.StringProperty() 
