import cgi
import os
import urllib

from google.appengine.api import users
from google.appengine.ext import ndb

import jinja2
import webapp2

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)
    
def generateLogInOutContextInfo(self, context):
  user = users.get_current_user()
  if user:
    context['userLogInOutLink'] = users.create_logout_url(self.request.uri)
    context['userLogInOutText'] = 'Sign Out'
  else:
  	context['userLogInOutLink'] = users.create_login_url(self.request.uri)
  	context['userLogInOutText'] = 'Sign In'
  return context
    
class MainPageHandler(webapp2.RequestHandler):
  def get(self):
  	param = self.request.params
  	context = { }
  	
  	context = generateLogInOutContextInfo(self, context)
  	
  	contents = JINJA_ENVIRONMENT.get_template('index.html').render(context)
  	self.response.write(contents)
  	
app = webapp2.WSGIApplication([
    ('/', MainPageHandler)
], debug = True)
