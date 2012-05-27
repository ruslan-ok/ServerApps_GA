# coding=utf-8
import datetime

from google.appengine.api import users
from google.appengine.ext import db

from trip.person import persons

"""--------------------------------------------------------------"""
"""                         TRIP info                            """
"""--------------------------------------------------------------"""


status = ''


def summary():
  ret = u''
  saldos = Saldo.all().filter('user', users.GetCurrentUser())
  
  for s in saldos:
    if (s.summ != 0):
      if (ret != u''):
        ret += u', '
      if (s.summ < 0):
        ret += persons.NameI(s.p1) + ' ' + persons.NameD(s.p2) + ' ' + str(-1*s.summ)
      else:
        ret += persons.NameI(s.p2) + ' ' + persons.NameD(s.p1) + ' ' + str(s.summ)
  
  return u'<span style="color:yellow">' + ret + u'</span>'


"""--------------------------------------------------------------"""
"""                         TRIP                                 """
"""--------------------------------------------------------------"""

class Trip(db.Model):
  pid       = db.IntegerProperty(required=True)
  user      = db.UserProperty(required=True)
  date      = db.DateTimeProperty(required=True, auto_now_add=True)
  year      = db.IntegerProperty(required=True)
  week      = db.IntegerProperty(required=True)
  days      = db.IntegerProperty(required=True)
  oper      = db.IntegerProperty(required=True)
  price     = db.IntegerProperty(required=True)
  driver    = db.IntegerProperty(required=True)
  passenger = db.IntegerProperty(required=True)
  text      = db.StringProperty()

  def s_days(self):
    if (self.oper != 0):
      return ''

    s = '';
    for i in range(0, 7):
      n = 0
      m = 0
      for j in range(0, 2):
        if (self.days & (1 << (i*2+j))):
          n = n + 1
          if (j == 0):
            m = 1
      if (n == 0):
        s += '-'
      elif (n == 1):
        if (m == 1):
          s += '\''
        else:
          s += '.'
      else:
        s += ':'
    return s

  def s_oper(self):
    if (self.oper == 0):
      return 'проезд'
    else:
      return 'оплата'

  def s_prc(self):
    if (self.oper == 0):
      return self.price
    else:
      return ''

  def c_oper(self):
    if (self.oper == 0):
      return 'oper_trip'
    else:
      return 'oper_pay'

  def s_driv(self):
    pers = persons.get(self.driver)
    if pers:
      return pers.name
    else:
      return '?'

  def s_pass(self):
    pers = persons.get(self.passenger)
    if pers:
      return pers.name
    else:
      return '?'

  def summa(self):
    if (self.oper == 1):
      return self.price

    kol = 0
    for i in range(0, 7):
      for j in range(0, 2):
        if (self.days & (1 << (i*2+j))):
          kol = kol + 1
    return kol * self.price



def insert(i_year, i_week, i_days, i_oper, i_price, i_driver, i_pass, i_text):
  maxnum = 1
  last = Trip.all().filter('user', users.GetCurrentUser()).order('-pid').get()
  if last:
    maxnum = last.pid + 1
  trip = Trip(pid       = maxnum, \
              user      = users.GetCurrentUser(), \
              date      = datetime.datetime.now(), \
              year      = i_year, \
              week      = i_week, \
              days      = i_days, \
              oper      = i_oper, \
              price     = i_price, \
              driver    = i_driver, \
              passenger = i_pass, \
              text      = i_text)
  if trip:
    trip.put()
    saldo_update(trip.driver, trip.passenger, trip.oper, trip.summa())

def update(i_pid, i_year, i_week, i_days, i_oper, i_price, i_driver, i_pass, i_text):
  trip = Trip.all().filter('user', users.GetCurrentUser()).filter('pid', i_pid).get()
  if trip:
    saldo_update(trip.driver, trip.passenger, trip.oper, -1*trip.summa())
    trip.date      = datetime.datetime.now()
    trip.year      = i_year
    trip.week      = i_week
    trip.days      = i_days
    trip.oper      = i_oper
    trip.price     = i_price
    trip.driver    = i_driver
    trip.passenger = i_pass
    trip.text      = i_text
    trip.put()
    saldo_update(trip.driver, trip.passenger, trip.oper, trip.summa())

def delete(i_pid):
  trip = Trip.all().filter('user', users.GetCurrentUser()).filter('pid', i_pid).get()
  if trip:
    saldo_update(trip.driver, trip.passenger, trip.oper, -1*trip.summa())
    trip.delete()

def get(i_pid):
  if i_pid:
    return Trip.all().filter('user', users.GetCurrentUser()).filter('pid', i_pid).get()
  else:
    # Инициализация полей новой записи
    shift = datetime.date.today().weekday() * 2
    a_week = int(datetime.datetime.now().strftime("%j")) / 7 + 1
    #enab = 0
    #for i in range(0, shift-1):
    #  enab += (1 << shift)
    last_trip = Trip.all().filter('user', users.GetCurrentUser()).filter('oper', 0).order('-year').order('-week').order('-days').get()
    last_pay  = Trip.all().filter('user', users.GetCurrentUser()).filter('oper', 1).order('-year').order('-week').order('-days').get()
    
    week_trip = a_week
    week_pay  = a_week
    week_new  = a_week
    
    days_trip = 0
    days_pay  = 0
    days_new  = (1 << shift) + (1 << (shift+1))
    
    oper_new  = 0

    price_trip = 0
    price_pay  = 0
    price_new  = 0

    drvr_new = 2
    pass_new = 1

    if last_trip: # последняя поездка
      week_trip  = last_trip.week
      days_trip  = last_trip.days
      price_trip = last_trip.price
      drvr_new   = last_trip.driver
      pass_new   = last_trip.passenger
    if last_pay:  # последняя оплата
      week_pay  = last_pay.week
      days_pay  = last_pay.days
      price_pay = last_pay.price

    price_new = price_trip
    #if (week_trip <= week_pay):
      #week_new  = week_trip
      #price_new = price_trip
    #else:
      #week_new  = week_pay
      #price_new = price_pay

    """
    for i in range(0, 15):
      a1 = enab      & (1 << i)
      a2 = days_trip & (1 << i)
      a3 = days_pay  & (1 << i)
      
      if (a1 > 0) and (a2 <> a3):
        if (a2 > a3):
          oper_new = 1 # оплата
        else
          oper_new = 0 # поездка
    """

    #a_days = (1 << shift) + (1 << (shift+1))

    return Trip(pid       = 0, \
                user      = users.GetCurrentUser(), \
                date      = datetime.datetime.now(), \
                year      = datetime.datetime.now().year, \
                week      = week_new, \
                #days      = days_new, \
                days      = 0, \
                oper      = oper_new, \
                price     = price_new, \
                driver    = drvr_new, \
                passenger = pass_new, \
                text      = '')

def all():
  all = Trip.gql('WHERE user = :1 ORDER BY year DESC, week DESC, date DESC, oper DESC, days DESC LIMIT 30', users.GetCurrentUser())
  return all

"""--------------------------------------------------------------"""
"""                         SALDO                                """
"""--------------------------------------------------------------"""

class Saldo(db.Model):
  user = db.UserProperty(required=True)
  p1   = db.IntegerProperty(required=True)
  p2   = db.IntegerProperty(required=True)
  me   = db.IntegerProperty(required=True)
  summ = db.IntegerProperty(required=True)

def saldo_update(p1, p2, oper, sum):
  if (p1 > p2):
    tmp = p1
    p1 = p2
    p2 = tmp
    sum *= -1
  if (oper == 1):
    sum *= -1
  saldo = Saldo.all().filter('user', users.GetCurrentUser()).filter('p1', p1).filter('p2', p2).get()
  if saldo:
    saldo.summ += sum
  else:
    me_code = persons.me_code()
    is_me = 0
    if (p1 == me_code) or (p2 == me_code):
      is_me = 1
    saldo = Saldo(user = users.GetCurrentUser(), p1 = p1, p2 = p2, me = is_me, summ = sum)
  saldo.put()

def saldo_recount():
  saldos = Saldo.all().filter('user', users.GetCurrentUser())
  if saldos:
    db.delete(saldos)
  trips = Trip.all().filter('user', users.GetCurrentUser())
  for t in trips:
    saldo_update(t.driver, t.passenger, t.oper, t.summa())
