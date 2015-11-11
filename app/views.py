from flask import render_template, flash, redirect
from app import app, db
from datetime import datetime
from models import Aggregate, Day, Hours
from bitcoin_api import buyHour, sellHour, buyDay, sellDay, buyMonth, sellMonth


@app.route('/')
@app.route('/index')
def index():
  date = datetime.now()

  time_h = date.hour
  time_d = date.day
  time_m = date.month

  print 'checking'
  if Aggregate.query.filter_by(month_number=time_m).first() is None:
    # Create Month
    print 'no month'
    month = Aggregate(month=date.strftime("%B"), month_number=time_m, average_buy=-1, average_sell=-1)
    db.session.add(month)
    db.session.commit()

    if Aggregate.query.filter_by(days.contains(time_d)).first() is None:
      # Create Day

      day = Day(month=date.strftime("%B"), month_number=time_m, average_buy=-1, average_sell=-1, parent_month=time_m, day_number=time_d)
      db.session.add(day)
      db.session.commit()

      if Aggregate.query.filter_by(hour=time_h).first() is None:
        hour = Hours(hour_number=time, buy_price=-1, sell_price=-1, hour=time_h)
        db.session.add(hour)
        db.session.commit()

        buyHour(hour)
        sellHour(hour)

      if(day.totals.count() > 23):
        buyDay(day)
        sellDay(day)
        day.delete_hours()

    if(month.days.count() > 29):
      buyMonth(month)
      sellMonth(month)
      month.delete_days()


  hours = Hours.query.all()
  days = Day.query.all()
  months = Aggregate.query.all()
    
  return render_template('index.html', title='Home', hours=hours)
