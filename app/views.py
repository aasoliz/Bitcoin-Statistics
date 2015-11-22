from flask import render_template, flash, redirect
from app import app, db
from models import Aggregate, Day, Hours

@app.route('/')
@app.route('/index')
def index():

  months = Aggregate.query.filter_by(discriminator='aggregate')
  days = Day.query.filter_by(discriminator='days')
  hours = Hours.query.all()

  return render_template('index.html', title='Home', hours=hours, days=days, months=months)
