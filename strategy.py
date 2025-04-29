import pandas as pd
import numpy as np
import talib
from config import (
    RSI_PERIOD, RSI_OVERBOUGHT, RSI_OVERSOLD,
    MA_PERIOD, MA_FAST_PERIOD, MA_SLOW_PERIOD,
    MACD_FAST_PERIOD, MACD_SLOW_PERIOD, MACD_SIGNAL_PERIOD,
    BB_PERIOD, BB_STD_DEV,
    ATR_PERIOD, ATR_MULTIPLIER,
    VP_BINS,
    STOP_LOSS_PCT, TAKE_PROFIT_PCT,
    MAX_POSITION_SIZE, VOLATILITY_THRESHOLD
)
from ai_models import AIModels

class TradingStrategy:
    def __init__(self):
        # Initialize parameters
        self.rsi_period = RSI_PERIOD
        self.rsi_overbought = RSI_OVERBOUGHT
        self.rsi_oversold = RSI_OVERSOLD
        self.ma_period = MA_PERIOD
        self.ma_fast_period = MA_FAST_PERIOD
        self.ma_slow_period = MA_SLOW_PERIOD
        self.macd_fast = MACD_FAST_PERIOD
        self.macd_slow = MACD_SLOW_PERIOD
        self.macd_signal = MACD_SIGNAL_PERIOD
        self.bb_period = BB_PERIOD
        self.bb_std = BB_STD_DEV
        self.atr_period = ATR_PERIOD
        self.atr_multiplier = ATR_MULTIPLIER
        self.vp_bins = VP_BINS
        
        # Risk management parameters
        self.stop_loss_pct = STOP_LOSS_PCT
        self.take_profit_pct = TAKE_PROFIT_PCT
        self.max_position_size = MAX_POSITION_SIZE
        self.volatility_threshold = VOLATILITY_THRESHOLD
        
        # Initialize AI models
        self.ai_models = AIModels()
        self.is_ai_trained = False
        
    def train_ai_models(self, df):
        """训练AI模型"""
        print("Training random forest model...")
        rf_accuracy = self.ai_models.train_random_forest(df)
        print(f"Random forest accuracy: {rf_accuracy:.2f}")
        
        print("Training LSTM model...")
        lstm_accuracy = self.ai_models.train_lstm(df)
        print(f"LSTM accuracy: {lstm_accuracy:.2f}")
        
        print("Training reinforcement learning model...")
        self.ai_models.train_rl(df)
        
        self.is_ai_trained = True
        
    def calculate_indicators(self, df):
        """计算技术指标"""
        # RSI
        df['rsi'] = talib.RSI(df['close'], timeperiod=self.rsi_period)
        
        # Moving Averages
        df['ma'] = talib.SMA(df['close'], timeperiod=self.ma_period)
        df['ma_fast'] = talib.SMA(df['close'], timeperiod=self.ma_fast_period)
        df['ma_slow'] = talib.SMA(df['close'], timeperiod=self.ma_slow_period)
        
        # MACD
        macd, signal, hist = talib.MACD(
            df['close'],
            fastperiod=self.macd_fast,
            slowperiod=self.macd_slow,
            signalperiod=self.macd_signal
        )
        df['macd'] = macd
        df['macd_signal'] = signal
        df['macd_hist'] = hist
        
        # Bollinger Bands
        upper, middle, lower = talib.BBANDS(
            df['close'],
            timeperiod=self.bb_period,
            nbdevup=self.bb_std,
            nbdevdn=self.bb_std
        )
        df['bb_upper'] = upper
        df['bb_middle'] = middle
        df['bb_lower'] = lower
        
        # ATR
        df['atr'] = talib.ATR(
            df['high'],
            df['low'],
            df['close'],
            timeperiod=self.atr_period
        )
        
        # Volume Profile
        df['volume_profile'] = self._calculate_volume_profile(df)
        
        # Volatility
        df['volatility'] = df['close'].pct_change().rolling(window=20).std()
        
        return df
    
    def _calculate_volume_profile(self, df):
        """计算成交量分布"""
        price_range = df['close'].max() - df['close'].min()
        bin_size = price_range / self.vp_bins
        bins = np.arange(df['close'].min(), df['close'].max() + bin_size, bin_size)
        volume_profile = pd.cut(df['close'], bins=bins, labels=False)
        return volume_profile
    
    def calculate_position_size(self, df, current_price, balance):
        """计算仓位大小"""
        # Adjust position size based on volatility
        current_volatility = df['volatility'].iloc[-1]
        volatility_factor = 1 - (current_volatility / self.volatility_threshold)
        volatility_factor = max(0.1, min(1.0, volatility_factor))
        
        # Adjust stop loss distance based on ATR
        atr = df['atr'].iloc[-1]
        stop_distance = atr * self.atr_multiplier
        
        # Calculate maximum allowed position size
        max_position_value = balance * self.max_position_size
        position_size = max_position_value * volatility_factor / current_price
        
        return position_size, stop_distance
    
    def generate_signals(self, df):
        """生成交易信号"""
        signals = []
        stop_losses = []
        take_profits = []
        
        for i in range(1, len(df)):
            current = df.iloc[i]
            previous = df.iloc[i-1]
            
            # Get AI prediction
            if self.is_ai_trained:
                ai_signal = self.ai_models.predict(df.iloc[:i+1])
            else:
                ai_signal = 0
            
            # RSI signal
            rsi_signal = 0
            if current['rsi'] > self.rsi_overbought and previous['rsi'] <= self.rsi_overbought:
                rsi_signal = -1
            elif current['rsi'] < self.rsi_oversold and previous['rsi'] >= self.rsi_oversold:
                rsi_signal = 1
                
            # MACD signal
            macd_signal = 0
            if current['macd'] > current['macd_signal'] and previous['macd'] <= previous['macd_signal']:
                macd_signal = 1
            elif current['macd'] < current['macd_signal'] and previous['macd'] >= previous['macd_signal']:
                macd_signal = -1
                
            # Bollinger Bands signal
            bb_signal = 0
            if current['close'] < current['bb_lower']:
                bb_signal = 1
            elif current['close'] > current['bb_upper']:
                bb_signal = -1
                
            # Combined signal
            signal = 0
            if (rsi_signal == 1 and macd_signal == 1) or (rsi_signal == 1 and bb_signal == 1):
                signal = 1
            elif (rsi_signal == -1 and macd_signal == -1) or (rsi_signal == -1 and bb_signal == -1):
                signal = -1
                
            # Combine with AI signal
            if self.is_ai_trained:
                if ai_signal == 1 and signal == 1:
                    signal = 1  # Strong buy
                elif ai_signal == 2 and signal == -1:
                    signal = -1  # Strong sell
                elif ai_signal == 0:
                    signal = 0  # Hold
                
            # Calculate stop loss and take profit prices
            stop_loss = current['close'] * (1 - self.stop_loss_pct) if signal == 1 else current['close'] * (1 + self.stop_loss_pct)
            take_profit = current['close'] * (1 + self.take_profit_pct) if signal == 1 else current['close'] * (1 - self.take_profit_pct)
            
            signals.append(signal)
            stop_losses.append(stop_loss)
            take_profits.append(take_profit)
            
        # Add signal for the first time point (default to 0)
        signals.insert(0, 0)
        stop_losses.insert(0, 0)
        take_profits.insert(0, 0)
        
        df['signal'] = signals
        df['stop_loss'] = stop_losses
        df['take_profit'] = take_profits
        
        return df
    
    def get_trade_signal(self, df):
        """获取最新的交易信号"""
        if len(df) < 2:
            return 0, 0, 0
            
        current_signal = df['signal'].iloc[-1]
        current_stop_loss = df['stop_loss'].iloc[-1]
        current_take_profit = df['take_profit'].iloc[-1]
        
        return current_signal, current_stop_loss, current_take_profit 