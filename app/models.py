from app import db
import math
import time

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
    #stats_id = db.Column(db.Integer, db.ForeignKey('statistics.id'))
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
            
        return 0
        
    def delete_hours(self):
        # TODO: before delete gather statistics
        #   e.g. when times were best and worst
        #     save somewhere (new table?)
        
        for hour in totals:
            db.session.delete(hour)
            
        db.session.commit()
        
    def getStats(self):
        buy, sell = 0, 0
        buy_hours, sell_hours = [], []
        length = 0
        
        # Get totals
        for hour in self.totals:
            buy += hour.buy_price
            sell += hour.sell_price
            
            buy_hours.insert(length, hour.buy_price)
            sell_hours.insert(length, hour.sell_price)
            
            length += 1
            
        # Day averages
        self.average_buy = buy / 24
        self.average_sell = sell / 24
        
        db.session.add(self)
        db.session.commit()
        
        # Create initial Statistics entry with computed day averages
        stat = Statistics(b_average=self.average_buy, s_average=self.average_sell, stats_agg=self)
        
        stat.standard_deviation(self)
        stat.biggest_difference(buy_hours, sell_hours)
        
        db.session.add(stat)
        db.session.commit()
        
    def __repr__(self):
        return '<Month %r, Day %r, id=%r, avg %r %r>' % ((super(Day, self).month), 
                                                         self.day_number, self.id, 
                                                         (super(Day, self).average_buy), 
                                                         (super(Day, self).average_sell))

class Hours(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    hour_number = db.Column(db.Integer)
    buy_price = db.Column(db.Numeric(precision=2))
    sell_price = db.Column(db.Numeric(precision=2))
    belong_day = db.Column(db.Integer)
    day_id = db.Column(db.Integer, db.ForeignKey('aggregate.id'))
    
    def __repr__(self):
        return '<Time %r:00, id=%r>' % (self.hour_number, self.id)

# TODO:
# Based on previous day or available points for today?
class Predictions(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    right = db.Column(db.Boolean, default=False)
    
    # TODO:
    # If 'buy' the next point should be higher
    # If 'sell' the next point should be lower
    # Just next point or a series of points? 
    
    # Recommend buy or sell
    buy_prediction = db.Column(db.Boolean, default=False)
    sell_prediction = db.Column(db.Boolean, default=False)
    
    # To buy or sell
    #self_type = db.Column(db.String(5))
    
    # One to Many (Predictions to Statistics)
    statistic_data = db.relationship('Statistics', backref="stat_pred", lazy='dynamic')
    
    def predict(self):
        check = Predictions()
        print check.id
        print check.buy_prediction
        
        current_date = 17
        current_month = 12
        # currentDate = time.strftime("%m/%d/%Y")
        
        month = Aggregate.query.filter_by(discriminator='aggregate', month_number=(current_month - 1), year=2015)
        
        if month.first() is not None:
            if month.first().statistics is not None:
                b_avg, s_avg = 0, 0
                b_dev, s_dev = 0, 0
                b_dif, s_dif = 0, 0
                
                count = 0
                for stat in month.first().statistics:
                    b_avg += stat.b_average
                    s_avg += stat.s_average
                    
                    b_dev += stat.b_stnd_dev
                    s_dev += stat.s_stnd_dev
                    
                    b_dif += stat.b_biggest_diff
                    s_dif += stat.s_biggest_diff
                    
                    count += 1
                    
                b_avg =  b_avg / count
                s_avg = s_avg / count
                
                b_dev = b_dev / count
                s_dev = s_dev / count
                
                b_dif = b_dif / count
                s_dif = s_dif / count
                
                if b_dev < 10:
                    if b_dif < 5:
                        self.buy_prediction = True
                        
                        if s_dev < 10:
                            if s_dif < 5:
                                self.sell_prediction = True
                                
        else: 
            day = Day.query.filter_by(month_number=current_month, day_number=current_date)
                
            if day.first().statistics is not None:
                print 'hey'
                stats = day.first().statistics
                
                for stat in stats:
                    self.stat_pred = stat
                    print stat
                    if stat.b_stnd_dev < 10:
                        if stat.b_biggest_diff < 5:
                            self.buy_prediction = True
                            
                            if stat.s_stnd_dev < 10:
                                if stat.s_biggest_diff < 5:
                                    self.sell_prediction = True
                                    
        print self
        db.session.add(self)
        db.session.commit()
        
    def __repr__(self):
        return 'id %r, buy %r, sell %r, %r' % (self.id, self.buy_prediction, self.sell_prediction, self.stat_pred)

# TODO:
# One 'Statistics' for 'buy' and 'sell'?
# For now together
# If separate, need Many to Many relationship with extra table
class Statistics(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    b_biggest_diff = db.Column(db.Float, default=0)
    s_biggest_diff = db.Column(db.Float, default=0)
    b_plateau = db.Column(db.Integer, default=0)
    s_plateau = db.Column(db.Integer, default=0)
    b_average = db.Column(db.Float)
    s_average = db.Column(db.Float)
    
    # How central are the points
    # e.g. how scattered are they
    b_stnd_dev = db.Column(db.Float, default=0)
    s_stnd_dev = db.Column(db.Float, default=0)
    
    # Type (buy or sell), for separate
    # tpe = db.Column(db.String(5))
    
    predict = db.Column(db.Integer, db.ForeignKey('predictions.id'))
    day_id = db.Column(db.Integer, db.ForeignKey('aggregate.id'))
    
    # Compute Standard Deviation on hours
    def standard_deviation(self, day):
        buy, sell = 0, 0
        
        # Compute (value - average) ^ 2
        for hour in day.totals:
            buy += (hour.buy_price - day.average_buy) ** 2
            sell += (hour.sell_price - day.average_sell) ** 2
            
        # Compute standard deviation square root of new averages
        self.b_stnd_dev = math.sqrt(buy / 24)
        self.s_stnd_dev = math.sqrt(sell / 24)
        
    # Calculate the biggest difference between the hours
    def biggest_difference(self, buy_hours, sell_hours):
        b_low, b_high = min(buy_hours), max(buy_hours)
        s_low, s_high = min(sell_hours), max(sell_hours)
        
        self.b_biggest_diff = b_high - b_low
        self.s_biggest_diff = s_high - s_low
        
    def __repr__(self):
        return 'b_average: %r, s_average: %r, b_dev %r, s_dev %r, b_biggest %r, s_biggest %r' % (self.b_average, self.s_average, 
                                                                                                 self.b_stnd_dev, self.s_stnd_dev,
                                                                                                 self.b_biggest_diff, self.s_biggest_diff)
