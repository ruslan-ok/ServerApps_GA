# coding=utf-8

import os

from google.appengine.ext.webapp import template
from ForceLogin import ForceLoginPage
from communal import communal


""" ---------------------------------------------------------- """
"""                   COMMUNAL IMPORT                          """
""" ---------------------------------------------------------- """

class CommImpPage(ForceLoginPage):
  template_path = os.path.join(os.path.dirname(__file__), 'CommImp.html')
  ci_status = ''
  
  def Get(self):

    template_values = {
      'app_text': 'Приложения',
      'ci_status': self.ci_status
    }
    return template.render(CommImpPage.template_path, template_values)

  def post(self):
    self.ci_status = 'www'
    text = str(self.request.get('myfile'))
    
    #lines = text.split('\n')
    #fields = []
    #if len(lines) > 0:
    #  fields = lines[0].split('\t')
    #ci_status = 'filesize = ' + str(len(text)) + ', lines = ' + str(len(lines)) + ', fields = ' + str(len(fields))
    communal.import_from_file(text)
    self.redirect('/communal')
