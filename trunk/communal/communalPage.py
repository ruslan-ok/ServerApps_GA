# coding=utf-8

import os
import datetime

from google.appengine.ext.webapp import template
from ForceLogin  import ForceLoginPage
import communal


""" ---------------------------------------------------------- """
"""                          COMMUNAL                          """
""" ---------------------------------------------------------- """

class CommunalPage(ForceLoginPage):
  template_path = os.path.join(os.path.dirname(__file__), 'communal.html')

  def Get(self):
    template_values = {
      'app_text':        'Приложения',
      'imp_text':        'Импорт из файла',
      'page_title':      'Коммунальные платежи',
      'communal_summary': communal.summary(),
      'communal_status':  communal.status,
      'bills':            communal.all()
      }
    return template.render(CommunalPage.template_path, template_values)


  def post(self):
    communal.status = ''
    next = communal.insert()
    self.redirect('/communal/edit?year=' + str(next.year) + '&month=' + str(next.month))


