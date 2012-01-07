# coding=utf-8

import os

from google.appengine.api        import users
from google.appengine.ext.webapp import template
from ForceLogin  import ForceLoginPage
from trip.person import persons

""" ---------------------------------------------------------- """
"""                         PERSONS                            """
""" ---------------------------------------------------------- """

class PersonPage(ForceLoginPage):
  template_path = os.path.join(os.path.dirname(__file__), 'persons.html')
  i_pid    = 0
  i_act    = ''
  i_name   = ''
  i_dative = ''
  i_me     = 0

  
  def Get(self):

    i_pid = 0
    if self.request.get('pid'):
      try:
        i_pid = int(self.request.get('pid'))
      except ValueError:
        i_pid = 0

    edit_rec = (i_pid != 0)


    template_values = {
      'page_title':  'Водители и пассажиры',
      'app_text':    'Приложения',
      'trip_text':   'Проезд',
      'page_status':  persons.status,
      'edit_rec':     edit_rec,
      'cur':          persons.get(i_pid),
      'pers':         persons.all()
      }
    return template.render(PersonPage.template_path, template_values)

  def check_param(self, a_pid, a_act, a_name, a_dative, a_me):

    if (a_act != 'insert') and (a_act != 'update') and (a_act != 'delete') and (a_act != 'cancel'):
      persons.status = 'Недопустимое значение параметра action: "' + a_act + '"'
      return False
    
    self.i_act = a_act

    if (self.i_act == 'update') or (self.i_act == 'delete'):
      try:
        self.i_pid = int(a_pid)
      except ValueError:
        persons.status = 'Прикладная ошибка: не определен идентификатор записи'
        self.i_act = 'cancel'
        return False
    
    if (self.i_act == 'update') or (self.i_act == 'insert'):
      if (a_name != ''):
        persons.last_name = a_name

      if (a_dative != ''):
        persons.last_dative = a_dative

      if (a_name != ''):
        self.i_name = a_name
        p = persons.Person.all().filter('user', users.GetCurrentUser()).filter('name', a_name).get()
        if p:
          persons.status = 'Такое имя уже есть'
          self.i_act = 'cancel'
          return False
      else:
        persons.status = 'Не задано имя'
        self.i_act = 'cancel'
        return False
        
      if (a_dative != ''):
        self.i_dative = a_dative
        p = persons.Person.all().filter('user', users.GetCurrentUser()).filter('dative', a_dative).get()
        if p:
          persons.status = 'Такое имя в дательном падеже уже есть'
          self.i_act = 'cancel'
          return False
      else:
        persons.status = 'Не задано имя в дательном падеже'
        self.i_act = 'cancel'
        return False

      self.i_me = 0
      if (a_me == 'true'):
        self.i_me = 1
        me_code = persons.me_code()
        if (me_code != 0):
          persons.status = 'Уже есть персона, помеченная признаком "Я"'
          self.i_act = 'cancel'
          return False

    return True


        
  def post(self):
    a_pid    = self.request.get('pid')
    a_act    = self.request.get('action')
    a_name   = self.request.get('name')
    a_dative = self.request.get('dative')
    a_me     = self.request.get('me')
    
    persons.status = ''

    # Назад
    if (a_act == 'back'):
      self.redirect('/trip')
    else:
      if self.check_param(a_pid, a_act, a_name, a_dative, a_me):
        # Добавление
        if (self.i_act == 'insert'):
          persons.insert(self.i_name, self.i_dative, self.i_me)
        # Изменение
        elif (self.i_act == 'update'):
          persons.update(self.i_pid, self.i_name, self.i_dative, self.i_me)
        # Удаление
        elif (self.i_act == 'delete'):
          persons.delete(self.i_pid)
        # Ошибка
        elif (self.i_act != 'cancel'):
          persons.status = 'Необработанная прикладная ошибка'
        # Отмена
        else:
          persons.status = ''

        persons.last_name   = ''
        persons.last_dative = ''
        self.redirect('/trip/person')
      
      elif (a_act == 'update'):
        self.redirect('/trip/person?pid=' + a_pid)
      else:
        self.redirect('/trip/person')
      


