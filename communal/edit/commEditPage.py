# coding=utf-8

import os
import datetime

from google.appengine.ext.webapp import template
from ForceLogin  import ForceLoginPage
from communal import communal


def get_int(_value):
  ret = 0
  if (_value != ''):
    try:
      ret = int(_value)
    except ValueError:
      communal.status = 'Некорректен числовой параметр "' + _value + '"'
  return ret


def get_float(_value):
  ret = 0.
  if (_value != ''):
    try:
      ret = float(_value)
    except ValueError:
      communal.status = 'Некорректен вещественный параметр "' + _value + '"'
  return ret

  
""" ---------------------------------------------------------- """
"""                          COMMUNAL                          """
""" ---------------------------------------------------------- """

class CommEditPage(ForceLoginPage):
  template_path = os.path.join(os.path.dirname(__file__), 'commEdit.html')
  i_act    = ''
  i_year   = datetime.datetime.now().year
  i_month  = datetime.datetime.now().month

  
  def Get(self):

    i_year  = 0
    i_month = 0

    try:
      i_year  = int(self.request.get('year'))
      i_month = int(self.request.get('month'))
    except ValueError:
      i_year  = 0
      i_month = 0

    is_first = communal.isFirst(i_year, i_month)
    is_last  = communal.isLast(i_year, i_month)

    template_values = {
      'app_text':        'Приложения',
      'imp_text':        'Импорт из файла',
      'page_title':      'Коммунальные платежи',
      'communal_status':  communal.status,
      'cur':              communal.get(i_year, i_month),
      'is_first':         is_first,
      'is_last':          is_last,
      'uttermost':        (is_last == 1)
      }
    return template.render(CommEditPage.template_path, template_values)


  def check_param(self, a_act, a_year, a_month, a_dCounter, a_dPay, a_tv_tar, a_tv_pay, a_phone_tar, \
                  a_phone_pay, a_zhirovka, a_hot_pay, a_repair_pay, a_ZKX_pay, a_el_old, a_el_new, \
                  a_el_tar, a_el_pay, a_cold_old, a_cold_new, a_hot_old, a_hot_new, a_water_tar, \
                  a_water_pay, a_gas_old, a_gas_new, a_gas_tar, a_gas_pay, a_penalty, a_prev_per, a_course):

    if (a_act != 'insert') and (a_act != 'update') and (a_act != 'delete') and (a_act != 'cancel'):
      communal.status = 'Недопустимое значение параметра action: "' + a_act + '"'
      return False
    
    self.i_act = a_act

    if (self.i_act == 'update') or (self.i_act == 'delete'):
      try:
        self.i_year = int(a_year)
      except ValueError:
        communal.status = 'Некорректное значение года'
        self.i_act = 'cancel'
        return False

      if (self.i_year < 2000) or (self.i_year > 3000):
        communal.status = 'Нереальное значение года'
        self.i_act = 'cancel'
        return False

      try:
        self.i_month = int(a_month)
      except ValueError:
        communal.status = 'Некорректное значение месяца'
        self.i_act = 'cancel'
        return False
    
      if (self.i_month < 1) or (self.i_month > 12):
        communal.status = 'Нереальное значение месяца'
        self.i_act = 'cancel'
        return False

    ret = True
    
    if (self.i_act == 'update'):
      n_year  = self.i_year
      n_month = self.i_month + 1
      if (n_month > 12):
        n_year += 1
        n_month = 1
    
      self.i_dCounter = datetime.datetime(n_year, n_month, 15)
      self.i_dPay     = self.i_dCounter

      try:
        self.i_dCounter = datetime.datetime.strptime(a_dCounter, "%d.%m.%Y")
      except ValueError:
        communal.status = 'Некорректная дата снятия показаний счетчиков'
        ret = False

      try:
        self.i_dPay = datetime.datetime.strptime(a_dPay, "%d.%m.%Y")
      except ValueError:
        communal.status = 'Некорректная дата платежей'
        ret = False

      self.i_tv_tar     = get_int(a_tv_tar)
      self.i_tv_pay     = get_int(a_tv_pay)
      self.i_phone_tar  = get_int(a_phone_tar)
      self.i_phone_pay  = get_int(a_phone_pay)
      self.i_zhirovka   = get_int(a_zhirovka)
      self.i_hot_pay    = get_int(a_hot_pay)
      self.i_repair_pay = get_int(a_repair_pay)
      self.i_ZKX_pay    = get_int(a_ZKX_pay)
      self.i_el_old     = get_int(a_el_old)
      self.i_el_new     = get_int(a_el_new)
      self.i_el_tar     = get_float(a_el_tar)
      self.i_el_pay     = get_int(a_el_pay)
      self.i_cold_old   = get_int(a_cold_old)
      self.i_cold_new   = get_int(a_cold_new) 
      self.i_hot_old    = get_int(a_hot_old)  
      self.i_hot_new    = get_int(a_hot_new)  
      self.i_water_tar  = get_float(a_water_tar) 
      self.i_water_pay  = get_int(a_water_pay) 
      self.i_gas_old    = get_int(a_gas_old)  
      self.i_gas_new    = get_int(a_gas_new)   
      self.i_gas_tar    = get_float(a_gas_tar)   
      self.i_gas_pay    = get_int(a_gas_pay)   
      self.i_penalty    = get_int(a_penalty)   
      self.i_prev_per   = get_int(a_prev_per)  
      self.i_course     = get_int(a_course)

    return ret

        
  def post(self):
    a_act        = self.request.get('action')
    a_year       = self.request.get('year')
    a_month      = self.request.get('month')
    a_dCounter   = self.request.get('dCounter')
    a_dPay       = self.request.get('dPay')
    a_tv_tar     = self.request.get('tv_tar')
    a_tv_pay     = self.request.get('tv_pay')
    a_phone_tar  = self.request.get('phone_tar')
    a_phone_pay  = self.request.get('phone_pay')
    a_zhirovka   = self.request.get('zhirovka')
    a_hot_pay    = self.request.get('hot_pay')
    a_repair_pay = self.request.get('repair_pay')
    a_ZKX_pay    = self.request.get('ZKX_pay')
    a_el_old     = self.request.get('el_old')
    a_el_new     = self.request.get('el_new')
    a_el_tar     = self.request.get('el_tar')
    a_el_pay     = self.request.get('el_pay')
    a_cold_old   = self.request.get('cold_old')
    a_cold_new   = self.request.get('cold_new')
    a_hot_old    = self.request.get('hot_old')
    a_hot_new    = self.request.get('hot_new')
    a_water_tar  = self.request.get('water_tar')
    a_water_pay  = self.request.get('water_pay')
    a_gas_old    = self.request.get('gas_old')
    a_gas_new    = self.request.get('gas_new')
    a_gas_tar    = self.request.get('gas_tar')
    a_gas_pay    = self.request.get('gas_pay')
    a_penalty    = self.request.get('penalty')
    a_prev_per   = self.request.get('prev_per')
    a_course     = self.request.get('course')
    
    communal.status = ''

    if self.check_param(a_act, a_year, a_month, a_dCounter, a_dPay, a_tv_tar, a_tv_pay, a_phone_tar, \
                a_phone_pay, a_zhirovka, a_hot_pay, a_repair_pay, a_ZKX_pay, a_el_old, a_el_new, \
                a_el_tar, a_el_pay, a_cold_old, a_cold_new, a_hot_old, a_hot_new, a_water_tar, \
                a_water_pay, a_gas_old, a_gas_new, a_gas_tar, a_gas_pay, a_penalty, a_prev_per, a_course):
      # Добавление
      if (self.i_act == 'insert'):
        per = communal.insert()
        communal.status = 'year=' + str(per.year) + '&month=' + str(per.month)
        self.redirect('/communal/edit?year=' + str(per.year) + '&month=' + str(per.month))
      # Изменение
      elif (self.i_act == 'update'):
        communal.update(self.i_year, self.i_month, self.i_dCounter, self.i_dPay, self.i_tv_tar, self.i_tv_pay, \
                        self.i_phone_tar, self.i_phone_pay, self.i_zhirovka, self.i_hot_pay, self.i_repair_pay, \
                        self.i_ZKX_pay, self.i_el_old, self.i_el_new, self.i_el_tar, self.i_el_pay, \
                        self.i_cold_old, self.i_cold_new, self.i_hot_old, self.i_hot_new, self.i_water_tar, \
                        self.i_water_pay, self.i_gas_old, self.i_gas_new, self.i_gas_tar, self.i_gas_pay, \
                        self.i_penalty, self.i_prev_per, self.i_course, self.request.get('text'))
      # Удаление
      elif (self.i_act == 'delete'):
        communal.delete(self.i_year, self.i_month)
      # Ошибка
      elif (self.i_act != 'cancel'):
        communal.status = 'Необработанная прикладная ошибка'
      # Отмена
      else:
        communal.status = ''

    self.redirect('/communal')


