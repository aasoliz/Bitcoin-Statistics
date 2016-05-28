from flask import render_template, flash, redirect, url_for
from app import app, db
from models import Aggregate, Day, Hours, Statistics
from bitcoin import consolidate
import json

@app.route('/')
@app.route('/index')
def index():
  consolidate()

  # List of Dictionaries of points for the graph
  prices = [[], []]

  # TODO: fix if month or day comes out to be null
  months = Aggregate.query.filter_by(discriminator='aggregate', month_number=12, year=2015)
  days = Day.query.filter_by(parent_month=months.first(), day_number=17)
  hours = Hours.query.filter_by(day_id=days.first().id)

  # Enough information to compute day statistics
  if(days.first().priceDay() is not -1):
    days.first().getStats()

  # Enough information to compute month statistics
  if(months.first().priceMonth() is not -1):
    months.first().getStats()

  stats = days.first().statistics

  length = len(prices[0])

  # Input hours [(buy) [{hour: #} {price: #}], (sell) [{hour: #} {price: #}]
  for hour in hours:
    prices[0].insert(length, {'hour': str(hour.hour_number), 'price': str(hour.buy_price)})
    prices[1].insert(length, {'hour': str(hour.hour_number), 'price': str(hour.sell_price)})

    length += 1;

  return render_template('index.html', title='Home', data=str(prices), hours=hours, days=days, months=months, stats=stats)
