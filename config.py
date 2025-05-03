import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# API configuration
API_KEY = os.getenv('OKX_API_KEY')
SECRET_KEY = os.getenv('OKX_SECRET_KEY')
PASSPHRASE = os.getenv('OKX_PASSPHRASE')

# Trading configuration
SYMBOL = 'BTC/USDT'
TIMEFRAME = '1h'

# Backtest configuration
BACKTEST_START_DATE = '2022-01-01'
BACKTEST_END_DATE = '2023-12-31'

# Risk management parameters
STOP_LOSS_PCT = 0.03  # 3% stop loss
TAKE_PROFIT_PCT = 0.06  # 6% take profit
MAX_DRAWDOWN_PCT = 0.05  # 5% maximum drawdown

# Technical indicator parameters
RSI_PERIOD = 14
RSI_OVERBOUGHT = 70  # More conservative
RSI_OVERSOLD = 30  # More conservative

MACD_FAST = 12
MACD_SLOW = 26
MACD_SIGNAL = 9

BB_PERIOD = 20
BB_STD = 2.0  # More conservative

MA_PERIOD = 20

# Trading configuration
LEVERAGE = 1  # Leverage ratio
POSITION_SIZE = 0.01  # Position size per trade (BTC)

# Risk management parameters
MAX_POSITION_SIZE = 0.1  # Maximum position size (10%)
VOLATILITY_THRESHOLD = 0.03  # Volatility threshold (3%)

# Technical indicator parameters
# Moving Average parameters
MA_FAST_PERIOD = 10
MA_SLOW_PERIOD = 30

# MACD parameters
MACD_FAST_PERIOD = 12
MACD_SLOW_PERIOD = 26
MACD_SIGNAL_PERIOD = 9

# Bollinger Bands parameters
BB_STD_DEV = 2

# ATR parameters
ATR_PERIOD = 14
ATR_MULTIPLIER = 2  # Used for calculating stop loss distance

# Volume Profile parameters
VP_BINS = 20  # Number of volume distribution bins

# AI algorithm parameters
# Random Forest parameters
RF_N_ESTIMATORS = 100  # Number of decision trees
RF_MAX_DEPTH = 10  # Maximum depth
RF_MIN_SAMPLES_SPLIT = 5  # Minimum samples required to split

# LSTM parameters
LSTM_SEQUENCE_LENGTH = 60  # Sequence length
LSTM_BATCH_SIZE = 32  # Batch size
LSTM_EPOCHS = 50  # Number of epochs
LSTM_HIDDEN_UNITS = 64  # Number of hidden units

# Reinforcement Learning parameters
RL_STATE_SIZE = 10  # State space size
RL_ACTION_SIZE = 3  # 动作空间大小（买入、卖出、持有）
RL_MEMORY_SIZE = 10000  # 经验回放缓冲区大小
RL_BATCH_SIZE = 32  # 训练批次大小
RL_GAMMA = 0.95  # 折扣因子
RL_EPSILON = 1.0  # 探索率
RL_EPSILON_MIN = 0.01  # 最小探索率
RL_EPSILON_DECAY = 0.995  # 探索率衰减 