from flask import render_template, flash, redirect
from app import app, db

@app.route('/')
@app.route('/index')
def index():

  months = Aggregate.query.filter_by(discriminator='aggregate')
  days = Day.query.filter_by(day_number=time_d, month_id=month.id)
  hours = Hours.query.filter_by(hour_number=time_h, day_id=day.id)

  return render_template('index.html', title='Home', hours=hours, days=days, months=months)
