#!venv/bin/python

from datetime import datetime
import unirest
import json

def buyHour(key):
  response = unirest.get("https://montanaflynn-bitcoin-exchange-rate.p.mashape.com/prices/buy?qty=1",
    headers={
      "X-Mashape-Key": key,
      "Accept": "text/plain"
    }
  )

  return float(response.body['total']['amount'])

def sellHour(key):
  response = unirest.get("https://montanaflynn-bitcoin-exchange-rate.p.mashape.com/prices/sell?qty=1",
    headers={
      "X-Mashape-Key": key,
      "Accept": "text/plain"
    }
  )

  return float(response.body['total']['amount']);

date = datetime.now()
key = 'HXieJjOkGemshiw8hzl3Iq0Cgd8Ip1gT7JYjsn5myB8JJQ6rBl'

buy_price = buyHour(key)
sell_price = sellHour(key)

f = open('hours.txt', 'a')

f.write(date.strftime('%m/%d/%y %H:%M') + " ")
f.write(str(buy_price) + " ")
f.write(str(sell_price) + "\n")

f.close()