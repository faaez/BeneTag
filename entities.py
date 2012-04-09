from google.appengine.ext import db

"""
Data type representing a producer
"""
class Producer(db.Model):
    #profile information
    name = db.StringProperty(required=True)
    email = db.StringProperty(required=True)
    owner = db.UserProperty(required=True)
    description = db.TextProperty()
    verified = db.BooleanProperty()
    logo = db.BlobProperty()
       
    #hierarchical information    
    def factories(self):
        return Factory.all().filter('producer =', self)
    def workers(self):
        return Worker.all().filter('producer =', self)
 
"""
Data type representing a factory
"""
class Factory(db.Model):
    #profile information
    name = db.StringProperty(required=True)
    address = db.PostalAddressProperty()
    location = db.GeoPtProperty()
    
    #hierarchical information
    producer = db.ReferenceProperty(Producer,required=True)
    def workers(self):
        return Worker.all().filter('factory =', self)
    
"""
Data type representing a worker
"""
class Worker(db.Model):
    # profile information
    name = db.StringProperty(required=True)
    profile = db.TextProperty()
    picture = db.BlobProperty()
    
    # hierarchical information
    producer = db.ReferenceProperty(Producer,required=True)
    factory = db.ReferenceProperty(Factory,required=True)

"""
Data type representing a product with a BeneTag
"""
class Product(db.Model):
    name = db.StringProperty(required=True)
    picture = db.BlobProperty()
    
    # hierarchical information
    producer = db.ReferenceProperty(Producer)
    factory = db.ReferenceProperty(Factory)
    badges = db.ListProperty(db.Key)
    rating = db.FloatProperty()

"""
Data type representing a badge
"""
class Badge(db.Model):
    name = db.StringProperty(required=True)
    icon = db.BlobProperty()
    description = db.StringProperty() 
