import time
import hmac
import base64
import hashlib
import requests
from config import API_KEY, SECRET_KEY, PASSPHRASE, SYMBOL

class OKXAPI:
    def __init__(self):
        self.api_key = API_KEY
        self.secret_key = SECRET_KEY
        self.passphrase = PASSPHRASE
        self.base_url = 'https://www.okx.com'
        
    def _get_timestamp(self):
        return str(int(time.time() * 1000))
    
    def _get_signature(self, timestamp, method, request_path, body=''):
        message = timestamp + method + request_path + body
        mac = hmac.new(bytes(self.secret_key, encoding='utf8'), 
                      bytes(message, encoding='utf-8'), 
                      digestmod='sha256')
        return base64.b64encode(mac.digest()).decode()
    
    def _get_headers(self, method, request_path, body=''):
        timestamp = self._get_timestamp()
        signature = self._get_signature(timestamp, method, request_path, body)
        return {
            'OK-ACCESS-KEY': self.api_key,
            'OK-ACCESS-SIGN': signature,
            'OK-ACCESS-TIMESTAMP': timestamp,
            'OK-ACCESS-PASSPHRASE': self.passphrase,
            'Content-Type': 'application/json'
        }
    
    def get_klines(self, timeframe='1h', limit=100):
        """获取K线数据"""
        endpoint = f'/api/v5/market/candles'
        params = {
            'instId': SYMBOL,
            'bar': timeframe,
            'limit': limit
        }
        url = self.base_url + endpoint
        response = requests.get(url, params=params)
        return response.json()
    
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