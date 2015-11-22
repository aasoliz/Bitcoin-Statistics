from bitcoin_api import buyHour, sellHour
from datetime import datetime

date = datetime.now()
key = 'HXieJjOkGemshiw8hzl3Iq0Cgd8Ip1gT7JYjsn5myB8JJQ6rBl'

buy_price = buyHour(key)
sell_price = sellHour(key)

f = open('hours.txt', 'a')

f.write(date + "\n");
f.write(buy_price + "\n")
f.write(sell_price + "\n")

f.close()