import cgi
import os
import urllib
import datetime

from google.appengine.api import users
from google.appengine.ext import ndb
import jinja2
import webapp2

import login
import sessions_datastore
import reservations_datastore
import utilities



JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)
    
    
    
class TagPageHandler(webapp2.RequestHandler):
	
  def get(self):
    params = self.request.params
    context = { }

    context = utilities.redirectToIndexPage(self, context);

    contents = JINJA_ENVIRONMENT.get_template('index.html').render(context)
    self.response.write(contents)
	
		
	
  def post(self):
  	params = self.request.params
  	context = { }
  	context = login.generateLogInOutContextInfo(self, context)
  	
  	"""Get user information"""
  	user = users.get_current_user();
  	context['user'] = user;
  	if user:
  	  context['userId'] = user.user_id();
  	  context['userEmail'] = user.email();

  	"""Query all sessions"""
  	sessions_query = sessions_datastore.Session.query(ancestor=sessions_datastore.sessions_key()).order(-sessions_datastore.Session.sessionStartTime);
  	sessions = sessions_query.fetch(1000000);
  	context['sessions'] = sessions;
  	
  	"""Find matching session"""
  	matchingSessions = [];
  	for session in sessions:
  	  sessionTags = str(session.sessionTags).split(",");
  	  for tag in sessionTags:
  	  	if tag.strip() == params['tagName'].strip():
  	  	  matchingSessions.append(session);
  	
  	context['str'] = str;
  	context['present'] = datetime.datetime.now();
  	context['datetime'] = datetime; 
  	context['sessions'] = matchingSessions;
	context['tagName'] = params['tagName'];
  	
  	contents = JINJA_ENVIRONMENT.get_template('tag.html').render(context)
  	self.response.write(contents)
  	
  	
  	
app = webapp2.WSGIApplication([
    ('/tag.*', TagPageHandler)
], debug = True)
