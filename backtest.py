import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from strategy import TradingStrategy
from config import (
    BACKTEST_START_DATE, BACKTEST_END_DATE, TIMEFRAME,
    STOP_LOSS_PCT, TAKE_PROFIT_PCT, MAX_DRAWDOWN_PCT
)

class BacktestEngine:
    def __init__(self):
        self.strategy = TradingStrategy()
        self.trades = []
        self.equity_curve = []
        self.price_curve = []  # 新增价格曲线
        self.initial_balance = 10000  # Starting balance
        
    def run_backtest(self, df):
        """Run backtest on historical data"""
        # Filter data by date range
        df = df[(df.index >= BACKTEST_START_DATE) & (df.index <= BACKTEST_END_DATE)]
        
        # Initialize variables
        balance = self.initial_balance
        position = 0
        entry_price = 0
        stop_loss = 0
        take_profit = 0
        max_drawdown = 0
        
        # Train AI models
        print("\nTraining AI models...")
        self.strategy.train_ai_models(df)
        
        # Run backtest
        print("\nRunning backtest...")
        for i in range(len(df)):
            current_price = df['close'].iloc[i]
            
            # Get trading signal
            signal = self.strategy.get_signal(df.iloc[:i+1])
            
            # Update position
            if position == 0:  # No position
                if signal == 1:  # Buy signal
                    position = 1
                    entry_price = current_price
                    stop_loss = current_price * (1 - STOP_LOSS_PCT)
                    take_profit = current_price * (1 + TAKE_PROFIT_PCT)
                    max_drawdown = current_price
                    self.trades.append({
                        'type': 'buy',
                        'price': current_price,
                        'time': df.index[i]
                    })
                    print(f"Buy at {current_price:.2f}")
                elif signal == -1:  # Sell signal
                    position = -1
                    entry_price = current_price
                    stop_loss = current_price * (1 + STOP_LOSS_PCT)
                    take_profit = current_price * (1 - TAKE_PROFIT_PCT)
                    max_drawdown = current_price
                    self.trades.append({
                        'type': 'sell',
                        'price': current_price,
                        'time': df.index[i]
                    })
                    print(f"Sell at {current_price:.2f}")
            else:  # Has position
                if position == 1:  # Long position
                    if current_price <= stop_loss:  # Stop loss hit
                        balance *= (current_price / entry_price)
                        position = 0
                        self.trades.append({
                            'type': 'stop_loss',
                            'price': current_price,
                            'time': df.index[i]
                        })
                        print(f"Stop loss at {current_price:.2f}")
                    elif current_price >= take_profit:  # Take profit hit
                        balance *= (current_price / entry_price)
                        position = 0
                        self.trades.append({
                            'type': 'take_profit',
                            'price': current_price,
                            'time': df.index[i]
                        })
                        print(f"Take profit at {current_price:.2f}")
                    elif current_price > max_drawdown:
                        max_drawdown = current_price
                    elif signal == -1:  # Exit on opposite signal
                        balance *= (current_price / entry_price)
                        position = 0
                        self.trades.append({
                            'type': 'signal_exit',
                            'price': current_price,
                            'time': df.index[i]
                        })
                        print(f"Signal exit at {current_price:.2f}")
                else:  # Short position
                    if current_price >= stop_loss:  # Stop loss hit
                        balance *= (entry_price / current_price)
                        position = 0
                        self.trades.append({
                            'type': 'stop_loss',
                            'price': current_price,
                            'time': df.index[i]
                        })
                        print(f"Stop loss at {current_price:.2f}")
                    elif current_price <= take_profit:  # Take profit hit
                        balance *= (entry_price / current_price)
                        position = 0
                        self.trades.append({
                            'type': 'take_profit',
                            'price': current_price,
                            'time': df.index[i]
                        })
                        print(f"Take profit at {current_price:.2f}")
                    elif current_price < max_drawdown:
                        max_drawdown = current_price
                    elif signal == 1:  # Exit on opposite signal
                        balance *= (entry_price / current_price)
                        position = 0
                        self.trades.append({
                            'type': 'signal_exit',
                            'price': current_price,
                            'time': df.index[i]
                        })
                        print(f"Signal exit at {current_price:.2f}")
            
            # Update equity curve
            self.equity_curve.append(balance)
            self.price_curve.append(current_price)  # 记录价格
        
        # Calculate metrics
        metrics = self.calculate_metrics()
        
        return metrics
        
    def calculate_metrics(self):
        """Calculate backtest metrics"""
        if not self.trades:
            return {
                'total_return': 0,
                'max_drawdown': 0,
                'sharpe_ratio': 0,
                'win_rate': 0,
                'total_trades': 0
            }
            
        # Calculate returns
        returns = pd.Series(self.equity_curve).pct_change().dropna()
        
        # Total return
        total_return = (self.equity_curve[-1] / self.initial_balance - 1) * 100
        
        # Maximum drawdown
        max_drawdown = ((pd.Series(self.equity_curve).cummax() - pd.Series(self.equity_curve)) / 
                       pd.Series(self.equity_curve).cummax()).max() * 100
        
        # Sharpe ratio
        sharpe_ratio = np.sqrt(252) * returns.mean() / returns.std() if len(returns) > 0 else 0
        
        # Win rate
        winning_trades = [t for t in self.trades if t['type'] in ['take_profit', 'max_drawdown']]
        win_rate = len(winning_trades) / len(self.trades) * 100 if self.trades else 0
        
        return {
            'total_return': total_return,
            'max_drawdown': max_drawdown,
            'sharpe_ratio': sharpe_ratio,
            'win_rate': win_rate,
            'total_trades': len(self.trades)
        }
        
    def plot_results(self, metrics):
        """Plot backtest results"""
        plt.ion()  # 开启交互模式
        # Create figure with subplots
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8), gridspec_kw={'height_ratios': [2, 1]})
        # 最大化窗口（Windows下）
        try:
            fig.canvas.manager.window.state('zoomed')
        except Exception:
            try:
                fig.canvas.manager.window.showMaximized()
            except Exception:
                pass  # 兼容不同平台
        # Plot equity curve
        ax1.plot(self.equity_curve, label='Equity Curve', color='blue')
        ax1.set_title('Equity Curve')
        ax1.set_xlabel('Time')
        ax1.set_ylabel('Equity (USDT)')
        ax1.grid(True)
        ax1.legend()
        # Plot price chart
        ax2.plot(self.price_curve, label='Price', color='green')
        ax2.set_title('Price Chart')
        ax2.set_xlabel('Time')
        ax2.set_ylabel('Price (USDT)')
        ax2.grid(True)
        ax2.legend()
        # 自适应布局
        plt.tight_layout()
        fig.autofmt_xdate()
        # Print metrics
        print("\nBacktest Results:")
        print(f"Total Return: {metrics['total_return']:.2f}%")
        print(f"Maximum Drawdown: {metrics['max_drawdown']:.2f}%")
        print(f"Sharpe Ratio: {metrics['sharpe_ratio']:.2f}")
        print(f"Win Rate: {metrics['win_rate']:.2f}%")
        print(f"Total Trades: {metrics['total_trades']}")
        # Show plot
        plt.show(block=True) 