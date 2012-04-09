from google.appengine.api import users
from google.appengine.ext import db, webapp
from google.appengine.ext.webapp import template
import entities
import bene_util
import os



"""
Creates a form for Producers to enter information 
about a Product
"""
class CreateProductPage(webapp.RequestHandler):
    def get(self):
        user = users.get_current_user()

        factory_names = []
        factories = entities.Factory.all()
        for factory in factories:
            factory_names.append(factory.name)
        template_values = {
            'producerName': bene_util.getCurrentProducer().name,
            'badges' : entities.Badge.all(),
            'factory_names' : factory_names
        }
        path = os.path.join(os.path.dirname(__file__), 'createproduct.html')
        self.response.out.write(template.render(path, template_values))
      
"""
Page that stores Product in datastore
"""
class StoreProductPage(webapp.RequestHandler):
    def post(self):
        user = users.get_current_user()
        if user:
            _name = self.request.get('name')
            _producer = entities.Producer.gql("WHERE name = :1", self.request.get('producerName')).get()
            _factoryName = self.request.get('factoryName')
            _badges = self.request.get_all('badges')
            _picture = self.request.get('picture')
            if isinstance(_picture, unicode):
                _picture = _picture.encode('utf-8', 'replace')
            _factoryMade = entities.Factory.gql("WHERE name = :1", _factoryName).get()
            

            p = entities.Product(name=_name, producer=_producer, factory=_factoryMade)
            for _badge in _badges:
                p.badges.append(db.Key(_badge))
            p.picture = db.Blob(_picture)
            self.response.out.write("<html><body>"+str(_badges)+"</html></body>")
            #p.put()
            #self.redirect('/mobilepage?id=' + str(p.key()))
        else:
            self.redirect(users.create_login_url(self.request.uri))
