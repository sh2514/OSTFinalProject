import cgi
import os
import urllib
import datetime
import uuid

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


    
class CreateSessionPageHandler(webapp2.RequestHandler):
  
  def get(self):
  	params = self.request.params
  	context = { }
  	context = login.generateLogInOutContextInfo(self, context)
  	
  	contents = JINJA_ENVIRONMENT.get_template('create_session.html').render(context)
  	self.response.write(contents)
  	
  	
  	
  def post(self):
  	params = self.request.params
  	context = { }
  	context = login.generateLogInOutContextInfo(self, context)
  	
  	"""Query all sessions"""
  	sessions_query = sessions_datastore.Session.query(ancestor=sessions_datastore.sessions_key()).order(-sessions_datastore.Session.sessionStartTime);
  	sessions = sessions_query.fetch(1000000);
  	context['sessions'] = sessions;
  	
  	"""Parse HTML date and time inputs into datetime object"""
  	rawStartTimeInput = params['session_start_time'];
  	startDate = rawStartTimeInput.split("T")[0];
  	startTime = rawStartTimeInput.split("T")[1];
  	startDateTokens = startDate.split("-");
  	startTimeTokens = startTime.split(":");
  	parsedStartTimeInput = datetime.datetime(int(startDateTokens[0]), int(startDateTokens[1]), int(startDateTokens[2]), int(startTimeTokens[0]), int(startTimeTokens[1]));
  	
  	rawEndTimeInput = params['session_end_time'];
  	endDate = rawEndTimeInput.split("T")[0];
  	endTime = rawEndTimeInput.split("T")[1];
  	endDateTokens = endDate.split("-");
  	endTimeTokens = endTime.split(":");
  	parsedEndTimeInput = datetime.datetime(int(endDateTokens[0]), int(endDateTokens[1]), int(endDateTokens[2]), int(endTimeTokens[0]), int(endTimeTokens[1]));
  	
  	sessionGUID = str(uuid.uuid4());
  	
  	"""Add template values"""
  	context['notification'] = 'Session Created!';
  	context['sessionResponse'] = True;
  	context['sessionGUID'] = sessionGUID;
  	context['sessionInstructor'] = users.get_current_user().nickname();
  	context['sessionOwner'] = users.get_current_user().user_id();
  	context['sessionEmail'] = users.get_current_user().email();
  	context['sessionName'] = params['session_name'];
  	context['sessionStartTime'] = parsedStartTimeInput;
  	context['sessionEndTime'] = parsedEndTimeInput;
  	context['sessionTags'] = params['session_tags'];
  	context['sessionRawStartTime'] = rawStartTimeInput;
  	context['sessionRawEndTime'] = rawEndTimeInput;
  	
  	"""Create session for data store"""
  	session = sessions_datastore.Session(parent = sessions_datastore.sessions_key());
  	session.sessionGUID = sessionGUID;
  	session.sessionInstructor = users.get_current_user().nickname();
  	session.sessionOwner = users.get_current_user().user_id();
  	session.sessionEmail = users.get_current_user().email();
  	session.sessionName = params['session_name'];
  	session.sessionStartTime = parsedStartTimeInput;
  	session.sessionEndTime = parsedEndTimeInput;
  	session.sessionTags = params['session_tags'];
  	session.sessionRawStartTime = rawStartTimeInput;
  	session.sessionRawEndTime = rawEndTimeInput;
	  
	"""Determine if new session is valid, handle appropriately"""
	present = datetime.datetime.now();
	if session.sessionStartTime > present and session.sessionStartTime < session.sessionEndTime:
	  isValidNewSession = True;
	  for sessionClone in sessions:
	    if session.sessionOwner == sessionClone.sessionOwner and ((session.sessionStartTime >= sessionClone.sessionStartTime and session.sessionStartTime < sessionClone.sessionEndTime) or (sessionClone.sessionStartTime < session.sessionEndTime and session.sessionEndTime <= sessionClone.sessionEndTime)):
	      isValidNewSession = False;
	  if isValidNewSession:
	    session.put();
	    context['notification'] = 'Session created!';
	  else:
	    context['notification'] = 'Session overlaps an existing session!';
  	elif session.sessionStartTime <= present:
  	  context['notification'] = 'Invalid start time specified!';
  	elif session.sessionStartTime > session.sessionEndTime:
  	  context['notification'] = 'Invalid end time specified!';
  	
  	contents = JINJA_ENVIRONMENT.get_template('create_session.html').render(context)
  	self.response.write(contents)
  	
  	
  	
app = webapp2.WSGIApplication([
    ('/create_session.*', CreateSessionPageHandler)
], debug = True)
