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
import utilities



JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)


    
class MainPageHandler(webapp2.RequestHandler):

  def get(self):
  	params = self.request.params
  	context = { }
  	context = utilities.redirectToIndexPage(self, context);
    
  	contents = JINJA_ENVIRONMENT.get_template('index.html').render(context)
  	self.response.write(contents)
  	
  	
  	
  def post(self):
  	params = self.request.params;
  	context = { };
  	context = login.generateLogInOutContextInfo(self, context)
	  
	if 'delete_form_submit' in params:
	  """Query all reservations"""
  	  reservations_query = reservations_datastore.Reservation.query(ancestor=reservations_datastore.reservations_key()).order(reservations_datastore.Reservation.reservationStartTime);
  	  reservations = reservations_query.fetch(1000000);
	  
	  """Delete the reservation specified"""
	  for reservation in reservations:
	    if reservation.reservationGUID == params['reservationGUID']:
	      reservation.key.delete();
	      
	if 'session_search_submit' in params:
	  """Query all sessions"""
	  sessions_query = sessions_datastore.Session.query(ancestor=sessions_datastore.sessions_key()).order(-sessions_datastore.Session.sessionStartTime)
	  sessions = sessions_query.fetch(1000000);
	  matchedSessions = [];
	  sessionSearched = params['sessionSearchText'];
	  for session in sessions:
	    if session.sessionName == sessionSearched:
		  matchedSessions.append(session);
	  context['sessions'] = matchedSessions;
	  context['str'] = str;
  	  context['present'] = datetime.datetime.now();
  	  context['datetime'] = datetime;
		  
	  contents = JINJA_ENVIRONMENT.get_template('search.html').render(context)
	  self.response.write(contents)
	  return;
	  
	if 'session_search_by_time_submit' in params:
	  """Query all sessions"""
	  sessions_query = sessions_datastore.Session.query(ancestor=sessions_datastore.sessions_key()).order(-sessions_datastore.Session.sessionStartTime)
	  sessions = sessions_query.fetch(1000000);
	  matchedSessions = [];
	  
	  searchStartTime = params['reservation_start_time'];
	  startDate = searchStartTime.split("T")[0];
	  startTime = searchStartTime.split("T")[1];
  	  startDateTokens = startDate.split("-");
  	  startTimeTokens = startTime.split(":");
  	  convertedStartTime = datetime.datetime(int(startDateTokens[0]), int(startDateTokens[1]), int(startDateTokens[2]), int(startTimeTokens[0]), int(startTimeTokens[1]));
  	  if params['reservation_duration'] != "":
  	    if not utilities.is_integer(params['reservation_duration']) or 'reservation_duration'<= 0:
  	      context['notification'] = 'Invalid duration entered!';
  	      contents = JINJA_ENVIRONMENT.get_template('search.html').render(context)
  	      self.response.write(contents)
  	      return;
  	    else:
  	      searchDuration = int(params['reservation_duration']);
	      durationInSeconds = searchDuration * 60;
	      convertedEndTime = convertedStartTime + datetime.timedelta(seconds = durationInSeconds);
	
	  present = datetime.datetime.now();
	  for session in sessions:
	    if session.sessionStartTime > present and session.sessionStartTime > convertedStartTime:
		  if params['reservation_duration'] != "":
		    if session.sessionEndTime > convertedEndTime:
			  matchedSessions.append(session);
		  else:
		    matchedSessions.append(session);
	      
	  context['sessions'] = matchedSessions;
	  context['str'] = str;
  	  context['present'] = datetime.datetime.now();
  	  context['datetime'] = datetime;
	      
	  contents = JINJA_ENVIRONMENT.get_template('search.html').render(context)
	  self.response.write(contents)
	  return;
      
	self.get();
	
	
  	
app = webapp2.WSGIApplication([
    ('/', MainPageHandler)
], debug = True)
