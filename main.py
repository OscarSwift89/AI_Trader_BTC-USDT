import pandas as pd
from okx_api import OKXAPI
from backtest import BacktestEngine
from config import BACKTEST_START_DATE, BACKTEST_END_DATE, TIMEFRAME

def main():
    # Initialize API
    api = OKXAPI()
    
    # Get historical data
    print("Getting historical data...")
    klines = api.get_klines(timeframe=TIMEFRAME, limit=1000)
    
    # Convert data format
    df = pd.DataFrame(klines['data'], columns=['timestamp', 'open', 'high', 'low', 'close', 'volume', 'volCcy'])
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    df.set_index('timestamp', inplace=True)
    for col in ['open', 'high', 'low', 'close', 'volume', 'volCcy']:
        df[col] = df[col].astype(float)
    
    # Run backtest
    print("Running backtest...")
    backtest = BacktestEngine()
    
    # Train AI models
    print("\nTraining AI models...")
    backtest.strategy.train_ai_models(df)
    
    # Run backtest
    results = backtest.run_backtest(df)
    
    # Calculate and display backtest metrics
    metrics = backtest.calculate_metrics(results)
    print("\nBacktest results:")
    print(f"Total return: {metrics['total_return']:.2f}%")
    print(f"Maximum drawdown: {metrics['max_drawdown']:.2f}%")
    print(f"Sharpe ratio: {metrics['sharpe_ratio']:.2f}")
    print(f"Win rate: {metrics['win_rate']:.2f}%")
    print(f"Total trades: {metrics['total_trades']}")
    print(f"Average holding time: {metrics['avg_holding_time']:.2f} hours")
    
    # Analyze trade records
    trades = backtest.trades
    if trades:
        print("\nTrade analysis:")
        buy_trades = [t for t in trades if t['type'] == 'buy']
        sell_trades = [t for t in trades if t['type'] == 'sell']
        stop_loss_trades = [t for t in trades if t['type'] == 'stop_loss']
        take_profit_trades = [t for t in trades if t['type'] == 'take_profit']
        max_drawdown_trades = [t for t in trades if t['type'] == 'max_drawdown']
        
        print(f"Buy trades: {len(buy_trades)}")
        print(f"Sell trades: {len(sell_trades)}")
        print(f"Stop loss trades: {len(stop_loss_trades)}")
        print(f"Take profit trades: {len(take_profit_trades)}")
        print(f"Max drawdown trades: {len(max_drawdown_trades)}")
        
        # Calculate average trade price
        if buy_trades:
            avg_buy_price = sum(t['price'] for t in buy_trades) / len(buy_trades)
            print(f"Average buy price: {avg_buy_price:.2f}")
        if sell_trades:
            avg_sell_price = sum(t['price'] for t in sell_trades) / len(sell_trades)
            print(f"Average sell price: {avg_sell_price:.2f}")
        
        # Analyze AI prediction performance
        print("\nAI prediction analysis:")
        ai_correct = 0
        ai_total = 0
        
        for i in range(1, len(results)):
            if results['signal'].iloc[i] != 0:  # Has trading signal
                ai_total += 1
                if (results['signal'].iloc[i] == 1 and results['close'].iloc[i] < results['close'].iloc[i+1]) or \
                   (results['signal'].iloc[i] == -1 and results['close'].iloc[i] > results['close'].iloc[i+1]):
                    ai_correct += 1
        
        if ai_total > 0:
            ai_accuracy = ai_correct / ai_total * 100
            print(f"AI prediction accuracy: {ai_accuracy:.2f}%")
    
    # Plot backtest results
    print("\nPlotting backtest results...")
    backtest.plot_results(results)

if __name__ == "__main__":
    main() 