import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from strategy import TradingStrategy
from config import POSITION_SIZE, MAX_DRAWDOWN

class BacktestEngine:
    def __init__(self, initial_balance=10000):
        self.initial_balance = initial_balance
        self.balance = initial_balance
        self.position = 0
        self.trades = []
        self.strategy = TradingStrategy()
        self.max_drawdown = 0
        self.current_drawdown = 0
        self.peak_balance = initial_balance
        
    def run_backtest(self, df):
        """运行回测"""
        # 计算技术指标
        df = self.strategy.calculate_indicators(df)
        df = self.strategy.generate_signals(df)
        
        # 初始化回测结果
        df['balance'] = self.initial_balance
        df['position'] = 0
        df['pnl'] = 0
        df['drawdown'] = 0
        
        for i in range(1, len(df)):
            current = df.iloc[i]
            previous = df.iloc[i-1]
            
            # 更新持仓市值和回撤
            if self.position != 0:
                pnl = (current['close'] - previous['close']) * self.position
                self.balance += pnl
                df.at[i, 'pnl'] = pnl
                
                # 更新回撤
                self.peak_balance = max(self.peak_balance, self.balance)
                self.current_drawdown = (self.peak_balance - self.balance) / self.peak_balance
                self.max_drawdown = max(self.max_drawdown, self.current_drawdown)
                df.at[i, 'drawdown'] = self.current_drawdown
                
                # 检查是否触发止损或止盈
                if self.position > 0:  # 多头持仓
                    if current['low'] <= current['stop_loss']:
                        # 触发止损
                        self.position = 0
                        self.trades.append({
                            'timestamp': current.name,
                            'type': 'stop_loss',
                            'price': current['stop_loss'],
                            'size': abs(self.position)
                        })
                    elif current['high'] >= current['take_profit']:
                        # 触发止盈
                        self.position = 0
                        self.trades.append({
                            'timestamp': current.name,
                            'type': 'take_profit',
                            'price': current['take_profit'],
                            'size': abs(self.position)
                        })
                elif self.position < 0:  # 空头持仓
                    if current['high'] >= current['stop_loss']:
                        # 触发止损
                        self.position = 0
                        self.trades.append({
                            'timestamp': current.name,
                            'type': 'stop_loss',
                            'price': current['stop_loss'],
                            'size': abs(self.position)
                        })
                    elif current['low'] <= current['take_profit']:
                        # 触发止盈
                        self.position = 0
                        self.trades.append({
                            'timestamp': current.name,
                            'type': 'take_profit',
                            'price': current['take_profit'],
                            'size': abs(self.position)
                        })
            
            # 检查最大回撤限制
            if self.current_drawdown > MAX_DRAWDOWN:
                # 如果超过最大回撤限制，平掉所有仓位
                if self.position != 0:
                    self.trades.append({
                        'timestamp': current.name,
                        'type': 'max_drawdown',
                        'price': current['close'],
                        'size': abs(self.position)
                    })
                self.position = 0
                continue
            
            # 执行交易信号
            signal = current['signal']
            
            if signal == 1 and self.position <= 0:  # 买入信号
                # 计算动态仓位大小
                position_size, _ = self.strategy.calculate_position_size(
                    df.iloc[:i+1],
                    current['close'],
                    self.balance
                )
                self.position = position_size
                self.trades.append({
                    'timestamp': current.name,
                    'type': 'buy',
                    'price': current['close'],
                    'size': position_size
                })
            elif signal == -1 and self.position >= 0:  # 卖出信号
                # 计算动态仓位大小
                position_size, _ = self.strategy.calculate_position_size(
                    df.iloc[:i+1],
                    current['close'],
                    self.balance
                )
                self.position = -position_size
                self.trades.append({
                    'timestamp': current.name,
                    'type': 'sell',
                    'price': current['close'],
                    'size': position_size
                })
            
            # 更新余额和持仓
            df.at[i, 'balance'] = self.balance
            df.at[i, 'position'] = self.position
            
        return df
    
    def calculate_metrics(self, df):
        """计算回测指标"""
        # 计算总收益率
        total_return = (self.balance - self.initial_balance) / self.initial_balance * 100
        
        # 计算最大回撤
        max_drawdown = self.max_drawdown * 100
        
        # 计算夏普比率
        returns = df['balance'].pct_change().dropna()
        sharpe_ratio = np.sqrt(252) * returns.mean() / returns.std()
        
        # 计算胜率
        winning_trades = len([t for t in self.trades if t['type'] in ['take_profit', 'max_drawdown']])
        total_trades = len(self.trades)
        win_rate = (winning_trades / total_trades * 100) if total_trades > 0 else 0
        
        # 计算平均持仓时间
        if len(self.trades) >= 2:
            trade_times = [t['timestamp'] for t in self.trades]
            holding_times = [(trade_times[i+1] - trade_times[i]).total_seconds() / 3600 
                           for i in range(0, len(trade_times)-1, 2)]
            avg_holding_time = np.mean(holding_times)
        else:
            avg_holding_time = 0
        
        return {
            'total_return': total_return,
            'max_drawdown': max_drawdown,
            'sharpe_ratio': sharpe_ratio,
            'win_rate': win_rate,
            'total_trades': total_trades,
            'avg_holding_time': avg_holding_time
        }
    
    def plot_results(self, df):
        """绘制回测结果"""
        plt.figure(figsize=(15, 12))
        
        # 绘制价格和信号
        plt.subplot(4, 1, 1)
        plt.plot(df.index, df['close'], label='Price')
        plt.plot(df.index, df['bb_upper'], 'r--', label='BB Upper')
        plt.plot(df.index, df['bb_middle'], 'g--', label='BB Middle')
        plt.plot(df.index, df['bb_lower'], 'r--', label='BB Lower')
        
        buy_signals = df[df['signal'] == 1].index
        sell_signals = df[df['signal'] == -1].index
        plt.scatter(buy_signals, df.loc[buy_signals, 'close'], color='green', label='Buy Signal')
        plt.scatter(sell_signals, df.loc[sell_signals, 'close'], color='red', label='Sell Signal')
        plt.legend()
        plt.title('Price, Bollinger Bands and Trading Signals')
        
        # 绘制技术指标
        plt.subplot(4, 1, 2)
        plt.plot(df.index, df['rsi'], label='RSI')
        plt.plot(df.index, df['macd'], label='MACD')
        plt.plot(df.index, df['macd_signal'], label='MACD Signal')
        plt.axhline(y=70, color='r', linestyle='--')
        plt.axhline(y=30, color='g', linestyle='--')
        plt.legend()
        plt.title('Technical Indicators')
        
        # 绘制账户余额和回撤
        plt.subplot(4, 1, 3)
        plt.plot(df.index, df['balance'], label='Balance')
        plt.plot(df.index, df['drawdown'] * 100, 'r--', label='Drawdown %')
        plt.legend()
        plt.title('Account Balance and Drawdown')
        
        # 绘制持仓
        plt.subplot(4, 1, 4)
        plt.plot(df.index, df['position'], label='Position')
        plt.legend()
        plt.title('Position Size')
        
        plt.tight_layout()
        plt.show() 