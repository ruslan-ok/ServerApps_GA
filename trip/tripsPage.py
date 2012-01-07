# coding=utf-8

import os
import datetime

from google.appengine.ext.webapp import template
from ForceLogin  import ForceLoginPage
from trip        import trips
from trip.person import persons


""" ---------------------------------------------------------- """
"""                          TRIP                              """
""" ---------------------------------------------------------- """

class TripPage(ForceLoginPage):
  template_path = os.path.join(os.path.dirname(__file__), 'trips.html')
  i_pid    = 0
  i_act    = ''
  i_date   = datetime.datetime.now()
  i_year   = 0
  i_week   = 0
  i_days   = 0
  i_oper   = 0
  i_price  = 0
  i_driver = 0
  i_pass   = 0
  i_text   = ''

  
  def Get(self):

    i_pid = 0
    if self.request.get('pid'):
      try:
        i_pid = int(self.request.get('pid'))
      except ValueError:
        i_pid = 0

    if self.request.get('count'):
      trips.saldo_recount()

    trips.summary()

    template_values = {
      'app_text':       'Приложения',
      'count_text':     'Пересчитать',
      'pers_text':      'Люди',
      'week_text':      'Выходные',
      'page_title':     'Проезд',
      'trip_summary':    trips.summary(),
      'trip_status':     trips.status,
      'edit_rec':        (i_pid != 0),
      'cur':             trips.get(i_pid),
      'oper_trip':      'проезд',
      'oper_pay':       'оплата',
      'trips':           trips.all(),
      'persons':         persons.all()
      }
    return template.render(TripPage.template_path, template_values)


  def check_param(self, a_pid, a_act, a_year, a_week, a_days, a_oper, a_price, a_driver, a_pass):

    if (a_act != 'insert') and (a_act != 'update') and (a_act != 'delete') and (a_act != 'cancel'):
      trips.status = 'Недопустимое значение параметра action: "' + a_act + '"'
      return False
    
    self.i_act = a_act

    if (self.i_act == 'update') or (self.i_act == 'delete'):
      try:
        self.i_pid = int(a_pid)
      except ValueError:
        trips.status = 'Прикладная ошибка: не определен идентификатор записи'
        self.i_act = 'cancel'
        return False
    
    if (self.i_act == 'update') or (self.i_act == 'insert'):
      try:
        self.i_year = int(a_year)
        if (self.i_year < 2011) or (self.i_year > 3000):
          trips.status = 'Некорректное значение года'
          self.i_act = 'cancel'
          return False
      except ValueError:
        trips.status = 'Некорректное значение года'
        self.i_act = 'cancel'
        return False

      try:
        self.i_week = int(a_week)
        if (self.i_week < 0) or (self.i_week > 60):
          trips.status = 'Некорректный номер недели 1'
          self.i_act = 'cancel'
          return False
      except ValueError:
        trips.status = 'Некорректный номер недели 2'
        self.i_act = 'cancel'
        return False

      try:
        self.i_oper = int(a_oper)
        if (self.i_oper != 0) and (self.i_oper != 1):
          trips.status = 'Некорректно указана операция'
          self.i_act = 'cancel'
          return False
      except ValueError:
        trips.status = 'Некорректно указана операция'
        self.i_act = 'cancel'
        return False

      if (self.i_oper == 1):
        i_days = 0
      else:
        try:
          self.i_days = int(a_days)
          if (self.i_days == 0):
            trips.status = 'Не указаны дни'
            self.i_act = 'cancel'
            return False
        except ValueError:
          trips.status = 'Некорректно указаны дни'
          self.i_act = 'cancel'
          return False

      try:
        self.i_price = int(a_price)
      except ValueError:
        trips.status = 'Некорректное значение цены'
        self.i_act = 'cancel'
        return False

      try:
        self.i_driver = int(a_driver)
        if not persons.NameI(self.i_driver):
          trips.status = 'Указанный водитель не найден в справочнике водителей и пассажиров (код ' + str(self.i_driver) + ')'
          self.i_act = 'cancel'
          return False
      except ValueError:
        trips.status = 'Некорректно задан водитель'
        self.i_act = 'cancel'
        return False

      try:
        self.i_pass = int(a_pass)
        if not persons.NameI(self.i_pass):
          trips.status = 'Указанный пассажир не найден в справочнике водителей и пассажиров (код ' + str(self.i_pass) + ')'
          self.i_act = 'cancel'
          return False
      except ValueError:
        trips.status = 'Некорректно задан пассажир'
        self.i_act = 'cancel'
        return False

    return True


        
  def post(self):
    a_pid    = self.request.get('pid')
    a_act    = self.request.get('action')
    a_year   = self.request.get('year')
    a_week   = self.request.get('week')
    a_days   = self.request.get('ret_days')
    a_oper   = self.request.get('oper')
    a_price  = self.request.get('price')
    a_driver = self.request.get('driver')
    a_pass   = self.request.get('passenger')
    a_text   = self.request.get('text')
    
    trips.status = ''

    # Назад
    if (a_act == 'back'):
      self.redirect('/')
    else:
      if self.check_param(a_pid, a_act, a_year, a_week, a_days, a_oper, a_price, a_driver, a_pass):
        # Добавление
        if (self.i_act == 'insert'):
          trips.insert(self.i_year, self.i_week, self.i_days, self.i_oper, self.i_price, self.i_driver, self.i_pass, a_text)
          self.redirect('/')
        # Изменение
        elif (self.i_act == 'update'):
          trips.update(self.i_pid, self.i_year, self.i_week, self.i_days, self.i_oper, self.i_price, self.i_driver, self.i_pass, a_text)
          self.redirect('/')
        # Удаление
        elif (self.i_act == 'delete'):
          trips.delete(self.i_pid)
        # Ошибка
        elif (self.i_act != 'cancel'):
          trips.status = 'Необработанная прикладная ошибка'
        # Отмена
        else:
          trips.status = ''

      self.redirect('/trip')

