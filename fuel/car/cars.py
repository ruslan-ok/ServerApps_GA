# coding=utf-8

from google.appengine.api import users
from google.appengine.ext import db
#from fuel                 import fuels

"""--------------------------------------------------------------"""
"""                           CAR info                           """
"""--------------------------------------------------------------"""

status = ''
"""
def updateAllFuels():
  fuels = Fuel.all().filter('user', users.GetCurrentUser())
  for fuel in fuels:
    fuel.car = 1
    fuel.put()
"""
"""--------------------------------------------------------------"""
"""                          CAR                                 """
"""--------------------------------------------------------------"""

class Car(db.Model):
  pid    = db.IntegerProperty(required=True)
  user   = db.UserProperty(required=True)
  name   = db.StringProperty(required=True)
  plate  = db.StringProperty()
  active = db.IntegerProperty()

def make_active(a_pid, a_active):
  if (a_active == 1):
    all = Car.all().filter('user', users.GetCurrentUser())
    for cur in all:
      if (cur.pid != a_pid and cur.active == 1):
        cur.active = 0
        cur.put()

def insert(i_name, i_plate, i_active):
  maxnum = 1
  last = Car.all().filter('user', users.GetCurrentUser()).order('-pid').get()
  if last:
    maxnum = last.pid + 1
  cars = Car(pid    = maxnum, \
             user   = users.GetCurrentUser(), \
             name   = i_name, \
             plate  = i_plate, \
             active = i_active)
  if cars:
    cars.put()
    make_active(maxnum, i_active)

def update(i_pid, i_name, i_plate, i_active):
  cars = Car.all().filter('user', users.GetCurrentUser()).filter('pid', i_pid).get()
  if cars:
    cars.name   = i_name
    cars.plate  = i_plate
    cars.active = i_active
    cars.put()
    make_active(i_pid, i_active)

def delete(i_pid):
  cars = Car.all().filter('user', users.GetCurrentUser()).filter('pid', i_pid).get()
  if cars:
    cars.delete()

def get(i_pid):
  if i_pid:
    return Car.all().filter('user', users.GetCurrentUser()).filter('pid', i_pid).get()
  else:
    # Инициализация полей новой записи
    # active_new = 1
    # name_new = 'Я'
    # dati_new = 'Мне'
    # car_new = Car.all().filter('user', users.GetCurrentUser()).filter('active', 1).get()
    # if me_pers:
    #   me_new = 0
    #   name_new = last_name
    #   dati_new = last_active

    return Car(pid = 0, user = users.GetCurrentUser(), name = '?', plate = '', active = 1)


def all():
  return Car.all().filter('user', users.GetCurrentUser()).order('-active').order('name')

def setActive(i_car):
  for car in all():
    if (car.pid == i_car):
      car.active = 1
    else:
      car.active = 0
    car.put()


  

#def me_code():
#  ret = 0
#  me = Car.all().filter('user', users.GetCurrentUser()).filter('me', 1).get()
#  if (me):
#    ret = me.pid
#  return ret


#def NameI(i_pid):
#  if (i_pid == 0):
#    return '?'
#  else:
#    cars = Car.all().filter('user', users.GetCurrentUser()).filter('pid', i_pid).get()
#    if cars:
#      return cars.name
#    else:
#      return '?'


#def NameD(i_pid):
#  if (i_pid == 0):
#    return '?'
#  else:
#    cars = Car.all().filter('user', users.GetCurrentUser()).filter('pid', i_pid).get()
#    if cars:
#      return cars.active
#    else:
#      return '?'

