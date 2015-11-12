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

  print "%s" % type(time_h)

  month = Aggregate.query.filter_by(month_number=time_m).first()

  if month is None:
    # Create Month, Day, Hour
    month = Aggregate(month=date.strftime("%B"), month_number=time_m, average_buy=-1, average_sell=-1)
    day = Day(month=date.strftime("%B"), month_number=time_m, average_buy=-1, average_sell=-1, parent_month=month, day_number=time_d)
    hour = Hours(hour_number=time_h, buy_price=-1, sell_price=-1)

    db.session.add(month)
    db.session.add(day)
    db.session.add(hour)
    db.session.commit()

    buyHour(hour)
    sellHour(hour)

  if month:
    day = Day.query.filter_by(day_number=time_d, month_id=month.id).first()
    print "hadysdf %r" % day

    if day is None:
      day = Day(month=date.strftime("%B"), month_number=time_m, average_buy=-1, average_sell=-1, parent_month=month, day_number=time_d)
      hour = Hours(hour_number=time_h, buy_price=-1, sell_price=-1)

      db.session.add(day)
      db.session.add(hour)
      db.session.commit()

      buyHour(hour)
      sellHour(hour)

    if day:
      hour = Hours.query.filter_by(hour_number=time_h).first()
      print "hourasdf %r ajkdfl %r jkasdljf %r" % (hour, day.id, time_h)

      if hour is None:
        hour = Hours(hour_number=time_h, buy_price=-1, sell_price=-1)

        db.session.add(hour)
        db.session.commit()

        buyHour(hour)
        sellHour(hour)

  months = Aggregate.query.filter_by(discriminator='aggregate')

  hours = Hours.query.all()
  print "hours %r" % hours

  days = Day.query.all()
  print "days %r" % days

  print "months %r" % months

  return render_template('index.html', title='Home', hours=hours, days=days, months=months)
