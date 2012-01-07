# coding=utf-8
import datetime
#import string

from google.appengine.api import users
from google.appengine.ext import db

"""--------------------------------------------------------------"""
"""                         COMMUNAL info                        """
"""--------------------------------------------------------------"""


status = ''
err = 0

"""--------------------------------------------------------------"""
"""                         COMMUNAL                             """
"""--------------------------------------------------------------"""

class Communal(db.Model):
  user       = db.UserProperty(required=True)
  year       = db.IntegerProperty(required=True)
  month      = db.IntegerProperty(required=True) # 1 - январь
  dCounter   = db.DateTimeProperty()
  dPay       = db.DateTimeProperty()
  tv_tar     = db.IntegerProperty()
  tv_pay     = db.IntegerProperty()
  phone_tar  = db.IntegerProperty()
  phone_pay  = db.IntegerProperty()
  zhirovka   = db.IntegerProperty()
  hot_pay    = db.IntegerProperty()
  repair_pay = db.IntegerProperty()
  ZKX_pay    = db.IntegerProperty()
  el_old     = db.IntegerProperty()
  el_new     = db.IntegerProperty()
  el_tar     = db.FloatProperty()
  el_pay     = db.IntegerProperty()
  cold_old   = db.IntegerProperty()
  cold_new   = db.IntegerProperty()
  hot_old    = db.IntegerProperty()
  hot_new    = db.IntegerProperty()
  water_tar  = db.FloatProperty()
  water_pay  = db.IntegerProperty()
  gas_old    = db.IntegerProperty()
  gas_new    = db.IntegerProperty()
  gas_tar    = db.FloatProperty()
  gas_pay    = db.IntegerProperty()
  penalty    = db.IntegerProperty()
  prev_per   = db.IntegerProperty()
  course     = db.IntegerProperty()
  text       = db.StringProperty()

  def s_dCounter(self):
    return str(self.dCounter.day) + '.' + str(self.dCounter.month) + '.' + str(self.dCounter.year)

  def s_dPay(self):
    return str(self.dPay.day) + '.' + str(self.dPay.month) + '.' + str(self.dPay.year)

  #def el_vol(self):
  #  return self.el_new - self.el_old #          self.el_new - self.el_old

  #def el_sum(self):
  #  return self.el_vol * self.el_tar

  #def water_vol(self):
  #  return (self.cold_new - self.cold_old) + (self.hot_new - self.hot_old)

  #def water_sum(self):
  #  return self.water_vol * self.water_tar

  #def gas_vol(self):
  #  return int(self.gas_new - self.gas_old)

  #def gas_sum(self):
  #  return self.gas_vol * self.gas_tar

  def total_bill(self):
    bill = self.tv_tar + self.phone_tar + self.zhirovka + \
           (self.el_new - self.el_old) * self.el_tar + \
           ((self.cold_new - self.cold_old) + (self.hot_new - self.hot_old)) * self.water_tar + \
           (self.gas_new - self.gas_old) * self.gas_tar
    return int(round(bill, 0))

  def total_usd(self):
    if (self.course == 0):
      return 0
    else:
      bill = self.tv_tar + self.phone_tar + self.zhirovka + \
             (self.el_new - self.el_old) * self.el_tar + \
             ((self.cold_new - self.cold_old) + (self.hot_new - self.hot_old)) * self.water_tar + \
             (self.gas_new - self.gas_old) * self.gas_tar
      return int(round(bill / self.course, 0))

  #def zhir_pay(self):
  #  return self.hot_pay + self.repair_pay + self.ZKX_pay

  def total_pay(self):
    pay = self.tv_pay + self.phone_pay + \
          self.hot_pay + self.repair_pay + self.ZKX_pay + \
          self.el_pay + self.water_pay + self.gas_pay
    return pay

  def debt(self):
    bill = self.tv_tar + self.phone_tar + self.zhirovka + \
           (self.el_new - self.el_old) * self.el_tar + \
           ((self.cold_new - self.cold_old) + (self.hot_new - self.hot_old)) * self.water_tar + \
           (self.gas_new - self.gas_old) * self.gas_tar
    pay = self.tv_pay + self.phone_pay + \
          self.hot_pay + self.repair_pay + self.ZKX_pay + \
          self.el_pay + self.water_pay + self.gas_pay
    return int(round(bill, 0)) - pay


def add_month(_date):
  if (_date.month < 12):
    return datetime.datetime(_date.year, _date.month + 1, _date.day)
  else:
    return datetime.datetime(_date.year+1, 1, _date.day)


def insert():
  last = Communal.all().filter('user', users.GetCurrentUser()).order('-year').order('-month').get()
  if last:
    n_year  = last.year
    n_month = last.month
    if (n_month < 12):
      n_month = n_month + 1
    else:
      n_year  = n_year + 1
      n_month = 1
      
    cmnl = Communal(user       = users.GetCurrentUser(), \
                    year       = n_year, \
                    month      = n_month, \
                    dCounter   = add_month(last.dCounter), \
                    dPay       = add_month(last.dPay), \
                    tv_tar     = last.tv_tar, \
                    tv_pay     = 0, \
                    phone_tar  = last.phone_tar, \
                    phone_pay  = 0, \
                    zhirovka   = last.zhirovka, \
                    hot_pay    = 0, \
                    repair_pay = 0, \
                    ZKX_pay    = 0, \
                    el_old     = last.el_new, \
                    el_new     = last.el_new+200, \
                    el_tar     = last.el_tar, \
                    el_pay     = 0, \
                    cold_old   = last.cold_new, \
                    cold_new   = last.cold_new+5, \
                    hot_old    = last.cold_old, \
                    hot_new    = last.cold_old+5, \
                    water_tar  = last.water_tar, \
                    water_pay  = 0, \
                    gas_old    = last.gas_new, \
                    gas_new    = last.gas_new+10, \
                    gas_tar    = last.gas_tar, \
                    gas_pay    = 0, \
                    penalty    = 0, \
                    prev_per   = 0, \
                    course     = last.course, \
                    text       = '')
  else:
    n_year  = datetime.datetime.now().year
    n_month = datetime.datetime.now().month
    if (n_month > 1):
      n_month = n_month - 1
    else:
      n_year  = n_year - 1
      n_month = 12

    cmnl = Communal(user       = users.GetCurrentUser(), \
                    year       = n_year, \
                    month      = n_month, \
                    dCounter   = datetime.datetime.now(), \
                    dPay       = datetime.datetime.now(), \
                    tv_tar     = 0, \
                    tv_pay     = 0, \
                    phone_tar  = 0, \
                    phone_pay  = 0, \
                    zhirovka   = 0, \
                    hot_pay    = 0, \
                    repair_pay = 0, \
                    ZKX_pay    = 0, \
                    el_old     = 0, \
                    el_new     = 0, \
                    el_tar     = 0., \
                    el_pay     = 0, \
                    cold_old   = 0, \
                    cold_new   = 0, \
                    hot_old    = 0, \
                    hot_new    = 0, \
                    water_tar  = 0., \
                    water_pay  = 0, \
                    gas_old    = 0, \
                    gas_new    = 0, \
                    gas_tar    = 0., \
                    gas_pay    = 0, \
                    penalty    = 0, \
                    prev_per   = 0, \
                    course     = 0, \
                    text       = '')
  cmnl.put()
  return cmnl

def update(i_year, i_month, i_dCounter, i_dPay, i_tv_tar, i_tv_pay, i_phone_tar, i_phone_pay, i_zhirovka, \
           i_hot_pay, i_repair_pay, i_ZKX_pay, i_el_old, i_el_new, i_el_tar, i_el_pay, i_cold_old, i_cold_new, \
           i_hot_old, i_hot_new, i_water_tar, i_water_pay, i_gas_old, i_gas_new, i_gas_tar, i_gas_pay, \
           i_penalty, i_prev_per, i_course, i_text):
  cmnl = Communal.all().filter('user', users.GetCurrentUser()).filter('year', i_year).filter('month', i_month).get()
  if cmnl:
    cmnl.dCounter   = i_dCounter
    cmnl.dPay       = i_dPay
    cmnl.tv_tar     = i_tv_tar
    cmnl.tv_pay     = i_tv_pay
    cmnl.phone_tar  = i_phone_tar
    cmnl.phone_pay  = i_phone_pay
    cmnl.zhirovka   = i_zhirovka
    cmnl.hot_pay    = i_hot_pay
    cmnl.repair_pay = i_repair_pay
    cmnl.ZKX_pay    = i_ZKX_pay
    cmnl.el_old     = i_el_old
    cmnl.el_new     = i_el_new
    cmnl.el_tar     = i_el_tar
    cmnl.el_pay     = i_el_pay
    cmnl.cold_old   = i_cold_old
    cmnl.cold_new   = i_cold_new
    cmnl.hot_old    = i_hot_old
    cmnl.hot_new    = i_hot_new
    cmnl.water_tar  = i_water_tar
    cmnl.water_pay  = i_water_pay
    cmnl.gas_old    = i_gas_old
    cmnl.gas_new    = i_gas_new
    cmnl.gas_tar    = i_gas_tar
    cmnl.gas_pay    = i_gas_pay
    cmnl.penalty    = i_penalty
    cmnl.prev_per   = i_prev_per
    cmnl.course     = i_course
    cmnl.text       = i_text
    cmnl.put()


def delete(i_year, i_month):
  cmnl = Communal.all().filter('user', users.GetCurrentUser()).filter('year', i_year).filter('month', i_month).get()
  if cmnl:
    cmnl.delete()


def isFirst(i_year, i_month):
  cmnl = Communal.all().filter('user', users.GetCurrentUser()).order('year').order('month').get()
  if cmnl:
    if (i_year == cmnl.year) and (i_month == cmnl.month):
      return 1
  return 0


def isLast(i_year, i_month):
  cmnl = Communal.all().filter('user', users.GetCurrentUser()).order('-year').order('-month').get()
  if cmnl:
    if (i_year == cmnl.year) and (i_month == cmnl.month):
      return 1
  return 0


def get(i_year, i_month):
  cmnl = Communal.all().filter('user', users.GetCurrentUser()).filter('year', i_year).filter('month', i_month).get()
  if cmnl:
    t_year    = cmnl.year
    t_month   = cmnl.month
    if (t_month > 1):
      t_month -= 1
    else:
      t_year  -= 1
      t_month = 12

    prev = Communal.all().filter('user', users.GetCurrentUser()).filter('year =', t_year).filter('month <=', t_month).order('-month').get()
    if prev:
      cmnl.el_old   = prev.el_new
      cmnl.cold_old = prev.cold_new
      cmnl.hot_old  = prev.hot_new
      cmnl.gas_old  = prev.gas_new

    return cmnl

  else:
    # Инициализация полей новой записи
    t_year    = datetime.datetime.now().year
    t_month   = datetime.datetime.now().month
    t_tv      = 0
    t_phone   = 0
    t_el      = 0
    t_el_tar  = 0.
    t_cold    = 0
    t_hot     = 0
    t_water   = 0.
    t_gas     = 0
    t_gas_tar = 0.
    t_course  = 0
    last = Communal.all().filter('user', users.GetCurrentUser()).order('-year').order('-month').get()
    if last:
      if (last.month == 12):
        t_year  = last.year + 1
        t_month = 1
      else:
        t_year  = last.year
        t_month = last.month + 1
      t_tv      = last.tv_tar
      t_phone   = last.phone_tar
      t_el      = last.el_new
      t_el_tar  = last.el_tar
      t_cold    = last.cold_new
      t_hot     = last.hot_new
      t_water   = last.water_tar
      t_gas     = last.gas_new
      t_gas_tar = last.gas_tar
      t_course  = last.course
  
    return Communal(user       = users.GetCurrentUser(), \
                    year       = t_year, \
                    month      = t_month, \
                    dCounter   = datetime.datetime.now(), \
                    dPay       = datetime.datetime.now(), \
                    tv_tar     = t_tv, \
                    tv_pay     = 0, \
                    phone_tar  = t_phone, \
                    phone_pay  = 0, \
                    zhirovka   = 0, \
                    hot_pay    = 0, \
                    repair_pay = 0, \
                    ZKX_pay    = 0, \
                    el_old     = t_el, \
                    el_new     = t_el + 100, \
                    el_tar     = t_el_tar, \
                    el_pay     = 0, \
                    cold_old   = t_cold, \
                    cold_new   = t_cold + 5, \
                    hot_old    = t_hot, \
                    hot_new    = t_hot + 5, \
                    water_tar  = t_water, \
                    water_pay  = 0, \
                    gas_old    = t_gas, \
                    gas_new    = t_gas + 5, \
                    gas_tar    = t_gas_tar, \
                    gas_pay    = 0, \
                    penalty    = 0, \
                    prev_per   = 0, \
                    course     = t_course, \
                    text       = '')

def all():
  return Communal.all().filter('user', users.GetCurrentUser()).order('-year').order('-month')


def get_fld(arr, num):
  if (arr[num] == ''):
    return 0
  else:
    return int(arr[num])


def get_dat(arr, num):
  if (arr[num] == ''):
    return datetime.datetine.now()
  else:
    f_tmp = str(arr[num]).split('.')
    return datetime.datetime(int(f_tmp[2]), int(f_tmp[1]), int(f_tmp[0]))


def subMonths(_y2, _m2, _y1, _m1):
  return (_y2 - _y1 - 1) * 12 + _m2 + (12 - _m1)


def days(_kol):
  if (_kol == 1):
    return u'<span style="color:red">Сегодня последний день.</span>'
  elif (_kol > 1) and (_kol < 5):
    return u'Осталось <span style="color:red">' + str(_kol) + u'</span> дня.'
  else:
    return u'Осталось <span style="color:yellow">' + str(_kol) + u'</span> дней.'


def checkPay(_mode, _year, _month):
  now = datetime.datetime.now()
  delta = subMonths(now.year, now.month, _year, _month)

  if (delta == 1) and (now.day >= 10) and (now.day <= 25):
    return days(26 - now.day)
    #if (_mode == 1):
    #  return u'<span style="color:yellow">Пора платить. ' + days(26 - now.day) + u'</span>'
    #else:
    #  return u'<span style="color:yellow">Не все счета оплачены. ' + days(26 - now.day) + u'</span>'
  elif (delta < 1) or ((delta == 1) and (now.day < 10)):
    return u''
  else:
    return u'<span style="color:red">Платеж просрочен</span>'


def summary():
  last = Communal.all().filter('user', users.GetCurrentUser()).order('-year').order('-month').get()
  if not last:
    return 'Сумма квартплаты за прошлый месяц, предупреждения о сроке оплаты'

  # Определяем за какой месяц была последняя оплата
  if (last.tv_pay  != 0) and (last.phone_pay != 0) and (last.hot_pay   != 0) and (last.repair_pay != 0) and \
     (last.ZKX_pay != 0) and (last.el_pay    != 0) and (last.water_pay != 0) and (last.gas_pay    != 0):
    # Последняя запись - всё оплачено
    if (last.month == 12):
      t_year  = last.year + 1
      t_month = 1
    else:
      t_year  = last.year
      t_month = last.month + 1
    return checkPay(1, t_year, t_month)
  elif (last.tv_pay  != 0) or (last.phone_pay != 0) or (last.hot_pay   != 0) or (last.repair_pay != 0) and \
       (last.ZKX_pay != 0) or (last.el_pay    != 0) or (last.water_pay != 0) or (last.gas_pay    != 0):
    # Последняя запись - оплачено частично
    return checkPay(2, last.year, last.month)
  else:
    # Последняя запись - ничего не оплачено. Считаем, что предыдущий месяц оплачен польностью
    return checkPay(1, last.year, last.month)

def import_from_file(_text):

  opers = Communal.all().filter('user', users.GetCurrentUser())
  if (opers):
    db.delete(opers)
  
  first = True
  
  lines = _text.split('\n')
  for line in lines:
    arr = line.split('\t')
    if (first):
      first = False
    elif (len(arr) >= 35):
      f29 = 0
      if (arr[29] != ''):
        f29 = int(arr[29])

      f30 = 0
      if (arr[30] != ''):
        f30 = int(arr[30])

      f31 = 0
      if (arr[31] != ''):
        f31 = int(arr[31])

      f32 = 0
      if (arr[32] != ''):
        f32 = int(arr[32])

      f33 = 0
      if (arr[33] != ''):
        f33 = int(arr[33])

      f34 = 0
      if (arr[34] != ''):
        f34 = int(arr[34])

      f_day = str(arr[2]).split('.')
      f02 = datetime.datetime(int(f_day[2]), int(f_day[1]), int(f_day[0]))
      
      f_day = str(arr[3]).split('.')
      f03 = datetime.datetime(int(f_day[2]), int(f_day[1]), int(f_day[0]))
      
      cmnl = Communal(user       = users.GetCurrentUser(), \
                      year       = int(arr[0]), \
                      month      = int(arr[1]), \
                      dCounter   = f02, \
                      dPay       = f03, \
                      tv_tar     = int(arr[4]), \
                      tv_pay     = int(arr[27]), \
                      phone_tar  = int(arr[5]), \
                      phone_pay  = int(arr[28]), \
                      zhirovka   = int(arr[6]), \
                      hot_pay    = f29, \
                      repair_pay = f30, \
                      ZKX_pay    = f31, \
                      el_old     = int(arr[7]), \
                      el_new     = int(arr[8]), \
                      el_tar     = float(str(arr[10]).replace(',', '.')), \
                      el_pay     = f32, \
                      cold_old   = int(arr[12]), \
                      cold_new   = int(arr[13]), \
                      hot_old    = int(arr[14]), \
                      hot_new    = int(arr[15]), \
                      water_tar  = float(str(arr[17]).replace(',', '.')), \
                      water_pay  = f33, \
                      gas_old    = int(arr[19]), \
                      gas_new    = int(arr[20]), \
                      gas_tar    = float(str(arr[22]).replace(',', '.')), \
                      gas_pay    = f34, \
                      penalty    = 0, \
                      prev_per   = 0, \
                      course     = int(arr[25]), \
                      text       = '')
      if cmnl:
        cmnl.put()
  
  return 'done'
