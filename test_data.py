import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def generate_test_data(start_date='2022-01-01', end_date='2023-12-31', interval='1h'):
    """Generate test data for backtesting"""
    # Convert dates to datetime
    start = pd.to_datetime(start_date)
    end = pd.to_datetime(end_date)
    
    # Generate timestamps
    if interval == '1h':
        timestamps = pd.date_range(start=start, end=end, freq='h')
    elif interval == '1d':
        timestamps = pd.date_range(start=start, end=end, freq='D')
    else:
        raise ValueError("Unsupported interval")
    
    # Generate random price data with trend and volatility
    n = len(timestamps)
    
    # Create more realistic market cycles
    total_periods = n
    single_cycle_length = total_periods // 3  # Divide total length into 3 major cycles
    phase_length = single_cycle_length // 3  # Each cycle has 3 phases
    
    cycles = []
    for _ in range(3):  # Create 3 market cycles
        # Bull market phase
        bull_trend = np.linspace(0, 1, phase_length) * 5000
        # Bear market phase
        bear_trend = np.linspace(1, 0.7, phase_length) * 5000
        # Sideways phase
        side_trend = np.ones(phase_length) * 3500
        cycles.extend([bull_trend, bear_trend, side_trend])
    
    # Combine cycles and ensure correct length
    trend = np.concatenate(cycles)
    if len(trend) < n:
        # Pad with the last value if needed
        padding = n - len(trend)
        trend = np.pad(trend, (0, padding), mode='edge')
    elif len(trend) > n:
        # Truncate if too long
        trend = trend[:n]
    
    # Add realistic volatility
    volatility = np.random.normal(0, 100, n)  # Base volatility
    # Add higher volatility during trend changes
    for i in range(0, n, n//10):
        end_idx = min(i + n//20, n)
        volatility[i:end_idx] *= 2
    
    price = 30000 + trend + volatility  # Base price + trend + volatility
    
    # Generate OHLCV data with more realistic patterns
    data = []
    for i in range(n):
        base_price = price[i]
        
        # Add realistic price movements
        high = base_price * (1 + abs(np.random.normal(0, 0.01)))
        low = base_price * (1 - abs(np.random.normal(0, 0.01)))
        
        # Ensure high > low
        if high < low:
            high, low = low, high
            
        # Generate open and close prices
        open_price = np.random.uniform(low, high)
        close = np.random.uniform(low, high)
        
        # Add realistic volume patterns
        if i % (n//10) == 0:  # Every 10% of the data
            volume = np.random.uniform(3, 8) * 100  # Higher volume during trend changes
        else:
            volume = np.random.uniform(1, 3) * 100  # Normal volume
        
        data.append([
            timestamps[i],
            open_price,
            high,
            low,
            close,
            volume
        ])
    
    # Create DataFrame
    df = pd.DataFrame(data, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
    df.set_index('timestamp', inplace=True)
    
    print(df['close'].describe())  # 打印价格统计信息
    return df 