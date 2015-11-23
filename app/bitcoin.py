from app import db
from config import bitcoin_key
from models import Aggregate, Day, Hours
from time import strptime, strftime, localtime
import os
import unirest
import json

def buyDay(day):
  count = day.totals.count()
  if(count < 24):
    return -1

  buy = 0
  for hour in day.totals:
    buy += hour.buy_price

  day.average_buy = buy/24
  db.session.add(day)
  db.session.commit()

  return 0

def sellDay(day):
  count = day.totals.count()
  if(count < 24):
    return -1

  sell = 0
  for hour in day.totals:
    sell += hour.sell_price

  day.average_sell = sell/24
  db.session.add(day)
  db.session.commit()

  return 0

def buyMonth(month):
  count = month.days.count()
  if(count < 30):
    return -1

  buy = 0
  for day in month.days:
    buy += day.average_buy

  month.average_buy = buy/30
  db.session.add(month)
  db.session.commit()

  return 0

def sellMonth(month):
  count = month.days.count()
  if(count < 30):
    return -1

  sell = 0
  for day in month.days:
    sell += day.average_sell

  month.average_sell = sell/30
  db.session.add(month)
  db.session.commit()

  return 0

def creation(date, buy, sell):
  date = strptime(date, '%m/%d/%y %H:%M')
  print("%r" % date)

  time_h = date.tm_hour
  time_d = date.tm_mday
  time_m = date.tm_mon
  complete_month = 0
  complete_day = 0

  monthDict={1:'Jan', 2:'Feb', 3:'Mar', 4:'Apr', 5:'May', 6:'Jun', 7:'Jul', 8:'Aug', 9:'Sep', 10:'Oct', 11:'Nov', 12:'Dec'}

  month = Aggregate.query.filter_by(month_number=time_m).first()
  day = Day.query.filter_by(month_number=time_m).first()

  if month is None:
    # Create Month, Day, Hour
    month = Aggregate(month=monthDict[time_m], month_number=time_m, average_buy=-1, average_sell=-1)
    day = Day(month=monthDict[time_m], month_number=time_m, average_buy=-1, average_sell=-1, parent_month=month, day_number=time_d)
    hour = Hours(hour_number=time_h, buy_price=buy, sell_price=sell, hour=day)

    db.session.add(month)
    db.session.add(day)
    db.session.add(hour)
    db.session.commit()

    complete_month = buyMonth(month)
    sellMonth(month)

  else:
    day = Day.query.filter_by(day_number=time_d, month_id=month.id).first()

    if day is None:
      day = Day(month=monthDict[time_m], month_number=time_m, average_buy=-1, average_sell=-1, parent_month=month, day_number=time_d)
      hour = Hours(hour_number=time_h, buy_price=buy, sell_price=sell, day_id=day.id)

      db.session.add(day)
      db.session.add(hour)
      db.session.commit()

      complete_day = buyDay(day)
      sellDay(day)

    else:
      hour = Hours.query.filter_by(hour_number=time_h, day_id=day.id).first()

      if hour is None:
        hour = Hours(hour_number=time_h, buy_price=buy, sell_price=sell, day_id=day.id)

        db.session.add(hour)
        db.session.commit()

  # if(complete_day is not -1):
  #   day.delete_hours()

  # if(complete_month is not -1):
  #   month.delete_day()

def consolidate():
  f = open('hours.txt', 'r')

  for line in f:
    arr = line.split()

    date = arr[0] + ' ' + arr[1]
    buy_price = arr[2]
    sell_price = arr[3]

    creation(date, buy_price, sell_price)

  f.close()

  os.remove('hours.txt')

def curr(curr, tocurr):
  response = unirest.get("https://montanaflynn-bitcoin-exchange-rate.p.mashape.com/prices/sell?qty=1",
    headers={
      "X-Mashape-Key": bitcoin_key,
      "Accept": "text/plain"
    }
  )

  try:
    curr = curr + '_to_' + tocurr
    return response.body[curr];
  except:
    print('currency exchange not supported')
    return