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
        # 初始化参数
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
        
        # 风险管理参数
        self.stop_loss_pct = STOP_LOSS_PCT
        self.take_profit_pct = TAKE_PROFIT_PCT
        self.max_position_size = MAX_POSITION_SIZE
        self.volatility_threshold = VOLATILITY_THRESHOLD
        
        # 初始化AI模型
        self.ai_models = AIModels()
        self.is_ai_trained = False
        
    def train_ai_models(self, df):
        """训练AI模型"""
        print("训练随机森林模型...")
        rf_accuracy = self.ai_models.train_random_forest(df)
        print(f"随机森林准确率: {rf_accuracy:.2f}")
        
        print("训练LSTM模型...")
        lstm_accuracy = self.ai_models.train_lstm(df)
        print(f"LSTM准确率: {lstm_accuracy:.2f}")
        
        print("训练强化学习模型...")
        self.ai_models.train_rl(df)
        
        self.is_ai_trained = True
        
    def calculate_indicators(self, df):
        """计算技术指标"""
        # RSI
        df['rsi'] = talib.RSI(df['close'], timeperiod=self.rsi_period)
        
        # 移动平均线
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
        
        # 波动率
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
        # 基于波动率调整仓位
        current_volatility = df['volatility'].iloc[-1]
        volatility_factor = 1 - (current_volatility / self.volatility_threshold)
        volatility_factor = max(0.1, min(1.0, volatility_factor))
        
        # 基于ATR调整止损距离
        atr = df['atr'].iloc[-1]
        stop_distance = atr * self.atr_multiplier
        
        # 计算最大允许仓位
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
            
            # 获取AI预测
            if self.is_ai_trained:
                ai_signal = self.ai_models.predict(df.iloc[:i+1])
            else:
                ai_signal = 0
            
            # RSI信号
            rsi_signal = 0
            if current['rsi'] > self.rsi_overbought and previous['rsi'] <= self.rsi_overbought:
                rsi_signal = -1
            elif current['rsi'] < self.rsi_oversold and previous['rsi'] >= self.rsi_oversold:
                rsi_signal = 1
                
            # MACD信号
            macd_signal = 0
            if current['macd'] > current['macd_signal'] and previous['macd'] <= previous['macd_signal']:
                macd_signal = 1
            elif current['macd'] < current['macd_signal'] and previous['macd'] >= previous['macd_signal']:
                macd_signal = -1
                
            # Bollinger Bands信号
            bb_signal = 0
            if current['close'] < current['bb_lower']:
                bb_signal = 1
            elif current['close'] > current['bb_upper']:
                bb_signal = -1
                
            # 综合信号
            signal = 0
            if (rsi_signal == 1 and macd_signal == 1) or (rsi_signal == 1 and bb_signal == 1):
                signal = 1
            elif (rsi_signal == -1 and macd_signal == -1) or (rsi_signal == -1 and bb_signal == -1):
                signal = -1
                
            # 结合AI信号
            if self.is_ai_trained:
                if ai_signal == 1 and signal == 1:
                    signal = 1  # 强烈买入
                elif ai_signal == 2 and signal == -1:
                    signal = -1  # 强烈卖出
                elif ai_signal == 0:
                    signal = 0  # 观望
                
            # 计算止损止盈价格
            stop_loss = current['close'] * (1 - self.stop_loss_pct) if signal == 1 else current['close'] * (1 + self.stop_loss_pct)
            take_profit = current['close'] * (1 + self.take_profit_pct) if signal == 1 else current['close'] * (1 - self.take_profit_pct)
            
            signals.append(signal)
            stop_losses.append(stop_loss)
            take_profits.append(take_profit)
            
        # 添加第一个时间点的信号（默认为0）
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