from google.appengine.ext import db

"""
Data type representing a user
"""
class User(db.Model):
    email = db.StringProperty()
    isProducer = db.BooleanProperty()
    isConsumer = db.BooleanProperty()
    owner = db.UserProperty()

"""
Data type representing a consumer
"""
class Consumer(db.Model):
    #profile information
    name = db.StringProperty()
    email = db.StringProperty()
    profile = db.TextProperty()
    picture = db.BlobProperty()

    #security
    owner = db.UserProperty()
    verified = db.BooleanProperty()
    
    #closet
    _products = db.ListProperty(db.Key)
    
    def addProduct(self, key):
        self._products.append(key) 
        return
    def remProduct(self, key):
        self._products.remove(key)
        return
    def products(self):
        if self._products:
            __products = db.get(self._products)
            return [product for product in __products if product] # return non-None products
        else:
            return None
    def hasProduct(self, key):
        return key in self._products

"""
Data type representing a producer
"""
class Producer(db.Model):
    #profile information
    name = db.StringProperty(required=True)
    email = db.StringProperty(required=True)
    description = db.TextProperty()
    logo = db.BlobProperty()
    
    #security
    owner = db.UserProperty()
    verified = db.BooleanProperty()
       
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
    picture = db.BlobProperty()
    
    #security
    owner = db.UserProperty()
    
    #producer-defined identifier (only for producer)
    unique = db.StringProperty()
#    def unique(self):
#        '''
#        Use this if you want to know any unique id for the entity. 
#        A possible use of this would be if you want to get input from user about a specific factory, 
#        and you want to uniquely identify it somehow
#        '''
#        if self.unique == None: return self.id
#        return self.unique 
    
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
    
    #producer-defined identifier (only for producer)
    unique = db.StringProperty()
#    def unique(self):
#        '''
#        Use this if you want to know any unique id for the entity. 
#        A possible use of this would be if you want to get input from user about a specific worker, 
#        and you want to uniquely identify it somehow
#        '''
#        if self.unique == None: return self.id
#        return self.unique
    
    # hierarchical information
    producer = db.ReferenceProperty(Producer)
    factory = db.ReferenceProperty(Factory)
    ''' don't use products, use function products() instead '''
    _products = db.ListProperty(db.Key)
    def addProduct(self, key):
        self._products.append(key) 
    def remProduct(self, key):
        self._products.remove(key) 
    def products(self):
        if self._products:
            __products = db.get(self._products)
            return [product for product in __products if product] # return non-None products
        else:
            return None
        ''' 
        None products appear if a certain product was created by the worker, but was then deleted from
        datastore manually
        '''

"""
Data type representing a product with a BeneTag
"""
class Product(db.Model):
    # profile information
    name = db.StringProperty()
    picture = db.BlobProperty()
    
    # security
    owner = db.UserProperty()
    
    #producer-defined identifier (only for producer)
    unique = db.StringProperty()
#    def unique(self): 
#        '''
#        Use this if you want to know any unique id for the entity. 
#        A possible use of this would be if you want to get input from user about a specific product, 
#        and you want to uniquely identify it somehow
#        ''' 
#        if self.unique == None: return self.id
#        return self.unique
    
    # hierarchical information
    producer = db.ReferenceProperty(Producer)
    factory = db.ReferenceProperty(Factory)
    badges = db.ListProperty(db.Key)
    rating = db.FloatProperty()
    def workers(self):
        return Worker.all().filter('_products =', self)

"""
Data type representing a badge
"""
class Badge(db.Model):
    name = db.StringProperty()
    icon = db.BlobProperty()
    description = db.StringProperty() 
    
    # hierarchical information
    def products(self):
        return Product.all().filter('badges =', self)
