from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

import home
import about
import signup
import create_product
import create_badge
import view_product 
import create_qr
import create_factory
import view_factory
import search_product
import create_worker
import mobile_page

application = webapp.WSGIApplication([
  ('/', home.HomePage),
  ('/about', about.AboutPage),
  ('/signup', signup.CreateProducerPage),
  ('/storeproducer', signup.StoreProducerPage),
  ('/createproduct', create_product.CreateProductPage),
  ('/storeproduct', create_product.StoreProductPage),
  ('/createfactory', create_factory.CreateFactoryPage),
  ('/storefactory', create_factory.StoreFactoryPage),
  ('/createbadge', create_badge.CreateBadgePage),
  ('/storebadge', create_badge.StoreBadgePage),
  ('/createworker', create_worker.CreateWorkerPage),
  ('/storeworker', create_worker.StoreWorkerPage),
  ('/view', view_product.ViewProduct),
  ('/productimage', view_product.ProductImage),
  ('/badgeimage', mobile_page.BadgeImage),                          
  ('/mobilepage', mobile_page.ViewProduct),
  ('/qr', create_qr.CreateQrPage),
  ('/viewfactory', view_factory.ViewFactory),
  ('/searchproduct', search_product.CreateProductSearchPage),
  ('/productsearchresult', search_product.SearchResultPage)
], debug=True)

def main():
  run_wsgi_app(application)

if __name__ == '__main__':
  main()
