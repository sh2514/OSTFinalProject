from google.appengine.ext import ndb



"""Get key for datastore"""
def sessions_key():
  return ndb.Key('Sessions', 'default_sessions')

"""Representation of a session for datastore"""
class Session(ndb.Model):
  """Model for representing an individual sessions entry."""
  sessionGUID = ndb.StringProperty(indexed = False);
  sessionInstructor = ndb.StringProperty(indexed = True);
  sessionOwner = ndb.StringProperty(indexed = False);
  sessionEmail = ndb.StringProperty(indexed = False);
  sessionName = ndb.StringProperty(indexed = True);
  sessionStartTime = ndb.DateTimeProperty(indexed = True);
  sessionEndTime = ndb.DateTimeProperty(indexed = True);
  sessionTags = ndb.StringProperty(indexed = False);
  sessionRawStartTime = ndb.StringProperty(indexed = False);
  sessionRawEndTime = ndb.StringProperty(indexed = False);
