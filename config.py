import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# API配置
API_KEY = os.getenv('OKX_API_KEY')
SECRET_KEY = os.getenv('OKX_SECRET_KEY')
PASSPHRASE = os.getenv('OKX_PASSPHRASE')

# 交易配置
SYMBOL = 'BTC-USDT'  # 交易对
LEVERAGE = 1  # 杠杆倍数
POSITION_SIZE = 0.01  # 每次交易的数量（BTC）

# 回测配置
BACKTEST_START_DATE = '2023-01-01'
BACKTEST_END_DATE = '2023-12-31'
TIMEFRAME = '1h'  # 时间周期：1小时

# 风险管理参数
MAX_DRAWDOWN = 0.15  # 最大回撤限制（15%）
STOP_LOSS_PCT = 0.02  # 止损比例（2%）
TAKE_PROFIT_PCT = 0.04  # 止盈比例（4%）
MAX_POSITION_SIZE = 0.1  # 最大持仓比例（10%）
VOLATILITY_THRESHOLD = 0.03  # 波动率阈值（3%）

# 技术指标参数
# RSI参数
RSI_PERIOD = 14
RSI_OVERBOUGHT = 70
RSI_OVERSOLD = 30

# 移动平均线参数
MA_PERIOD = 20
MA_FAST_PERIOD = 10
MA_SLOW_PERIOD = 30

# MACD参数
MACD_FAST_PERIOD = 12
MACD_SLOW_PERIOD = 26
MACD_SIGNAL_PERIOD = 9

# Bollinger Bands参数
BB_PERIOD = 20
BB_STD_DEV = 2

# ATR参数
ATR_PERIOD = 14
ATR_MULTIPLIER = 2  # 用于计算止损距离

# Volume Profile参数
VP_BINS = 20  # 成交量分布区间数

# AI算法参数
# 随机森林参数
RF_N_ESTIMATORS = 100  # 决策树数量
RF_MAX_DEPTH = 10  # 最大深度
RF_MIN_SAMPLES_SPLIT = 5  # 分裂所需最小样本数

# LSTM参数
LSTM_SEQUENCE_LENGTH = 60  # 序列长度
LSTM_BATCH_SIZE = 32  # 批次大小
LSTM_EPOCHS = 50  # 训练轮数
LSTM_HIDDEN_UNITS = 64  # 隐藏单元数

# 强化学习参数
RL_STATE_SIZE = 10  # 状态空间大小
RL_ACTION_SIZE = 3  # 动作空间大小（买入、卖出、持有）
RL_MEMORY_SIZE = 10000  # 经验回放缓冲区大小
RL_BATCH_SIZE = 32  # 训练批次大小
RL_GAMMA = 0.95  # 折扣因子
RL_EPSILON = 1.0  # 探索率
RL_EPSILON_MIN = 0.01  # 最小探索率
RL_EPSILON_DECAY = 0.995  # 探索率衰减 