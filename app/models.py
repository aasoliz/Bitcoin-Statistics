from app import db


class Aggregate(db.Model):
    __tablename__ = 'aggregate'

    discriminator = db.Column('type', db.String(50))
    __mapper_args__ = {'polymorphic_identity': 'aggregate',
      'polymorphic_on': discriminator
    }

    id = db.Column(db.Integer, primary_key=True)
    month = db.Column(db.String(50), index=True, unique=True)
    average_buy = db.Column(db.Numeric(precision=2))
    average_sell = db.Column(db.Numeric(precision=2))

    # Many to One with itself (essentially aggregate to day)
    month_id = db.Column(db.Integer, db.ForeignKey('aggregate.id'))
    days = db.relationship('Aggregate', backref=db.backref('parent_month', remote_side=[id]))

    totals = db.relationship('Hours', backref='hour', lazy='dynamic')

    def month_buy(self):
      count = days.count()
      if(count < 30):
        return -1

      for day in days:
        buy += day.average_buy

      return buy/ count

    def month_sell(self):
      count = days.count()
      if(count < 30):
        return -1

      for day in days:
        sell = day.average_sell

      return sell/count

    def __repr__(self):
        return '<User %r>' % (self.month)

class Day(Aggregate):
  __mapper_args__ = {'polymorphic_identity': 'days'}

  day_number = db.Column(db.Integer)

  def __repr__(self):
    return '<Month %r, Day %r>' % ((super(Day, self).month), day_number)


class Hours(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    hour_number = db.Column(db.Integer)
    buy_price = db.Column(db.Numeric(precision=2))
    sell_price = db.Column(db.Numeric(precision=2))

    day_id = db.Column(db.Integer, db.ForeignKey('aggregate.id'))

    def __repr__(self):
        return '<Time %r:00>' % (self.hour_number)
