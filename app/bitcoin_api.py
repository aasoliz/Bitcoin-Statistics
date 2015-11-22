from app import db
from config import bitcoin_key
import unirest
import json

def buyDay(day):
    buy = 0
    for hour in day.totals:
      buy += hour.buy_price

    day.average_buy = buy/24
    db.session.add(day)
    db.session.commit()

def sellDay(day):
  sell = 0
  for hour in day.totals:
    sell += hour.sell_price

  day.average_sell = sell/24
  db.session.add(day)
  db.session.commit()

def buyMonth(month):
  count = days.count()
  if(count < 30):
    return -1

  buy = 0
  for day in days:
    buy += day.average_buy

  month.average_buy = buy/30
  db.session.add(month)
  db.session.commit()

def sellMonth(month):
  count = days.count()
  if(count < 30):
    return -1

  sell = 0
  for day in days:
    sell += day.average_sell

  month.average_sell = sell/30
  db.session.add(month)
  db.session.commit()

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