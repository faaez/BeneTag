from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

import home
import create_product
import view_product 
import create_qr
import create_factory

application = webapp.WSGIApplication([
  ('/', home.HomePage),
  ('/createproduct', create_product.CreateProductPage),
  ('/storeproduct', create_product.StoreProductPage),
  ('/createfactory', create_factory.CreateFactoryPage),
  ('/storefactory', create_factory.StoreFactoryPage),
  ('/view', view_product.ViewProduct),
  ('/qr', create_qr.CreateQrPage)
], debug=True)

def main():
  run_wsgi_app(application)

if __name__ == '__main__':
  main()
