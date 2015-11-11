from app import db
import unirest
from urllib2 import Request, urlopen, URLError

class Exchanges:

  def buyHour():
    response = unirest.get(http://montanaflynn-bitcoin)

# from urllib2 import Request, urlopen, URLError

# request = Request('http://placekitten.com/')

# try:
#   response = urlopen(request)
#   kittens = response.read()
#   print kittens[559:1000]
# except URLError, e:
#     print 'No kittez. Got an error code:', e

# response = unirest.get("https://montanaflynn-bitcoin-exchange-rate.p.mashape.com/prices/buy?qty=1",
#   headers={
#     "X-Mashape-Key": "HXieJjOkGemshiw8hzl3Iq0Cgd8Ip1gT7JYjsn5myB8JJQ6rBl",
#     "Accept": "text/plain"
#   }
# )