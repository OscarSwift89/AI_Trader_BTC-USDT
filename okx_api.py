import ccxt
import pandas as pd
from datetime import datetime
from config import API_KEY, SECRET_KEY, PASSPHRASE

class OKXAPI:
    def __init__(self):
        self.exchange = ccxt.okx({
            'apiKey': API_KEY,
            'secret': SECRET_KEY,
            'password': PASSPHRASE,
            'enableRateLimit': True
        })
        
    def get_klines(self, symbol='BTC/USDT', timeframe='1h', limit=1000):
        """Get historical kline data"""
        try:
            # Fetch OHLCV data
            ohlcv = self.exchange.fetch_ohlcv(symbol, timeframe, limit=limit)
            
            # Convert to DataFrame
            df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
            df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
            
            # Format data to match the expected structure
            data = {
                'data': df.values.tolist()
            }
            
            return data
            
        except Exception as e:
            print(f"Error fetching kline data: {e}")
            return None
    
    def get_account_balance(self):
        """获取账户余额"""
        endpoint = '/api/v5/account/balance'
        url = self.base_url + endpoint
        headers = self._get_headers('GET', endpoint)
        response = requests.get(url, headers=headers)
        return response.json()
    
    def place_order(self, side, size, price=None):
        """下单"""
        endpoint = '/api/v5/trade/order'
        url = self.base_url + endpoint
        
        order_data = {
            'instId': SYMBOL,
            'tdMode': 'cross',
            'side': side,
            'ordType': 'market' if price is None else 'limit',
            'sz': str(size)
        }
        
        if price is not None:
            order_data['px'] = str(price)
            
        headers = self._get_headers('POST', endpoint, str(order_data))
        response = requests.post(url, json=order_data, headers=headers)
        return response.json()
    
    def get_order_status(self, order_id):
        """获取订单状态"""
        endpoint = f'/api/v5/trade/order?instId={SYMBOL}&ordId={order_id}'
        url = self.base_url + endpoint
        headers = self._get_headers('GET', endpoint)
        response = requests.get(url, headers=headers)
        return response.json() 