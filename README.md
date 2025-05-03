# BTC AI Trading Bot

A Bitcoin trading bot based on machine learning for automated strategy backtesting and optimization.

## Project Introduction

This project is an AI-powered trading bot designed for Bitcoin trading strategy backtesting and optimization. It combines traditional technical analysis with machine learning methods to predict market trends and execute trading strategies automatically.

## Key Features

### Data Collection
- Real-time Bitcoin price data from OKX exchange
- Historical K-line data with multiple timeframes
- **Supports backtesting with real OKX BTC/USDT daily data (e.g., 2023)**
- Customizable data collection parameters

### AI Models
- Machine learning-based market prediction
- Multiple model architectures support
- Real-time model training and updating
- Model performance evaluation metrics

### Technical Analysis
- Support for multiple technical indicators
  - Moving Averages
  - RSI
  - MACD
  - Bollinger Bands
  - Custom indicators

### Backtesting System
- Comprehensive performance metrics
  - Total Return
  - Maximum Drawdown
  - Sharpe Ratio
  - Win Rate
  - Average Holding Time
  - Risk-Adjusted Return
- Detailed trade analysis
  - Entry/Exit points
  - Stop Loss/Take Profit analysis
  - Trade duration statistics
- Visualization tools
  - Equity curve
  - Drawdown chart
  - Trade distribution

## Installation Guide

### Prerequisites
- Python 3.8 or higher
- pip package manager
- Git

### Installation Steps

1. Clone the repository:
```bash
git clone https://github.com/yourusername/BTC_AI_Trading_bot.git
cd BTC_AI_Trading_bot
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure environment variables:
Create a `.env` file and add your OKX API credentials:
```
OKX_API_KEY=your_api_key
OKX_SECRET_KEY=your_secret_key
OKX_PASSPHRASE=your_passphrase
```

## Usage Guide

### 1. 获取真实BTC日线数据（OKX）
运行以下脚本，自动下载2023年BTC/USDT日线K线数据：
```bash
python fetch_okx_btc_daily.py
```
生成的文件为 `btc_okx_2023_1d.csv`。

### 2. 运行回测
```bash
python main.py
```
- 回测将自动读取 `btc_okx_2023_1d.csv` 作为数据源。
- 结果会显示真实BTC价格曲线和策略权益曲线。

### 3. 策略参数调整
- 策略信号阈值、止损止盈等参数可在 `config.py` 和 `strategy.py` 中调整：
  - `STOP_LOSS_PCT`、`TAKE_PROFIT_PCT`（止损/止盈百分比）
  - `get_signal` 方法中的信号阈值
- 支持趋势过滤、手续费模拟等高级自定义（详见代码注释）

### 4. 查看结果
- 自动弹出图表窗口，支持自适应和最大化显示
- Y轴单位均为 USDT
- 终端输出详细回测指标

## Project Structure

```
BTC_AI_Trading_bot/
├── main.py              # Main program entry
├── ai_models.py         # AI model training and prediction
├── backtest.py          # Backtesting engine
├── strategy.py          # Trading strategy implementation
├── okx_api.py           # OKX exchange API interface
├── fetch_okx_btc_daily.py # Script to fetch real BTC/USDT daily data from OKX
├── btc_okx_2023_1d.csv  # Real BTC/USDT daily data (generated)
├── config.py            # Configuration file
├── requirements.txt     # Dependencies
└── README.md            # Documentation
```

## Technical Details

### Data Processing
- Data normalization and standardization
- Feature engineering
- Time series analysis

### Machine Learning
- Model selection and optimization
- Hyperparameter tuning
- Cross-validation
- Model performance evaluation

### Risk Management
- Position sizing
- Stop loss and take profit strategies
- Risk-reward ratio calculation
- Portfolio optimization

## Important Notes

- This project is for educational and research purposes only
- Not financial advice
- Thorough testing required before live trading
- Trading involves risk

## Contributing

We welcome contributions to improve this project:
1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License
