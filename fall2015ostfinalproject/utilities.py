import datetime

from google.appengine.api import users

import login
import sessions_datastore
import reservations_datastore



def redirectToIndexPage(self, context):
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
  sessions_query = sessions_datastore.Session.query(ancestor=sessions_datastore.sessions_key()).order(-sessions_datastore.Session.sessionStartTime);
  sessions = sessions_query.fetch(1000000);
  context['sessions'] = sessions;

  """Query all reservations"""
  reservations_query = reservations_datastore.Reservation.query(ancestor=reservations_datastore.reservations_key()).order(-reservations_datastore.Reservation.reservationTime);
  reservations = reservations_query.fetch(1000000);
  context['reservations'] = reservations;
  
  sessionsGUIDByLastReservation = [];
  sessionsByLastReservation = [];
  for reservation in reservations:
    if not (reservation.sessionGUID in sessionsGUIDByLastReservation):
      sessionsGUIDByLastReservation.append(reservation.sessionGUID);
      for session in sessions:
        if session.sessionGUID == reservation.sessionGUID:
          sessionsByLastReservation.append(session);
          break;
  for session in sessions:
    if not (session in sessionsByLastReservation):
      sessionsByLastReservation.append(session);
  context['sessionsByLastReservation'] = sessionsByLastReservation;

  context['present'] = datetime.datetime.now();
  context['datetime'] = datetime;
  context['str'] = str;
  
  return context;
