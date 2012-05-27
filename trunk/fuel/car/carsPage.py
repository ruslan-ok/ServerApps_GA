# coding=utf-8

import os

from google.appengine.api        import users
from google.appengine.ext.webapp import template
from ForceLogin  import ForceLoginPage
from fuel.car import cars

""" ---------------------------------------------------------- """
"""                           CARS                             """
""" ---------------------------------------------------------- """

class CarPage(ForceLoginPage):
  template_path = os.path.join(os.path.dirname(__file__), 'cars.html')
  i_pid    = 0
  i_act    = ''
  i_name   = ''
  i_plate  = ''
  i_active = 0

  
  def Get(self):

    i_pid = 0
    if self.request.get('pid'):
      try:
        i_pid = int(self.request.get('pid'))
      except ValueError:
        i_pid = 0

    edit_rec = (i_pid != 0)


    template_values = {
      'page_title':  'Автомобили',
      'app_text':    'Приложения',
      'fuel_text':   'Заправка',
      'page_status':  cars.status,
      'edit_rec':     edit_rec,
      'cur':          cars.get(i_pid),
      'cars':         cars.all()
      }
    return template.render(CarPage.template_path, template_values)

  def check_param(self, a_pid, a_act, a_name, a_plate, a_active):

    if (a_act != 'insert') and (a_act != 'update') and (a_act != 'delete') and (a_act != 'cancel'):
      cars.status = 'Недопустимое значение параметра action: "' + a_act + '"'
      return False
    
    self.i_act = a_act

    if (self.i_act == 'update') or (self.i_act == 'delete'):
      try:
        self.i_pid = int(a_pid)
      except ValueError:
        cars.status = 'Прикладная ошибка: не определен идентификатор записи'
        self.i_act = 'cancel'
        return False
    
    if (self.i_act == 'update') or (self.i_act == 'insert'):
      if (a_name != '') and (a_name != '?'):
        cars.name = a_name
      else:
        cars.status = 'Не задано название'
        self.i_act = 'cancel'
        return False

      if (a_name == '') or (a_name == '?'):
        cars.status = 'Не задано название'
        self.i_act = 'cancel'
        return False
      else:
        self.i_name = a_name
        if (self.i_act == 'insert'):
          p = cars.Car.all().filter('user', users.GetCurrentUser()).filter('name', a_name).get()
          if p:
            cars.status = 'Такое имя уже есть'
            self.i_act = 'cancel'
            return False
        
      self.i_plate = a_plate
      self.i_active = int(a_active)

    return True


        
  def post(self):
    a_pid    = self.request.get('pid')
    a_act    = self.request.get('action')
    a_name   = self.request.get('name')
    a_plate  = self.request.get('plate')
    a_active = self.request.get('car_act')
    
    cars.status = ''

    # Назад
    if (a_act == 'back'):
      self.redirect('/fuel')
    else:
      if self.check_param(a_pid, a_act, a_name, a_plate, a_active):
        # Добавление
        if (self.i_act == 'insert'):
          cars.insert(self.i_name, self.i_plate, self.i_active)
        # Изменение
        elif (self.i_act == 'update'):
          cars.update(self.i_pid, self.i_name, self.i_plate, self.i_active)
        # Удаление
        elif (self.i_act == 'delete'):
          cars.delete(self.i_pid)
        # Ошибка
        elif (self.i_act != 'cancel'):
          cars.status = 'Необработанная прикладная ошибка'
        # Отмена
        else:
          cars.status = ''

        cars.name   = ''
        cars.active = False
        self.redirect('/fuel/car')
      
      elif (a_act == 'update'):
        self.redirect('/fuel/car?pid=' + a_pid)
      else:
        self.redirect('/fuel/car')
      


