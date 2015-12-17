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
  points = {}

  months = Aggregate.query.filter_by(discriminator='aggregate')
  days = Day.query.filter_by(discriminator='days')
  hours = Hours.query.all()

  # Input hours into 'points' {hour} {tuple(buy, sell)}
  for hour in hours:
    if not points.has_key(hour.hour_number):
      points[hour.hour_number] = (str(hour.buy_price), str(hour.sell_price))

  dumps = json.dumps(points)

  print dumps

  return render_template('index.html', title='Home', data=dumps, hours=hours, days=days, months=months)
