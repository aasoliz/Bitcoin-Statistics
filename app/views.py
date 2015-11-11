from flask import render_template, flash, redirect
from app import app, db
from datetime import datetime
from models import Aggregate, Day, Hours
from bitcoin_api import buyHour, sellHour


@app.route('/')
@app.route('/index')
def index():
  time = datetime.now().hour
  
  hour = Hours(hour_number=time, buy_price=-1, sell_price=-1)
  db.session.add(hour)
  db.session.commit()

  buyHour(hour)
  sellHour(hour)

  hours = Hours.query.all()
    
  return render_template('index.html', title='Home', hours=hours)
