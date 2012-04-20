from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
import about
import consumer_home
import create_badge
import create_consumer
import create_factory
import create_producer
import create_product
import create_qr
import create_worker
import edit_factory
import edit_producer
import edit_product
import edit_worker
import home
import mobile_page
import producer_home
import search_product
import signup
import view_factory
import view_producer
import view_product
import view_productworkers
import view_worker


application = webapp.WSGIApplication([
  ('/', home.HomePage),
  ('/signup', signup.Signup), 
  ('/producerhome', producer_home.HomePage),
  ('/consumerhome', consumer_home.HomePage), 
  ('/about', about.AboutPage),
  # create and edit producer page
  ('/createproducer', create_producer.CreateProducerPage),
  ('/storeproducer', create_producer.StoreProducerPage),
  ('/editproducer', edit_producer.EditProducerPage),
  ('/storeeditedproducer', edit_producer.StoreEditedProducerPage),
  ('/viewproducer', view_producer.ViewProducer),
  # create and edit consumer page
  ('/createconsumer', create_consumer.CreateConsumerPage),
  ('/storeconsumer', create_consumer.StoreConsumerPage),
  # create and edit product
  ('/createproduct', create_product.CreateProductPage),
  ('/storeproduct', create_product.StoreProductPage),
  ('/editproduct', edit_product.EditProductPage),
  ('/storeeditedproduct', edit_product.StoreEditedProductPage),
  # create and edit factory
  ('/createfactory', create_factory.CreateFactoryPage),
  ('/storefactory', create_factory.StoreFactoryPage),
  ('/editfactory', edit_factory.EditFactoryPage),
  ('/storeeditedfactory', edit_factory.StoreEditedFactoryPage),
  ('/viewfactory', view_factory.ViewFactory),
  # create and edit worker
  ('/createworker', create_worker.CreateWorkerPage),
  ('/storeworker', create_worker.StoreWorkerPage),
  ('/editworker', edit_worker.EditWorkerPage),
  ('/storeeditedworker', edit_worker.StoreEditedWorkerPage),
  ('/viewworker', view_worker.ViewWorker),
  
  # create badge
  ('/createbadge', create_badge.CreateBadgePage),
  ('/storebadge', create_badge.StoreBadgePage),
  
  ('/view', view_product.ViewProduct),
  ('/viewproductworkers', view_productworkers.ViewProductWorkers),
  ('/productimage', view_product.ProductImage),
  ('/badgeimage', mobile_page.BadgeImage),                          
  ('/mobilepage', mobile_page.ViewProduct),
  ('/qr', create_qr.CreateQrPage),
  
  ('/searchproduct', search_product.CreateProductSearchPage),
  ('/productsearchresult', search_product.SearchResultPage)
], debug=True)

def main():
    run_wsgi_app(application)

if __name__ == '__main__':
    main()
