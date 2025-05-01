import pandas as pd
from okx_api import OKXAPI
from backtest import BacktestEngine
from config import BACKTEST_START_DATE, BACKTEST_END_DATE, TIMEFRAME
from test_data import generate_test_data

def main():
    # Get test data
    print("Generating test data...")
    df = generate_test_data(BACKTEST_START_DATE, BACKTEST_END_DATE, TIMEFRAME)
    
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