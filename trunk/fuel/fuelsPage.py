# coding=utf-8

import os
import datetime

from google.appengine.ext.webapp import template
from ForceLogin import ForceLoginPage
from fuel       import fuels


""" ---------------------------------------------------------- """
"""                          FUEL                              """
""" ---------------------------------------------------------- """

class FuelPage(ForceLoginPage):
  template_path = os.path.join(os.path.dirname(__file__), 'fuels.html')
  i_pid     = 0
  i_act     = ''
  i_date    = datetime.datetime.now()
  i_counter = 0
  i_volume  = 0.
  i_price   = 0.

  
  def Get(self):

    i_pid = 0
    if self.request.get('pid'):
      try:
        i_pid = int(self.request.get('pid'))
      except ValueError:
        i_pid = 0

    template_values = {
      'app_text':     'Приложения',
      'page_title':   'Заправка',
      'fuel_summary':  fuels.summary(),
      'fuel_status':   fuels.status,
      'edit_rec':      (i_pid != 0),
      'cur':           fuels.get(i_pid),
      'fuels':         fuels.all()
      }
    return template.render(FuelPage.template_path, template_values)


  def check_param(self, a_pid, a_act, a_date, a_counter, a_volume, a_price):

    if (a_act != 'insert') and (a_act != 'update') and (a_act != 'delete') and (a_act != 'cancel'):
      fuels.status = 'Недопустимое значение параметра action: "' + a_act + '"'
      return False
    
    self.i_act = a_act

    if (self.i_act == 'update') or (self.i_act == 'delete'):
      try:
        self.i_pid = int(a_pid)
      except ValueError:
        fuels.status = 'Прикладная ошибка: не определен идентификатор записи'
        self.i_act = 'cancel'
        return False
    
    if (self.i_act == 'update') or (self.i_act == 'insert'):
      try:
        self.i_date = datetime.datetime.strptime(a_date, "%d.%m.%Y")
      except ValueError:
        fuels.status = 'Некорректное значение даты'
        self.i_act = 'cancel'
        return False

      try:
        self.i_counter = int(a_counter)
      except ValueError:
        fuels.status = 'Некорректное значение счетчика'
        self.i_act = 'cancel'
        return False

      try:
        self.i_volume = float(a_volume)
      except ValueError:
        fuels.status = 'Некорректное значение объёма'
        self.i_act = 'cancel'
        return False

      try:
        self.i_price = int(a_price)
      except ValueError:
        fuels.status = 'Некорректное значение цены'
        self.i_act = 'cancel'
        return False

    return True


        
  def post(self):
    a_pid     = self.request.get('pid')
    a_act     = self.request.get('action')
    a_date    = self.request.get('date')
    a_counter = self.request.get('counter')
    a_volume  = self.request.get('volume')
    a_price   = self.request.get('price')
    a_text    = self.request.get('text')
    
    fuels.status = ''

    # Назад
    if (a_act == 'back'):
      self.redirect('/')
    else:
      if self.check_param(a_pid, a_act, a_date, a_counter, a_volume, a_price):
        # Добавление
        if (self.i_act == 'insert'):
          fuels.insert(self.i_date, self.i_counter, self.i_volume, self.i_price, a_text)
        # Изменение
        elif (self.i_act == 'update'):
          fuels.update(self.i_pid, self.i_date, self.i_counter, self.i_volume, self.i_price, a_text)
        # Удаление
        elif (self.i_act == 'delete'):
          fuels.delete(self.i_pid)
        # Ошибка
        elif (self.i_act != 'cancel'):
          fuels.status = 'Необработанная прикладная ошибка'
        # Отмена
        else:
          fuels.status = ''

      self.redirect('/fuel')
