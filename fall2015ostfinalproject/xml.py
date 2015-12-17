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



JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)
    
    
    
class XMLPageHandler(webapp2.RequestHandler):
  def get(self):
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
  	
    """Query all reservations"""
    reservations_query = reservations_datastore.Reservation.query(ancestor=reservations_datastore.reservations_key()).order(-reservations_datastore.Reservation.reservationStartTime);
    reservations = reservations_query.fetch(1000000);
    context['reservations'] = reservations;

    context['present'] = datetime.datetime.now();
    context['datetime'] = datetime;
    context['str'] = str;

    contents = JINJA_ENVIRONMENT.get_template('index.html').render(context)
    self.response.write(contents)	



  def post(self):
  	params = self.request.params
  	context = { }
  	
  	"""Generate log in/out information"""
  	context = login.generateLogInOutContextInfo(self, context)

  	"""Query all sessions"""
  	sessions_query = sessions_datastore.Session.query(ancestor=sessions_datastore.sessions_key()).order(-sessions_datastore.Session.sessionStartTime);
  	sessions = sessions_query.fetch(1000000);
  	context['sessions'] = sessions;
  	
  	"""Query all reservations"""
  	reservations_query = reservations_datastore.Reservation.query(ancestor=reservations_datastore.reservations_key()).order(-reservations_datastore.Reservation.reservationTime);
  	reservations = reservations_query.fetch(1000000);
  	context['reservations'] = reservations;
  	
  	"""Get the selected session"""
  	context['sessionGUID'] = params['sessionGUID'];
  	context['present'] = datetime.datetime.now();
  	context['datetime'] = datetime;  
  	
  	contents = JINJA_ENVIRONMENT.get_template('xml.html').render(context)
  	self.response.write(contents)
  	
  	
  	
app = webapp2.WSGIApplication([
    ('/xml.*', XMLPageHandler)
], debug = True)
