# coding=utf-8

from google.appengine.api import users
from google.appengine.ext import db

"""--------------------------------------------------------------"""
"""                         PERSON info                          """
"""--------------------------------------------------------------"""


status = ''
last_name   = ''
last_dative = ''

"""--------------------------------------------------------------"""
"""                         PERSON                               """
"""--------------------------------------------------------------"""

class Person(db.Model):
  pid    = db.IntegerProperty(required=True)
  user   = db.UserProperty(required=True)
  name   = db.StringProperty()
  dative = db.StringProperty()
  me     = db.IntegerProperty()

def insert(i_name, i_dative, i_me):
  maxnum = 1
  last = Person.all().filter('user', users.GetCurrentUser()).order('-pid').get()
  if last:
    maxnum = last.pid + 1
  pers = Person(pid    = maxnum, \
                user   = users.GetCurrentUser(), \
                name   = i_name, \
                dative = i_dative, \
                me     = i_me)
  if pers:
    pers.put()

def update(i_pid, i_name, i_dative, i_me):
  pers = Person.all().filter('user', users.GetCurrentUser()).filter('pid', i_pid).get()
  if pers:
    pers.name   = i_name
    pers.dative = i_dative
    pers.me     = i_me
    pers.put()

def delete(i_pid):
  pers = Person.all().filter('user', users.GetCurrentUser()).filter('pid', i_pid).get()
  if pers:
    pers.delete()

def get(i_pid):
  if i_pid:
    return Person.all().filter('user', users.GetCurrentUser()).filter('pid', i_pid).get()
  else:
    # Инициализация полей новой записи
    me_new = 1
    name_new = 'Я'
    dati_new = 'Мне'
    me_pers = Person.all().filter('user', users.GetCurrentUser()).filter('me', 1).get()
    if me_pers:
      me_new = 0
      name_new = last_name
      dati_new = last_dative

    return Person(pid = 0, user = users.GetCurrentUser(), name = name_new, dative = dati_new, me = me_new)


def all():
  return Person.all().filter('user', users.GetCurrentUser()).order('-me').order('name')


def me_code():
  ret = 0
  me = Person.all().filter('user', users.GetCurrentUser()).filter('me', 1).get()
  if (me):
    ret = me.pid
  return ret


def NameI(i_pid):
  if (i_pid == 0):
    return '?'
  else:
    pers = Person.all().filter('user', users.GetCurrentUser()).filter('pid', i_pid).get()
    if pers:
      return pers.name
    else:
      return '?'


def NameD(i_pid):
  if (i_pid == 0):
    return '?'
  else:
    pers = Person.all().filter('user', users.GetCurrentUser()).filter('pid', i_pid).get()
    if pers:
      return pers.dative
    else:
      return '?'

