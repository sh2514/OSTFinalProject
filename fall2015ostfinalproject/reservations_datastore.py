from google.appengine.ext import ndb

def reservations_key():
  return ndb.Key('Reservations', 'default_reservations')

class Reservation(ndb.Model):
  """Model for representing an individual reservations entry."""
  reservationGUID = ndb.StringProperty(indexed = True);
  reservationOwnerName = ndb.StringProperty(indexed = True);
  reservationOwner = ndb.StringProperty(indexed = True);
  reservationEmail = ndb.StringProperty(indexed = True);
  reservationStartTime = ndb.DateTimeProperty(indexed = True);
  reservationDuration = ndb.IntegerProperty(indexed = False);
  sessionGUID = ndb.StringProperty(indexed = False);
  sessionInstructor = ndb.StringProperty(indexed = False);
  sessionOwner = ndb.StringProperty(indexed = False);
  sessionName = ndb.StringProperty(indexed = False);
