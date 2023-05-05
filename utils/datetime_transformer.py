""" 小工具 """
import pendulum
import datetime

def to_datetime(x):
    try:
        x = pendulum.parse(x)
        x = datetime.datetime(x.year, x.month, x.day)
    except:
        x = None
    return x

def to_date(x):
    try:
        x = pendulum.parse(x).date()
        x = datetime.date(x.year, x.month, x.day)
    except:
        x = None
    return x

def today_todatetime():
    t = datetime.datetime.today()
    t_datetime  = datetime.datetime(t.year, t.month, t.day)
    return t_datetime