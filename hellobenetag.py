from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

import create_product, view_product

application = webapp.WSGIApplication([
<<<<<<< HEAD
  ('/product', create_product.CreateProductPage),
  ('/storeProduct', create_product.StoreProductPage),
  ('/view', view_product.ViewProduct),
<<<<<<< HEAD
=======
  ('/createproduct', create_product.CreateProductPage),
  ('/storeproduct', create_product.StoreProductPage)
>>>>>>> master
=======
>>>>>>> 1f7ce105e99bf0a51ae65207adfaaccf9104a5fa
], debug=True)

def main():
  run_wsgi_app(application)

if __name__ == '__main__':
  main()
