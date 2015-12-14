import cgi
import os
import urllib

from google.appengine.api import users
from google.appengine.ext import ndb

import jinja2
import webapp2

import login
import sessions_datastore

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)
    
class SessionPageHandler(webapp2.RequestHandler):
  def post(self):
  	params = self.request.params
  	context = { }
  	
  	"""Generate log in/out information"""
  	context = login.generateLogInOutContextInfo(self, context)
  	
  	"""Get user information"""
  	user = users.get_current_user();
  	context['user'] = user;
  	if user:
  	  context['userId'] = user.user_id();
  	  context['userEmail'] = user.email();
  	  
  	"""Query all sessions"""
  	sessions_query = sessions_datastore.Session.query(ancestor=sessions_datastore.sessions_key()).order(-sessions_datastore.Session.sessionStartTime)
  	sessions = sessions_query.fetch(1000000);
  	context['sessions'] = sessions;
  	
  	"""Get the clicked session"""
  	for session in sessions:
  	  if session.sessionGUID == params['sessionGUID']:
  	    context['session'] = session;
  	  	
  	contents = JINJA_ENVIRONMENT.get_template('session.html').render(context)
  	self.response.write(contents)
  	
app = webapp2.WSGIApplication([
    ('/session.*', SessionPageHandler)
], debug = True)
