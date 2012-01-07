# coding=utf-8

import os

from google.appengine.ext.webapp import template
from ForceLogin import ForceLoginPage
import garage


""" ---------------------------------------------------------- """
"""                          IMPORT                            """
""" ---------------------------------------------------------- """

class FileContent():
  text = ''

class ImportPage(ForceLoginPage):
  template_path = os.path.join(os.path.dirname(__file__), 'import.html')
  f1 = FileContent()
  
  def Get(self):

    template_values = {
      'app_text':    'Приложения',
      'file_content': self.f1.text
    }
    return template.render(ImportPage.template_path, template_values)

  def post(self):
    text = str(self.request.get('myfile'))
    
    lines = text.split('\n')
    fields = []
    if len(lines) > 0:
      fields = lines[0].split('\t')
    self.f1.text = 'filesize = ' + str(len(text)) + ', lines = ' + str(len(lines)) + ', fields = ' + str(len(fields))
    garage.import_from_file(text)
    self.redirect('/import')
