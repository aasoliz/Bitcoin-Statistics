from flask import render_template, flash, redirect
from app import app, db
from models import Aggregate, Day, Hours


@app.route('/')
@app.route('/index')
def index():
  hour = Hours(hour_number=1, buy_price=244, sell_price=43)
  db.session.add(hour)
  db.session.commit()

  hours = Hours.query.all()
    
  return render_template('index.html', title='Home', hours=hours)
