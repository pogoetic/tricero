import requests
from creds import CoinAPIKey

url = 'https://rest.coinapi.io/v1/ohlcv/BITSTAMP_SPOT_BTC_USD/history?period_id=1MIN&time_start=2016-01-01T00:00:00'
headers = {'X-CoinAPI-Key' : CoinAPIKey}
response = requests.get(url, headers=headers)