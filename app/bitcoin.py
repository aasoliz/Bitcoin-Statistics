from app import db
from config import bitcoin_key
from models import Aggregate, Day, Hours, Predictions
from time import strptime, strftime, localtime
import os
import os.path
import unirest
import json

def creation(date, buy, sell):
    date = strptime(date, '%m/%d/%y %H:%M')
    
    time_h = date.tm_hour
    time_d = date.tm_mday
    time_m = date.tm_mon
    time_y = date.tm_year
      
    complete_month = 0
    complete_day = 0
    
    monthDict={1:'January', 2:'February', 3:'March', 4:'April', 5:'May', 6:'June', 7:'July', 
               8:'August', 9:'September', 10:'October', 11:'November', 12:'December'}
    
    month = Aggregate.query.filter_by(month_number=time_m, year=time_y).first()
    day = Day.query.filter_by(month_number=time_m, day_number=time_d).first()
    
    if month is None:
        # Create Month, Day, Hour
        month = Aggregate(year=time_y, month=monthDict[time_m], month_number=time_m, 
                          average_buy=-1, average_sell=-1)
        
        day = Day(year=time_y, month=monthDict[time_m], month_number=time_m, 
                  average_buy=-1, average_sell=-1, parent_month=month, day_number=time_d)
        
        hour = Hours(hour_number=time_h, buy_price=buy, sell_price=sell, belong_day=time_d, hour=day)
        
        db.session.add(month)
        db.session.add(day)
        db.session.add(hour)
        db.session.commit()
        
    else:
        day = Day.query.filter_by(day_number=time_d, month_id=month.id).first()
        
        if day is None:
            day = Day(year=time_y, month=monthDict[time_m], month_number=time_m, 
                      average_buy=-1, average_sell=-1, parent_month=month, day_number=time_d)
            
            hour = Hours(hour_number=time_h, buy_price=buy, sell_price=sell, belong_day=time_d, hour=day)
            
            db.session.add(day)
            db.session.add(hour)
            db.session.commit()
            
        else:
            hour = Hours.query.filter_by(hour_number=time_h, day_id=day.id).first()
            
            if hour is None:
                hour = Hours(hour_number=time_h, buy_price=buy, sell_price=sell, belong_day=time_d, hour=day)
                
                db.session.add(hour)
                db.session.commit()

    # Enough information to compute day statistics
    if(day.priceDay() is not -1):
        day.getStats()
        
        predict = Predictions(id=1, right=False, buy_prediction=False, sell_prediction=False)
        print predict.id
        predict.predict()
        
    if(month.priceMonth() is not -1):
        month.getStats()
        
        Predictions(right=False, buy_prediction=False, sell_prediction=False).predict()


def consolidate():
    if(os.path.exists('hours.txt')):
        f = open('hours.txt', 'r')
        
        for line in f:
            arr = line.split()
            
            date = arr[0] + ' ' + arr[1]
            buy_price = arr[2]
            sell_price = arr[3]
            
            creation(date, buy_price, sell_price)
            
        f.close()
        
       # os.remove('hours.txt')

def curr(curr, tocurr):
    response = unirest.get("https://montanaflynn-bitcoin-exchange-rate.p.mashape.com/prices/sell?qty=1",
        headers={
            "X-Mashape-Key": bitcoin_key,
            "Accept": "text/plain"
        }
    )

    try:
        curr = curr + '_to_' + tocurr
        return response.body[curr];
    except:
        print('currency exchange not supported')
        return
