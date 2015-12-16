import cgi
import os
import urllib
import datetime

from google.appengine.api import users
from google.appengine.ext import ndb
from google.appengine.ext.db import Query
import jinja2
import webapp2

import login
import sessions_datastore
import reservations_datastore



JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)
    
    
    
class ErrorPageHandler(webapp2.RequestHandler):
  def get(self):
  	params = self.request.params
  	context = { }
  	
  	"""Generate log in/out information"""
  	context = login.generateLogInOutContextInfo(self, context)
    
  	contents = JINJA_ENVIRONMENT.get_template('error.html').render(context)
  	self.response.write(contents)
  	
  	
  	
  def post(self):
  	params = self.request.params;
	self.get();
	
	
  	
app = webapp2.WSGIApplication([
    ('/.*', ErrorPageHandler)
], debug = True)
