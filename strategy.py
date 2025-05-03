import pandas as pd
import numpy as np
from ai_models import AIModels
from config import (
    STOP_LOSS_PCT, TAKE_PROFIT_PCT, MAX_DRAWDOWN_PCT,
    RSI_PERIOD, RSI_OVERBOUGHT, RSI_OVERSOLD,
    MACD_FAST, MACD_SLOW, MACD_SIGNAL,
    BB_PERIOD, BB_STD, MA_PERIOD
)

class TradingStrategy:
    def __init__(self):
        self.ai_models = AIModels()
        self.position = 0  # 0: no position, 1: long, -1: short
        self.entry_price = 0
        self.stop_loss = 0
        self.take_profit = 0
        self.max_drawdown = 0
        self.trades = []
        
    def calculate_indicators(self, df):
        """Calculate technical indicators"""
        # Create a copy of the dataframe
        df = df.copy()
        
        # RSI
        delta = df['close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=RSI_PERIOD).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=RSI_PERIOD).mean()
        rs = gain / loss
        df.loc[:, 'rsi'] = 100 - (100 / (1 + rs))
        
        # MACD
        exp1 = df['close'].ewm(span=MACD_FAST, adjust=False).mean()
        exp2 = df['close'].ewm(span=MACD_SLOW, adjust=False).mean()
        df.loc[:, 'macd'] = exp1 - exp2
        df.loc[:, 'macd_signal'] = df['macd'].ewm(span=MACD_SIGNAL, adjust=False).mean()
        df.loc[:, 'macd_hist'] = df['macd'] - df['macd_signal']
        
        # Bollinger Bands
        df.loc[:, 'bb_middle'] = df['close'].rolling(window=BB_PERIOD).mean()
        df.loc[:, 'bb_std'] = df['close'].rolling(window=BB_PERIOD).std()
        df.loc[:, 'bb_upper'] = df['bb_middle'] + (df['bb_std'] * BB_STD)
        df.loc[:, 'bb_lower'] = df['bb_middle'] - (df['bb_std'] * BB_STD)
        
        # Moving Average
        df.loc[:, 'ma'] = df['close'].rolling(window=MA_PERIOD).mean()
        
        return df
        
    def generate_signals(self, df):
        """Generate trading signals"""
        df = df.copy()
        
        # RSI signals
        rsi_signal = np.where(df['rsi'] > RSI_OVERBOUGHT, -1,
                            np.where(df['rsi'] < RSI_OVERSOLD, 1, 0))
        
        # MACD signals
        macd_signal = np.where(df['macd'] > df['macd_signal'], 1,
                             np.where(df['macd'] < df['macd_signal'], -1, 0))
        
        # Bollinger Bands signals
        bb_signal = np.where(df['close'] > df['bb_upper'], -1,
                           np.where(df['close'] < df['bb_lower'], 1, 0))
        
        # Moving Average signals
        ma_signal = np.where(df['close'] > df['ma'], 1,
                           np.where(df['close'] < df['ma'], -1, 0))
        
        # Combine signals with weights
        signals = (
            rsi_signal * 0.3 +
            macd_signal * 0.3 +
            bb_signal * 0.2 +
            ma_signal * 0.2
        )
        
        # Normalize to range [-2, 2] for stronger signals
        signals = signals * 2
        
        # Convert to pandas Series
        signals = pd.Series(signals, index=df.index)
        
        return signals
        
    def train_ai_models(self, df):
        """Train AI models"""
        df = self.calculate_indicators(df)
        accuracy = self.ai_models.train_random_forest(df)
        print(f"AI model training accuracy: {accuracy:.2%}")
        
    def get_signal(self, df):
        """Get trading signal"""
        df = self.calculate_indicators(df)
        tech_signal = self.generate_signals(df).iloc[-1]
        if tech_signal > 0.7:
            return 1  # Buy signal
        elif tech_signal < -0.7:
            return -1  # Sell signal
        else:
            return 0  # Hold
            
    def update_position(self, price, signal):
        """Update position based on signal"""
        if self.position == 0:  # No position
            if signal == 1:  # Buy signal
                self.position = 1
                self.entry_price = price
                self.stop_loss = price * (1 - STOP_LOSS_PCT)
                self.take_profit = price * (1 + TAKE_PROFIT_PCT)
                self.max_drawdown = price
                self.trades.append({
                    'type': 'buy',
                    'price': price,
                    'time': pd.Timestamp.now()
                })
            elif signal == -1:  # Sell signal
                self.position = -1
                self.entry_price = price
                self.stop_loss = price * (1 + STOP_LOSS_PCT)
                self.take_profit = price * (1 - TAKE_PROFIT_PCT)
                self.max_drawdown = price
                self.trades.append({
                    'type': 'sell',
                    'price': price,
                    'time': pd.Timestamp.now()
                })
        else:  # Has position
            if self.position == 1:  # Long position
                if price < self.stop_loss:
                    self.position = 0
                    self.trades.append({
                        'type': 'stop_loss',
                        'price': price,
                        'time': pd.Timestamp.now()
                    })
                elif price > self.take_profit:
                    self.position = 0
                    self.trades.append({
                        'type': 'take_profit',
                        'price': price,
                        'time': pd.Timestamp.now()
                    })
                elif price > self.max_drawdown:
                    self.max_drawdown = price
                elif (self.max_drawdown - price) / self.max_drawdown > MAX_DRAWDOWN_PCT:
                    self.position = 0
                    self.trades.append({
                        'type': 'max_drawdown',
                        'price': price,
                        'time': pd.Timestamp.now()
                    })
            else:  # Short position
                if price > self.stop_loss:
                    self.position = 0
                    self.trades.append({
                        'type': 'stop_loss',
                        'price': price,
                        'time': pd.Timestamp.now()
                    })
                elif price < self.take_profit:
                    self.position = 0
                    self.trades.append({
                        'type': 'take_profit',
                        'price': price,
                        'time': pd.Timestamp.now()
                    })
                elif price < self.max_drawdown:
                    self.max_drawdown = price
                elif (price - self.max_drawdown) / self.max_drawdown > MAX_DRAWDOWN_PCT:
                    self.position = 0
                    self.trades.append({
                        'type': 'max_drawdown',
                        'price': price,
                        'time': pd.Timestamp.now()
                    }) 