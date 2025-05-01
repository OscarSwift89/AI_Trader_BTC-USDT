import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def generate_test_data(start_date='2023-01-01', end_date='2023-12-31', interval='1h'):
    """Generate test data for backtesting"""
    # Convert dates to datetime
    start = pd.to_datetime(start_date)
    end = pd.to_datetime(end_date)
    
    # Generate timestamps
    if interval == '1h':
        timestamps = pd.date_range(start=start, end=end, freq='H')
    elif interval == '1d':
        timestamps = pd.date_range(start=start, end=end, freq='D')
    else:
        raise ValueError("Unsupported interval")
    
    # Generate random price data with trend and volatility
    n = len(timestamps)
    
    # Create multiple trends
    trend1 = np.linspace(0, 1, n//3) * 2000  # First upward trend
    trend2 = np.linspace(1, 0.5, n//3) * 2000  # Downward trend
    trend3 = np.linspace(0.5, 1.5, n//3) * 2000  # Second upward trend
    
    # Combine trends
    trend = np.concatenate([trend1, trend2, trend3])
    if len(trend) < n:
        trend = np.pad(trend, (0, n - len(trend)), mode='edge')
    
    # Add more volatility
    noise = np.random.normal(0, 200, n)  # Increased noise
    price = 30000 + trend + noise  # Base price + trend + noise
    
    # Generate OHLCV data with more realistic patterns
    data = []
    for i in range(n):
        base_price = price[i]
        
        # Add more realistic price movements
        high = base_price * (1 + abs(np.random.normal(0, 0.02)))  # Increased volatility
        low = base_price * (1 - abs(np.random.normal(0, 0.02)))  # Increased volatility
        
        # Ensure high > low
        if high < low:
            high, low = low, high
            
        # Generate open and close prices
        open_price = np.random.uniform(low, high)
        close = np.random.uniform(low, high)
        
        # Add volume spikes during trend changes
        if i % (n//10) == 0:  # Every 10% of the data
            volume = np.random.uniform(5, 15) * 100  # Higher volume during trend changes
        else:
            volume = np.random.uniform(1, 5) * 100  # Normal volume
        
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
    
    return df 