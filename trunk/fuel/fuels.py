# coding=utf-8
import datetime

from google.appengine.api import users
from google.appengine.ext import db

"""--------------------------------------------------------------"""
"""                         FUEL info                            """
"""--------------------------------------------------------------"""


status = ''


def summary():
  fuels = Fuel.all().filter('user', users.GetCurrentUser()).order('-date').order('-counter')
  counter_max = 0
  counter_min = 0
  total_volume = 0

  for f in fuels:
    counter_min = f.counter

    if (counter_max == 0):
      counter_max = f.counter
    else:
      total_volume += f.volume

  km = counter_max - counter_min

  if (total_volume == 0) or (km == 0):
    return u'Не удалось вычислить средний расход'

  return u'<span style="color:yellow">' + str(round((total_volume / km) * 100, 2)) + u'</span> л на 100 км'


"""--------------------------------------------------------------"""
"""                         FUEL                                 """
"""--------------------------------------------------------------"""

class Fuel(db.Model):
  pid     = db.IntegerProperty(required=True)
  user    = db.UserProperty(required=True)
  date    = db.DateTimeProperty(required=True, auto_now_add=True)
  counter = db.IntegerProperty(required=True)
  volume  = db.FloatProperty(required=True)
  price   = db.FloatProperty(required=True)
  text    = db.StringProperty()

  def s_date(self):
    return str(self.date.day) + '.' + str(self.date.month) + '.' + str(self.date.year)

  def iprice(self):
    return int(self.price)

  def summ(self):
    return int(round(self.volume * self.price, 0))

def insert(i_date, i_counter, i_volume, i_price, i_text):
  maxnum = 1
  last = Fuel.all().filter('user', users.GetCurrentUser()).order('-pid').get()
  if last:
    maxnum = last.pid + 1
  fuel = Fuel(pid     = maxnum, \
              user    = users.GetCurrentUser(), \
              date    = i_date, \
              counter = i_counter, \
              volume  = i_volume, \
              price   = float(i_price), \
              text    = i_text)
  if fuel:
    fuel.put()

def update(i_pid, i_date, i_counter, i_volume, i_price, i_text):
  fuel = Fuel.all().filter('user', users.GetCurrentUser()).filter('pid', i_pid).get()
  if fuel:
    fuel.date    = i_date
    fuel.counter = i_counter
    fuel.volume  = i_volume
    fuel.price   = float(i_price)
    fuel.text    = i_text
    fuel.put()

def delete(i_pid):
  fuel = Fuel.all().filter('user', users.GetCurrentUser()).filter('pid', i_pid).get()
  if fuel:
    fuel.delete()

def get(i_pid):
  if i_pid:
    return Fuel.all().filter('user', users.GetCurrentUser()).filter('pid', i_pid).get()
  else:
    # Инициализация полей новой записи
    last_counter = 0
    last_price   = 0.

    last_fuel = Fuel.all().filter('user', users.GetCurrentUser()).order('-date').order('-counter').get()
    if last_fuel:
      last_counter = last_fuel.counter
      last_price   = last_fuel.price
    
    return Fuel(pid     = 0, \
                user    = users.GetCurrentUser(), \
                date    = datetime.datetime.now(), \
                counter = last_counter, \
                volume  = 10., \
                price   = last_price, \
                text    = "")

def all():
  return Fuel.all().filter('user', users.GetCurrentUser()).order('-date').order('-counter')

