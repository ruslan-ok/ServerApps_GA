# coding=utf-8

import os
import datetime

from google.appengine.ext.webapp import template
from ForceLogin  import ForceLoginPage
import garage


""" ---------------------------------------------------------- """
"""                          GARAGE                            """
""" ---------------------------------------------------------- """

class GaragePage(ForceLoginPage):
  template_path = os.path.join(os.path.dirname(__file__), 'garage.html')
  i_pid    = 0
  i_act    = ''
  i_date   = datetime.datetime.now()
  i_kol    = 0.
  i_price  = 0
  i_course = 0
  i_usd    = 0

  
  def Get(self):

    i_pid = 0
    if self.request.get('pid'):
      try:
        i_pid = int(self.request.get('pid'))
      except ValueError:
        i_pid = 0

    if (self.request.get('act') == 'del'):
      garage.del_all()
    
    template_values = {
      'app_text':       'Приложения',
      'imp_text':       'Импорт из файла',
      'page_title':     'Гаражные расходы',
      'garage_summary':  garage.summary(2),
      'garage_status':   garage.status,
      'edit_rec':        (i_pid != 0),
      'cur':             garage.get(i_pid),
      'opers':           garage.all()
      }
    return template.render(GaragePage.template_path, template_values)


  def check_param(self, a_pid, a_act, a_date, a_kol, a_price, a_course, a_usd, a_kontr, a_text):

    if (a_act != 'insert') and (a_act != 'update') and (a_act != 'delete') and (a_act != 'cancel'):
      garage.status = 'Недопустимое значение параметра action: "' + a_act + '"'
      return False
    
    self.i_act = a_act

    if (self.i_act == 'update') or (self.i_act == 'delete'):
      try:
        self.i_date = datetime.datetime.strptime(a_date, "%d.%m.%Y")
      except ValueError:
        garage.status = 'Некорректное значение даты'
        self.i_act = 'cancel'
        return False

      try:
        self.i_pid = int(a_pid)
      except ValueError:
        garage.status = 'Прикладная ошибка: не определен идентификатор записи'
        self.i_act = 'cancel'
        return False
    
    if (self.i_act == 'update') or (self.i_act == 'insert'):
      try:
        self.i_kol = float(a_kol)
      except ValueError:
        garage.status = 'Некорректное значение количества'
        self.i_act = 'cancel'
        return False

      try:
        self.i_price = int(a_price)
      except ValueError:
        garage.status = 'Некорректное значение цены'
        self.i_act = 'cancel'
        return False

      try:
        self.i_course = int(a_course)
      except ValueError:
        garage.status = 'Некорректное значение курса доллара'
        self.i_act = 'cancel'
        return False

      try:
        self.i_usd = int(a_usd)
      except ValueError:
        garage.status = 'Некорректное значение суммы в долларах'
        self.i_act = 'cancel'
        return False

      if (self.i_usd == 0) and ((self.i_kol == 0) or (self.i_course == 0) or (self.i_price == 0)):
        garage.status = 'Должна быть указана сумма в долларах или количество, цена в рублях и курс доллара'
        self.i_act = 'cancel'
        return False

      if (a_kontr == ''):
        garage.status = 'Не указан контрагент'
        self.i_act = 'cancel'
        return False

      if (a_text == ''):
        garage.status = 'Нет описания операции'
        self.i_act = 'cancel'
        return False

    return True


        
  def post(self):
    a_pid    = self.request.get('pid')
    a_act    = self.request.get('action')
    a_date   = self.request.get('date')
    a_kol    = self.request.get('kol')
    a_price  = self.request.get('price')
    a_course = self.request.get('course')
    a_usd    = self.request.get('usd')
    a_kontr  = self.request.get('kontr')
    a_text   = self.request.get('text')
    
    garage.status = ''

    # Назад
    if (a_act == 'back'):
      self.redirect('/')
    else:
      if self.check_param(a_pid, a_act, a_date, a_kol, a_price, a_course, a_usd, a_kontr, a_text):
        # Добавление
        if (self.i_act == 'insert'):
          garage.insert(self.i_date, self.i_kol, self.i_price, self.i_course, self.i_usd, a_kontr, a_text)
        # Изменение
        elif (self.i_act == 'update'):
          garage.update(self.i_pid, self.i_date, self.i_kol, self.i_price, self.i_course, self.i_usd, a_kontr, a_text)
        # Удаление
        elif (self.i_act == 'delete'):
          garage.delete(self.i_pid)
        # Ошибка
        elif (self.i_act != 'cancel'):
          garage.status = 'Необработанная прикладная ошибка'
        # Отмена
        else:
          garage.status = ''

      self.redirect('/garage')

