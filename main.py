import pandas as pd
from okx_api import OKXAPI
from backtest import BacktestEngine
from config import BACKTEST_START_DATE, BACKTEST_END_DATE, TIMEFRAME
# from test_data import generate_test_data  # 注释掉

def main():
    # 读取真实BTC日线数据
    print("读取OKX BTC/USDT 2023年日线数据...")
    df = pd.read_csv('btc_okx_2023_1d.csv', index_col='timestamp', parse_dates=True)
    
    # Run backtest
    print("Running backtest...")
    backtest = BacktestEngine()
    
    # Train AI models
    print("\nTraining AI models...")
    backtest.strategy.train_ai_models(df)
    
    # Run backtest
    metrics = backtest.run_backtest(df)
    
    # Plot backtest results
    print("\nPlotting backtest results...")
    backtest.plot_results(metrics)

if __name__ == "__main__":
    main() 