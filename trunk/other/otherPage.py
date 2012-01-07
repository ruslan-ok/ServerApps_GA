# coding=utf-8

import os

from google.appengine.ext.webapp import template
from ForceLogin  import ForceLoginPage
from other       import otherData


""" ---------------------------------------------------------- """
"""                          OTHER                             """
""" ---------------------------------------------------------- """

class OtherPage(ForceLoginPage):
  template_path = os.path.join(os.path.dirname(__file__), 'other.html')
  
  def Get(self):

    template_values = {
        'app_text':    'Приложения',
        'page_title':  'Прочее',
        'trip_status':  otherData.status
      }
    return template.render(OtherPage.template_path, template_values)


