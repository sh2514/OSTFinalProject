import cgi
import os
import urllib

from google.appengine.api import users
from google.appengine.ext import ndb

import jinja2
import webapp2

import login

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)
    
class CreateSessionPageHandler(webapp2.RequestHandler):
  def get(self):
  	param = self.request.params
  	context = { }
  	
  	context = login.generateLogInOutContextInfo(self, context)
  	
  	contents = JINJA_ENVIRONMENT.get_template('create_session.html').render(context)
  	self.response.write(contents)
  	
app = webapp2.WSGIApplication([
    ('/create_session.*', CreateSessionPageHandler)
], debug = True)
