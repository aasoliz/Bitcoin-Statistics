from flask import render_template, flash, redirect, url_for
from app import app, db
from models import Aggregate, Day, Hours
from bitcoin import consolidate
import json

@app.route('/')
@app.route('/index')
def index():
  consolidate()

  # Dictionary of points for the graph
  buy = {}
  sell = {}

  months = Aggregate.query.filter_by(discriminator='aggregate')
  days = Day.query.filter_by(discriminator='days')
  hours = Hours.query.all()

  # Input hours into 'points' {hour} {tuple(buy, sell)}
  for hour in hours:
    if not buy.has_key(hour.hour_number):
      buy[str(hour.hour_number)] = str(hour.buy_price)
      sell[hour.hour_number] = str(hour.sell_price)

  dumps = json.dumps(buy)

  print buy
  print type(buy)
  print str(buy)
  print type(str(buy))
  print dumps
  print type(dumps)

  return render_template('index.html', title='Home', data=str(buy), hours=hours, days=days, months=months)
