from google.appengine.ext import db

"""
Data type representing a producer
"""
class Producer(db.Model):
    #profile information
    name = db.StringProperty(required=True)
    email = db.StringProperty(required=True)
    description = db.TextProperty()
    verified = db.BooleanProperty()
    logo = db.BlobProperty()
    
    #security
    owner = db.UserProperty()
       
    #hierarchical information    
    def factories(self):
        return self.factory_set
    def workers(self):
        return self.worker_set
    def products(self):
        return self.product_set
 
"""
Data type representing a factory
"""
class Factory(db.Model):
    #profile information
    name = db.StringProperty()
    address = db.PostalAddressProperty()
    location = db.GeoPtProperty()
    
    #security
    owner = db.UserProperty()
    
    #hierarchical information
    producer = db.ReferenceProperty(Producer)
    def workers(self):
        return self.worker_set
    def products(self):
        return self.product_set
    
"""
Data type representing a worker
"""
class Worker(db.Model):
    # profile information
    name = db.StringProperty()
    profile = db.TextProperty()
    picture = db.BlobProperty()
    
    # security
    owner = db.UserProperty()
    
    # hierarchical information
    producer = db.ReferenceProperty(Producer)
    factory = db.ReferenceProperty(Factory)

"""
Data type representing a product with a BeneTag
"""
class Product(db.Model):
    # profile information
    name = db.StringProperty()
    picture = db.BlobProperty()
    
    # security
    owner = db.UserProperty()
    
    # hierarchical information
    producer = db.ReferenceProperty(Producer)
    factory = db.ReferenceProperty(Factory)
    badges = db.ListProperty(db.Key)
    rating = db.FloatProperty()

"""
Data type representing a badge
"""
class Badge(db.Model):
    name = db.StringProperty()
    icon = db.BlobProperty()
    description = db.StringProperty() 
