from google.appengine.ext import db

"""
Data type representing a product with a BeneTag
"""
class Product(db.Model):
    name = db.StringProperty(required=True)
    picture = db.BlobProperty()
    producerName = db.StringProperty()
    factoryMade = db.ReferenceProperty()
    badges = db.ListProperty(db.Key)

"""
Data type representing a producer
"""
class Producer(db.Model):
	factories = db.ListProperty(db.Key)
    name = db.StringProperty(required=True)
	profileOwner = db.UserProperty(required=True)

"""
Data type representing a factory
"""
class Factory(db.Model)
	producers = db.ListProperty(db.Key)
	workers = db.ListProperty(db.Key)
	name = db.StringProperty(required=True)
	address = db.PostalAddressProperty()
	location = db.GeoPtProperty()

"""
Data type representing a worker
"""
class Worker(db.Model)
	name = db.StringProperty()
	factory = db.ReferenceProperty()
	profile = db.TextProperty()
	picture = db.BlobProperty()

"""
Data type representing a badge
"""
class Badge(db.Model):
    name = db.StringProperty(required=True)
    iconUrl = db.StringProperty()
    description = db.StringProperty() 
