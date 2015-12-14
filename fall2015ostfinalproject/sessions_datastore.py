from google.appengine.ext import ndb

def sessions_key():
  return ndb.Key('Sessions', 'default_sessions')

class Session(ndb.Model):
  """Model for representing an individual sessions entry."""
  sessionOwner = ndb.StringProperty(indexed = False);
  sessionEmail = ndb.StringProperty(indexed = False);
  sessionName = ndb.StringProperty(indexed = True);
  sessionStartTime = ndb.DateTimeProperty(indexed = True);
  sessionEndTime = ndb.DateTimeProperty(indexed = True);
  sessionTags = ndb.StringProperty(indexed = False);
