# coding=utf-8

import os

from google.appengine.api import users
from google.appengine.ext import webapp

""" ---------------------------------------------------------- """
"""                          LOGIN                             """
""" ---------------------------------------------------------- """

class ForceLoginPage(webapp.RequestHandler):
  template_path = os.path.join(os.path.dirname(__file__), 'base.html')
  def get(self):
    user = users.GetCurrentUser()
    if user:
      response = self.Get()
      if response:
        self.response.out.write(response)
    else:
      self.redirect(users.CreateLoginURL(self.request.uri))      

