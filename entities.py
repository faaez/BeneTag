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
    
    _picture = db.BlobProperty()
    def addPicture(self, picture_add):
        if picture_add:
            ''' 
            TODO: check for mimetype here. if not jpg/png/gif/etc. then don't add?
            '''
            if isinstance(picture_add, unicode):
                self._picture = picture_add.encode('utf-8', 'replace')
            else:
                self._picture = picture_add
        
    #security
    owner = db.UserProperty()
    verified = db.BooleanProperty()
    
    #closet
    _products = db.ListProperty(db.Key)
    def addProduct(self, key):
        if key:
            self._products.append(key) 
    def remProduct(self, key):
        if key:
            self._products.remove(key)
    def getProducts(self):
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
    
    _picture = db.BlobProperty()
    def addPicture(self, picture_add):
        if picture_add:
            ''' 
            TODO: check for mimetype here
            '''
            if isinstance(picture_add, unicode):
                self._picture = picture_add.encode('utf-8', 'replace')
            else:
                self._picture = picture_add
    
    #security
    owner = db.UserProperty()
    verified = db.BooleanProperty()
       
    #hierarchical information    
    def getFactories(self):
        return self.factory_set
    def getWorkers(self):
        return self.worker_set
    def getProducts(self):
        return self.product_set
 
"""
Data type representing a factory
"""
class Factory(db.Model):
    #profile information
    name = db.StringProperty()
    address = db.PostalAddressProperty()
    location = db.GeoPtProperty()
    
    _picture = db.BlobProperty()
    def addPicture(self, picture_add):
        if picture_add:
            ''' 
            TODO: check for mimetype here
            '''
            if isinstance(picture_add, unicode):
                self._picture = picture_add.encode('utf-8', 'replace')
            else:
                self._picture = picture_add
    
    #security
    owner = db.UserProperty()
    unique = db.StringProperty()
    
    #hierarchical information
    _producer = db.ReferenceProperty(Producer)
    def getProducer(self):
        return self._producer
    def addProducer(self, producer_add):
        self._producer = producer_add
        
    def getWorkers(self):
        return self.worker_set
    def getProducts(self):
        return self.product_set
    
"""
Data type representing a worker
"""
class Worker(db.Model):
    # profile information
    name = db.StringProperty()
    profile = db.TextProperty()
    
    _picture = db.BlobProperty()
    def addPicture(self, picture_add):
        if picture_add:
            ''' 
            TODO: check for mimetype here
            '''
            if isinstance(picture_add, unicode):
                self._picture = picture_add.encode('utf-8', 'replace')
            else:
                self._picture = picture_add
    
    # security
    owner = db.UserProperty()
    unique = db.StringProperty()

    # hierarchical information
    _producer = db.ReferenceProperty(Producer)
    def getProducer(self):
        return self._producer
    def addProducer(self, producer_add):
        self._producer = producer_add
        
    _factory = db.ReferenceProperty(Factory)
    def getFactory(self):
        return self._factory
    def addFactory(self, factory_add):
        self._factory = factory_add
        
    _products = db.ListProperty(db.Key)
    def addProduct(self, key):
        if key:
            self._products.append(key) 
    def remProduct(self, key):
        if key:
            self._products.remove(key) 
    def getProducts(self):
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
    rating = db.FloatProperty()
    _picture = db.BlobProperty()
    def addPicture(self, picture_add):
        if picture_add:
            ''' 
            TODO: check for mimetype here
            '''
            if isinstance(picture_add, unicode):
                self._picture = picture_add.encode('utf-8', 'replace')
            else:
                self._picture = picture_add
    
    # security
    owner = db.UserProperty()
    unique = db.StringProperty()
    
    # hierarchical information
    _producer = db.ReferenceProperty(Producer)
    def getProducer(self):
        return self._producer
    def addProducer(self, producer_add):
        self._producer = producer_add
        
    _factory = db.ReferenceProperty(Factory)
    def getFactories(self):
        return [self._factory]
    def addFactory(self, factory_add):
        self._factory = factory_add
        
    _badges = db.ListProperty(db.Key)
    def addBadge(self, key):
        if key:
            self._badges.append(key) 
    def remBadge(self, key):
        if key:
            self._badges.remove(key) 
    def getBadges(self):
        if self._badges:
            __badges = db.get(self._badges)
            return [badge for badge in __badges if badge] # return non-None badges
        else:
            return None
    
    def getWorkers(self):
        return Worker.all().filter('_products =', self)

"""
Data type representing a badge
"""
class Badge(db.Model):
    name = db.StringProperty()
    description = db.StringProperty()
    
    _picture = db.BlobProperty()
    def addPicture(self, picture_add):
        if picture_add:
            ''' 
            TODO: check for mimetype here
            '''
            if isinstance(picture_add, unicode):
                self._picture = picture_add.encode('utf-8', 'replace')
            else:
                self._picture = picture_add 
    
    # hierarchical information
    def getProducts(self):
        return Product.all().filter('badges =', self)
