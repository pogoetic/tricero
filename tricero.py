import requests, json
from creds import CoinAPIKey
from cryptos import cryptolist

headers = {'X-CoinAPI-Key' : CoinAPIKey}

#get valid symbols
URI = 'https://rest.coinapi.io/v1/symbols'
filter_symbol_id = 'BINANCE,BITTREX'
url = '{0}?filter_symbol_id={1}'.format(URI,filter_symbol_id)
r = requests.get(url, headers=headers)
resp = r.json()
apilimit = r.headers['X-RateLimit-Remaining']

#return only desired symbols
symbols = [x['symbol_id'] for x in resp if x['asset_id_base'] in cryptolist and x['asset_id_quote'] in ['USDT']]

#query historical OHLCV data (all times are in UTC)
symbol_id = symbols[0] #for now we force just 1 symbol_id
URI = 'https://rest.coinapi.io/v1/ohlcv/'
period_id='1HRS'
time_start='2018-05-06T00:00:00'
url = '{0}/{1}/history?period_id={2}&time_start={3}'.format(URI,symbol_id,period_id,time_start)
if apilimit > 1:
	r = requests.get(url, headers=headers)
	apilimit = r.headers['X-RateLimit-Remaining']
else:
	print 'CoinAPI rate limit reached'

print '\nData for symbol_id: {}'.format(symbol_id)
print 'Data rows: {}'.format(len(r.json()))
print json.dumps(r.json(), indent=4)


print '\n API calls remaining: {}'.format(apilimit)




"""Notes: 

1. If sqlite DB does not exist, create DB
2. Import past 2Yr of market data 
3. market data to import:
	- Open, High, Low, Close, Volume (OHLCV) timeseries data
	- 




Thoughts: 
- Try 1SEC, 1MIN, 1HRS, and 1DAY granularities and see if the model improves
- Currently USDT is our 'market', in future use BTC and ETH markets as well

"""