from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

import create_product, view_product

application = webapp.WSGIApplication([
<<<<<<< HEAD
  ('/product', create_product.CreateProductPage),
  ('/storeProduct', create_product.StoreProductPage),
  ('/view', view_product.ViewProduct),
=======
  ('/createproduct', create_product.CreateProductPage),
  ('/storeproduct', create_product.StoreProductPage)
>>>>>>> master
], debug=True)

def main():
  run_wsgi_app(application)

if __name__ == '__main__':
  main()
