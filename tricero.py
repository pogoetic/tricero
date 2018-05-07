import requests, json, sqlite3, os
from creds import CoinAPIKey
from cryptos import cryptolist

verbose = 1
headers = {'X-CoinAPI-Key' : CoinAPIKey}
dir_path = os.path.dirname(os.path.realpath(__file__))
dbpathname = '/tricero.db'

def echo(msg, verbosity=verbose):
    if verbosity == 1:
        print msg 
    else:
        return None

def dbprocess(path):
    try:
        echo(msg='Loading DB...',verbosity=1)
        con = sqlite3.connect(str(path)+dbpathname) #connect to existing or create new if does not exist
        cur = con.cursor()
        cur.execute('CREATE TABLE daily_trades(time_open datetime, time_close datetime, time_start datetime, time_end datetime, trades_count bigint, volume_traded decimal(20,10), price_open decimal(20,10), price_high decimal(20,10), price_low decimal(20,10), price_close decimal(20,10))')
        cur.execute('CREATE INDEX IDX_time ON daily_trades (time_start, time_end)')
        con.commit()
    except sqlite3.Error, e:
    	echo(msg="Error {}:".format(e.args[0]),verbosity=1)
        sys.exit(1)
    finally:
        if con:
            con.close()
            
#Create or Connect to existing Sqlite DB
if not os.path.isfile(str(dir_path)+dbpathname):
	con=dbprocess(path=dir_path)

con = sqlite3.connect(str(dir_path)+dbpathname) #connect to existing sqlite db
cur = con.cursor()

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
period_id='1DAY'
time_start='2016-01-01T00:00:00'
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

#load data into db
#cur.execute("Insert Into daily_trades(time_open,time_close,time_start,time_end,trades_count,volume_traded,price_open,price_high,price_low,price_close) values('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}')".format()
#con.commit()

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