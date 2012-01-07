# coding=utf-8

import os

from google.appengine.ext.webapp import template
from ForceLogin import ForceLoginPage
from garage import garage


""" ---------------------------------------------------------- """
"""                      GARAGE IMPORT                         """
""" ---------------------------------------------------------- """

gi_status = ''

class GarImpPage(ForceLoginPage):
  template_path = os.path.join(os.path.dirname(__file__), 'GarImp.html')
  
  def Get(self):

    template_values = {
      'app_text': 'Приложения',
      'status':    gi_status
    }
    return template.render(GarImpPage.template_path, template_values)

  def post(self):
    text = str(self.request.get('myfile'))
    
    lines = text.split('\n')
    fields = []
    if len(lines) > 0:
      fields = lines[0].split('\t')
    gi_status = 'filesize = ' + str(len(text)) + ', lines = ' + str(len(lines)) + ', fields = ' + str(len(fields))
    garage.import_from_file(text)
    self.redirect('/garage')
