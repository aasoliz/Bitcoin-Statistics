from app import db

class Aggregate(db.Model):
  __tablename__ = 'aggregate'

  discriminator = db.Column('type', db.String(50))
  __mapper_args__ = {'polymorphic_identity': 'aggregate',
    'polymorphic_on': discriminator
  }

  id = db.Column(db.Integer, primary_key=True)
  year = db.Column(db.Integer, index=True)
  month = db.Column(db.String(50), index=True)
  month_number = db.Column(db.Integer, index=True)
  average_buy = db.Column(db.Numeric(precision=2))
  average_sell = db.Column(db.Numeric(precision=2))

  # Many to One with itself (essentially aggregate to day)
  month_id = db.Column(db.Integer, db.ForeignKey('aggregate.id'))
  days = db.relationship('Aggregate', backref=db.backref('parent_month', remote_side=[id]))

  # Many to One (Statistics to Aggregate)
  stats_id = db.Column(db.Integer, db.ForeignKey('statistics.id'))
  statistics = db.relationship('Statistics', backref='stats_agg')

  def priceMonth(self):
    count = 0
    for day in self.days:
      count += 1

    if(count < 30):
      return -1

    buy = 0
    sell = 0
    for day in self.days:
      buy += day.average_buy
      sell += day.average_sell

    self.average_buy = buy / 30
    self.average_sell = buy / 30
    
    db.session.add(self)
    db.session.commit()

    return 0

  def delete_day(self):
    # TODO: before delete gather statistics
    #   e.g. when times were best and worst
    #     save somewhere (new table?)

    for day in days:
      db.session.delete(day)

    db.session.commit()

  def __repr__(self):
      return '<Month  %r, id=%r>' % (self.month, self.id)

class Day(Aggregate):
  __mapper_args__ = {'polymorphic_identity': 'days'}

  day_number = db.Column(db.Integer)

  totals = db.relationship('Hours', backref='hour', lazy='dynamic')

  def priceDay(self):
    count = 0
    for total in self.totals:
      count += 1

    if(count < 24):
      return -1

    buy = 0
    sell = 0
    for hour in self.totals:
      buy += hour.buy_price
      sell += hour.sell_price

    self.average_buy = buy / 24
    self.average_sell = sell / 24

    db.session.add(self)
    db.session.commit()

    return 0

  def delete_hours(self):
    # TODO: before delete gather statistics
    #   e.g. when times were best and worst
    #     save somewhere (new table?)

    for hour in totals:
      db.session.delete(hour)

    db.session.commit()

  def __repr__(self):
    return '<Month %r, Day %r, id=%r, avg %r %r>' % ((super(Day, self).month), self.day_number, self.id, (super(Day, self).average_buy), (super(Day, self).average_sell))


class Hours(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  hour_number = db.Column(db.Integer)
  buy_price = db.Column(db.Numeric(precision=2))
  sell_price = db.Column(db.Numeric(precision=2))
  belong_day = db.Column(db.Integer)

  day_id = db.Column(db.Integer, db.ForeignKey('aggregate.id'))
  stat_id = db.Column(db.Integer, db.ForeignKey('statistics.id'))
  
  def __repr__(self):
    return '<Time %r:00, id=%r>' % (self.hour_number, self.id)

class Predictions(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  right = db.Column(db.Boolean, default=False)
  
  # TODO:
  # If 'buy' the next point should be higher
  # If 'sell' the next point should be lower
  # Just next point or a series of points? 
  
  # Recommend buy or sell
  prediction = db.Column(db.String(50))
  
  # To buy or sell
  prediction_type = db.Column(db.String(5))

  # One to Many (Predictions to Statistics)
  statistic_data = db.relationship('Statistics', backref="stat_pred", lazy='dynamic')


# TODO:
# One 'Statistics' for 'buy' and 'sell'?
# For now together
# If separate, need Many to Many relationship with extra table
class Statistics(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  b_biggest_diff = db.Column(db.Integer)
  s_biggest_diff = db.Column(db.Integer)
  b_plateau = db.Column(db.Integer, default=0)
  s_plateau = db.Column(db.Integer, default=0)
  b_average = db.Column(db.Float)
  s_average = db.Column(db.Float)

  # How central are the points
  # e.g. how scattered are they
  b_stnd_dev = db.Column(db.Float)
  s_stnd_dev = db.Column(db.Float)

  # Type (buy or sell), for separate
  # tpe = db.Column(db.String(5))

  predict = db.Column(db.Integer, db.ForeignKey('predictions.id'))
  
  # Many to One (Statistics to Hours)
  hour = db.relationship('Hours', backref=('stats_hr'), lazy='dynamic')