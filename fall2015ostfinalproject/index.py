import cgi
import os
import urllib

from google.appengine.api import users
from google.appengine.ext import ndb
from google.appengine.ext.db import Query

import jinja2
import webapp2

import login
import sessions_datastore

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)
    
class MainPageHandler(webapp2.RequestHandler):
  def get(self):
  	params = self.request.params
  	context = { }
  	
  	"""Generate log in/out information"""
  	context = login.generateLogInOutContextInfo(self, context)
  	
  	sessions_query = sessions_datastore.Session.query(ancestor=sessions_datastore.sessions_key()).order(-sessions_datastore.Session.sessionStartTime)
  	sessions = sessions_query.fetch(1000000);
  	context['sessions'] = sessions;
    
  	contents = JINJA_ENVIRONMENT.get_template('index.html').render(context)
  	self.response.write(contents)
  	
app = webapp2.WSGIApplication([
    ('/', MainPageHandler)
], debug = True)
