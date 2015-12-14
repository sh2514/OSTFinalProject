from google.appengine.ext import ndb

def reservations_key():
  return ndb.Key('Reservations', 'default_reservations')

class Reservation(ndb.Model):
  """Model for representing an individual reservations entry."""
  reservationOwner = ndb.StringProperty(indexed = True);
  reservationEmail = ndb.StringProperty(indexed = True);
  sessionOwner = ndb.StringProperty(indexed = False);
  sessionName = ndb.StringProperty(indexed = False);
  sessionStartTime = ndb.DateTimeProperty(indexed = True);
  sessionDuration = ndb.IntegerProperty(indexed = False);
