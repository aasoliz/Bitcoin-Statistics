from app import app, db
from datetime import datetime
from models import Aggregate, Day, Hours
from bitcoin_api import buyHour, sellHour, buyDay, sellDay, buyMonth, sellMonth

date = datetime.now()

time_h = date.hour
time_d = date.day
time_m = date.month

month = Aggregate.query.filter_by(month_number=time_m).first()

if month is None:
  # Create Month, Day, Hour
  month = Aggregate(month=date.strftime("%B"), month_number=time_m, average_buy=-1, average_sell=-1)
  day = Day(month=date.strftime("%B"), month_number=time_m, average_buy=-1, average_sell=-1, parent_month=month, day_number=time_d)
  hour = Hours(hour_number=time_h, buy_price=-1, sell_price=-1, hour=day)


  db.session.add(month)
  db.session.add(day)
  db.session.add(hour)
  db.session.commit()

  buyHour(hour)
  sellHour(hour)

elif month:
  day = Day.query.filter_by(day_number=time_d, month_id=month.id).first()

  if day is None:
    day = Day(month=date.strftime("%B"), month_number=time_m, average_buy=-1, average_sell=-1, parent_month=month, day_number=time_d)
    hour = Hours(hour_number=time_h, buy_price=-1, sell_price=-1, day_id=day.id)

    db.session.add(day)
    db.session.add(hour)
    db.session.commit()

    buyHour(hour)
    sellHour(hour)

  elif day:
    hour = Hours.query.filter_by(hour_number=time_h, day_id=day.id).first()

    if hour is None:
      hour = Hours(hour_number=time_h, buy_price=-1, sell_price=-1, day_id=day.id)

      db.session.add(hour)
      db.session.commit()

      buyHour(hour)
      sellHour(hour)