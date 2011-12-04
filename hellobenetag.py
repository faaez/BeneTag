from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

import home
import create_product
import create_badge
import view_product 
import create_qr
import create_factory
import view_factory
import search_product

application = webapp.WSGIApplication([
  ('/', home.HomePage),
  ('/createproduct', create_product.CreateProductPage),
  ('/storeproduct', create_product.StoreProductPage),
  ('/createfactory', create_factory.CreateFactoryPage),
  ('/storefactory', create_factory.StoreFactoryPage),
  ('/createbadge', create_badge.CreateBadgePage),
  ('/storebadge', create_badge.StoreBadgePage),
  ('/view', view_product.ViewProduct),
  ('/productimage', view_product.ProductImage),
  ('/qr', create_qr.CreateQrPage),
  ('/viewfactory', view_factory.ViewFactory),
  ('/searchproduct', search_product.CreateProductSearchPage),
  ('/productsearchresult', search_product.SearchResultPage)
], debug=True)

def main():
  run_wsgi_app(application)

if __name__ == '__main__':
  main()
