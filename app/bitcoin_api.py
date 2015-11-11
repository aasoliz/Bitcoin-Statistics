from app import db
from config import bitcoin_key
import unirest
import json

def buyHour(hour):
  response = unirest.get("https://montanaflynn-bitcoin-exchange-rate.p.mashape.com/prices/buy?qty=1",
    headers={
      "X-Mashape-Key": bitcoin_key,
      "Accept": "text/plain"
    }
  )

  hour.buy_price = float(response.body['total']['amount']);
  db.session.add(hour)
  db.session.commit()

def sellHour(hour):
  response = unirest.get("https://montanaflynn-bitcoin-exchange-rate.p.mashape.com/prices/sell?qty=1",
    headers={
      "X-Mashape-Key": bitcoin_key,
      "Accept": "text/plain"
    }
  )

  hour.sell_price = float(response.body['total']['amount']);
  db.session.add(hour)
  db.session.commit()

def curr(curr, tocurr):
  response = unirest.get("https://montanaflynn-bitcoin-exchange-rate.p.mashape.com/prices/sell?qty=1",
    headers={
      "X-Mashape-Key": bitcoin_key,
      "Accept": "text/plain"
    }
  )

  tags = json.load(response)

  try:
    curr = curr + '_to_' + tocurr
    return tags[curr];
  except:
    print('currency exchange not supported')
    return