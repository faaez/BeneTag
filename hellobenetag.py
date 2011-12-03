from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

import create_product, view_product

application = webapp.WSGIApplication([
  ('/product', create_product.CreateProductPage),
  ('/storeProduct', create_product.StoreProductPage),
  ('/view', view_product.ViewProduct),
], debug=True)

def main():
  run_wsgi_app(application)

if __name__ == '__main__':
  main()
