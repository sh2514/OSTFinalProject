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
import reservations_datastore

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
		thisSession = session;
		
	"""Query all reservations"""
  	reservations_query = reservations_datastore.Reservation.query(ancestor=reservations_datastore.reservations_key()).order(reservations_datastore.Reservation.reservationStartTime);
  	reservations = reservations_query.fetch(1000000);
  	context['reservations'] = reservations;
  	    
  	    
  	    
  	"""Check if modify session form had been submitted"""
  	if 'edit_session_submit' in params:	
  	  thisSession.sessionName = params['session_name'];
  	  
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
  	  
  	  thisSession.sessionStartTime = parsedStartTimeInput;
  	  thisSession.sessionEndTime = parsedEndTimeInput;
  	  thisSession.sessionRawStartTime = params['session_start_time'];
  	  thisSession.sessionRawEndTime = params['session_end_time'];
  	  thisSession.sessionTags = params['session_tags'];
  	  
  	  present = datetime.datetime.now();
  	  if thisSession.sessionStartTime > present and thisSession.sessionStartTime < thisSession.sessionEndTime:
  	  	thisSession.put();
		context['notification'] = 'Session modifications submitted!';
  	  elif thisSession.sessionStartTime <= present:
  	  	context['notification'] = 'Invalid start time specified!';
	  elif thisSession.sessionStartTime > session.sessionEndTime:
  	  	context['notification'] = 'Invalid end time specified!';
  	  context['session'] = thisSession;  	  



  	"""Check if a reservation form had been submitted"""
  	if user and 'reserve_session_submit' in params:
  	  rawStartTimeInput = params['reservation_start_time'];
  	  startDate = rawStartTimeInput.split("T")[0];
  	  startTime = rawStartTimeInput.split("T")[1];
  	  startDateTokens = startDate.split("-");
  	  startTimeTokens = startTime.split(":");
  	  parsedStartTimeInput = datetime.datetime(int(startDateTokens[0]), int(startDateTokens[1]), int(startDateTokens[2]), int(startTimeTokens[0]), int(startTimeTokens[1]));
  	
	  reservationGUID = str(uuid.uuid4());
	  reservation = reservations_datastore.Reservation(parent = reservations_datastore.reservations_key()); 
	  reservation.reservationGUID = reservationGUID;
	  reservation.reservationOwnerName = user.nickname();
	  reservation.reservationOwner = user.user_id();
	  reservation.reservationEmail = user.email();
	  reservation.reservationStartTime = parsedStartTimeInput;
	  reservation.reservationDuration = int(params['reservation_duration']);
	  reservation.sessionGUID = params['sessionGUID'];
	  reservation.sessionInstructor = params['sessionInstructor'];
	  reservation.sessionOwner = params['sessionOwner'];
	  reservation.sessionName = params['sessionName'];
	  
	  """Check if reservation valid before storing"""
	  alreadyReserved = False;
	  for reservationClone in reservations:
	  	if reservationClone.reservationOwner == user.user_id() and reservationClone.sessionGUID == params['sessionGUID']:
	  	  alreadyReserved = True;
	  
	  present = datetime.datetime.now();
	  durationInSeconds = reservation.reservationDuration * 60;
	  if alreadyReserved:
	  	context['notification'] = 'You have already reserved the session!';
	  elif parsedStartTimeInput > present and parsedStartTimeInput >= thisSession.sessionStartTime and durationInSeconds > 0:
	    potentialEndTime = parsedStartTimeInput + datetime.timedelta(seconds = durationInSeconds);
	    if potentialEndTime <= thisSession.sessionEndTime:
	      reservation.put();
	      context['notification'] = 'Reservation made!';
	    else:
	      context['notification'] = 'Duration specified is too long!';
	  elif durationInSeconds <= 0:
	  	context['notification'] = 'Invalid duration specified!';
	  elif parsedStartTimeInput < thisSession.sessionStartTime:
	  	context['notification'] = 'Invalid start time specified!';
	  elif parsedStartTimeInput <= present:
	  	context['notification'] = 'Invalid start time specified!';
	  
	  context['reservationGUID'] = reservation.reservationGUID;
	  context['reservationOwnerName'] = reservation.reservationOwnerName;
	  context['reservationOwner'] = reservation.reservationOwner;
	  context['reservationEmail'] = reservation.reservationEmail;
	  context['reservationStartTime'] = reservation.reservationStartTime;
	  context['reservationDuration'] = reservation.reservationDuration;
	  context['sessionGUID'] = reservation.sessionGUID;
	  context['sessionInstructor'] = reservation.sessionInstructor;
	  context['sessionOwner'] = reservation.sessionOwner;
	  context['sessionName'] = reservation.sessionName;
	elif 'reserve_session_submit' in params:
	  context['notification'] = 'You must be signed in to make a reservation!';
  	
  	context['present'] = datetime.datetime.now();
  	context['datetime'] = datetime;  	
  	
  	context['tags'] = str(context['session'].sessionTags).split(",");
  	  	
  	contents = JINJA_ENVIRONMENT.get_template('session.html').render(context)
  	self.response.write(contents)
  	
app = webapp2.WSGIApplication([
    ('/session.*', SessionPageHandler)
], debug = True)
