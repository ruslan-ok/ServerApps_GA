# coding=utf-8
import datetime
import string

from google.appengine.api import users
from google.appengine.ext import db

"""--------------------------------------------------------------"""
"""                         GARAGE info                          """
"""--------------------------------------------------------------"""


status = ''


def summary(a_mode):
  if (a_mode == 1):
    return u''
  else:
    ret = 0.;
    opers = Garage.all().filter('user', users.GetCurrentUser())
    for g in opers:
      ret = ret + g.summa()
    return u'<span style="color:yellow">' + str(ret) + u'</span>$'

"""--------------------------------------------------------------"""
"""                         GARAGE                               """
"""--------------------------------------------------------------"""

class Garage(db.Model):
  pid       = db.IntegerProperty(required=True)
  user      = db.UserProperty(required=True)
  date      = db.DateTimeProperty(required=True, auto_now_add=True)
  kol       = db.FloatProperty()
  price     = db.IntegerProperty()
  course    = db.IntegerProperty()
  usd       = db.IntegerProperty()
  kontr     = db.StringProperty()
  text      = db.StringProperty()

  def s_date(self):
    return str(self.date.day) + '.' + str(self.date.month) + '.' + str(self.date.year)

  def summa(self):
    if (self.course == 0):
      return round(self.usd, 2)
    else:
      return round(self.usd + ((self.kol * self.price) / self.course), 2)



def insert(i_date, i_kol, i_price, i_course, i_usd, i_kontr, i_text):
  maxnum = 1
  last = Garage.all().filter('user', users.GetCurrentUser()).order('-pid').get()
  if last:
    maxnum = last.pid + 1
  gar = Garage(pid    = maxnum, \
               user   = users.GetCurrentUser(), \
               date   = i_date, \
               kol    = i_kol, \
               price  = i_price, \
               course = i_course, \
               usd    = i_usd, \
               kontr  = i_kontr, \
               text   = i_text)
  if gar:
    gar.put()

def update(i_pid, i_date, i_kol, i_price, i_course, i_usd, i_kontr, i_text):
  gar = Garage.all().filter('user', users.GetCurrentUser()).filter('pid', i_pid).get()
  if gar:
    gar.date   = i_date
    gar.kol    = i_kol
    gar.price  = i_price
    gar.course = i_course
    gar.usd    = i_usd
    gar.kontr  = i_kontr
    gar.text   = i_text
    gar.put()

def delete(i_pid):
  gar = Garage.all().filter('user', users.GetCurrentUser()).filter('pid', i_pid).get()
  if gar:
    gar.delete()

def get(i_pid):
  gar = Garage.all().filter('user', users.GetCurrentUser()).filter('pid', i_pid).get()
  if gar:
    return gar
  else:
    # Инициализация полей новой записи
    last_course = 0
    last_kontr = ''
    last = Garage.all().filter('user', users.GetCurrentUser()).order('-date').order('-pid').get()
    if last:
      last_course = last.course
      last_kontr  = last.kontr

    return Garage(pid    = 0, \
                  user   = users.GetCurrentUser(), \
                  date   = datetime.datetime.now(), \
                  kol    = 1., \
                  price  = 0, \
                  course = last_course, \
                  usd    = 0, \
                  kontr  = last_kontr, \
                  text   = '')

def all():
  return Garage.all().filter('user', users.GetCurrentUser()).order('-date').order('-pid')

def import_from_file(_text):

  opers = Garage.all().filter('user', users.GetCurrentUser())
  if (opers):
    db.delete(opers)
  
  ret = 1
  last_dat = datetime.datetime.now()
  last_org = ''

  lines = _text.split('\n')
  for line in lines:
    arr = line.split('\t')
    if (len(arr) >= 9):
      f_dat = arr[0]
      f_kol = arr[1]
      f_prc = arr[2]
      f_byr = arr[3]
      f_usd = arr[4]
      f_cur = arr[5]
      f_tot = arr[6]
      f_org = arr[7]
      f_txt = arr[8]
    
      if (f_dat == ''):
        i_dat = last_dat
      else:
        f_day = str(f_dat).split('.')
        i_dat = datetime.datetime(int(f_day[2]), int(f_day[1]), int(f_day[0]))
        last_dat = i_dat
      
      i_kol = 0.
      if (f_kol != ''):
        i_kol = float(f_kol.replace(' ', ''))
      
      i_prc = 0
      if (f_prc != ''):
        i_prc = int(f_prc.replace(' ', ''))
      
      i_byr = 0
      if (f_byr != ''):
        i_byr = int(f_byr.replace(' ', ''))

      if (i_prc == 0) or (i_kol == 0.):
        i_kol = 1.
        i_prc = i_byr
      
      i_usd = 0
      if (f_usd != ''):
        i_usd = int(f_usd.replace(' ', ''))
      
      i_cur = 0
      if (f_cur != ''):
        i_cur = int(f_cur.replace(' ', ''))
      
      i_tot = 0.
      if (f_tot != ''):
        i_tot = float(f_tot.replace(' ', '').replace(',', '.'))
      
      if (f_org == ''):
        f_org = last_org
      else:
        last_org = f_org

      u_org = unicode(f_org, 'utf-8')
      u_txt = unicode(f_txt, 'utf-8')
    
      ret += 1
    
      if (i_tot != 0.):
        gar = Garage(pid    = ret,   \
                     user   = users.GetCurrentUser(),   \
                     date   = i_dat, \
                     kol    = i_kol, \
                     price  = i_prc, \
                     course = i_cur, \
                     usd    = i_usd, \
                     kontr  = u_org, \
                     text   = u_txt)
        gar.put()



def del_all():

  opers = Garage.all().filter('user', users.GetCurrentUser())
  if (opers):
    db.delete(opers)
  
