import os

from google.appengine.ext import db
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template

import entities
import urllib
import urllib2

class CreateQrPage(webapp.RequestHandler):
    def get(self):
        curUrl = self.request.url
        curUrl = curUrl.replace('qr','view')
        curUrl = urllib.pathname2url(curUrl)
        url = "http://chart.apis.google.com/chart?cht=qr&chs=150x150&chl=%s&chId=HI0" % (curUrl)
        self.redirect(url)

