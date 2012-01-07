# coding=utf-8

import wsgiref.handlers
import os
import datetime

from google.appengine.api import users
from google.appengine.ext import db
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template

from trip     import trips
from fuel     import fuels
from garage   import garage
from communal import communal

from ForceLogin                 import ForceLoginPage
from trip.person.personsPage    import PersonPage
from trip.tripsPage             import TripPage
from fuel.fuelsPage             import FuelPage
from garage.garagePage          import GaragePage
from communal.communalPage      import CommunalPage
from other.otherPage            import OtherPage
from garage.imprt.GarImpPage    import GarImpPage
from communal.imprt.CommImpPage import CommImpPage
from communal.edit.commEditPage import CommEditPage

""" ---------------------------------------------------------- """

""" ---------------------------------------------------------- """
def get_now():
  now = datetime.datetime.now()
  return str(now.day) + '.' + str(now.month) + '.' + str(now.year)


""" ---------------------------------------------------------- """
"""                          APPS                              """
""" ---------------------------------------------------------- """

class Apps(db.Model):
  pid     = db.IntegerProperty(required=True)
  user    = db.UserProperty(required=True)
  name    = db.StringProperty(required=True)
  page    = db.StringProperty()
  title   = db.StringProperty()
  summary = db.StringProperty()

def init():
  apps = Apps.all().filter('user', users.GetCurrentUser())
  if apps:
    db.delete(apps)
  
  s1 = trips.summary()
  s2 = fuels.summary()
  s3 = communal.summary()
  s4 = garage.summary(1)
  
  Apps(pid = 1, user = users.GetCurrentUser(), name = u'Проезд',   page='/trip',     title = '', summary = s1).put()
  Apps(pid = 2, user = users.GetCurrentUser(), name = u'Заправка', page='/fuel',     title = '', summary = s2).put()
  Apps(pid = 3, user = users.GetCurrentUser(), name = u'Квартира', page='/communal', title = '', summary = s3).put()
  Apps(pid = 4, user = users.GetCurrentUser(), name = u'Гараж',    page='/garage',   title = '', summary = s4).put()


def get_apps():
  init()
  return Apps.all().filter('user', users.GetCurrentUser()).order('pid')

""" ---------------------------------------------------------- """
"""                          MAIN                              """
""" ---------------------------------------------------------- """

class MainPage(ForceLoginPage):
  template_path = os.path.join(os.path.dirname(__file__), 'main.html')
  def Get(self):

    template_values = {
      'user':         users.GetCurrentUser(),
      'logout_url':   users.CreateLogoutURL("/"),
      'logout_text': 'Выйти',

      'page_title':  'Приложения',

      'apps':         get_apps()
    }
    return template.render(MainPage.template_path, template_values)

def main():
  application = webapp.WSGIApplication(
    [('/',                MainPage),
     ('/trip',            TripPage),
     ('/trip/person',     PersonPage),
     ('/garage',          GaragePage),
     ('/garage/import',   GarImpPage),
     ('/fuel',            FuelPage),
     ('/communal',        CommunalPage),
     ('/communal/edit',   CommEditPage),
     ('/communal/import', CommImpPage),
     ('/other',           OtherPage)],
    debug=True)

  wsgiref.handlers.CGIHandler().run(application)

if __name__ == '__main__':
  main()
