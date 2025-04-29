# BTC AI Trading Bot / BTC AI 交易机器人

A Bitcoin trading bot based on machine learning for automated strategy backtesting and optimization.
一个基于机器学习的比特币交易机器人，用于自动化交易策略的回测和优化。

## Project Introduction / 项目简介

This project is an AI-powered trading bot designed for Bitcoin trading strategy backtesting and optimization. It combines traditional technical analysis with machine learning methods to predict market trends and execute trading strategies automatically.
这是一个用于比特币交易策略回测和优化的 AI 交易机器人。项目结合了传统技术分析和机器学习方法，通过历史数据训练模型来预测市场走势，并自动执行交易策略。

## Key Features / 主要功能

### Data Collection / 数据采集
- Real-time Bitcoin price data from OKX exchange / 实时获取 OKX 交易所的比特币价格数据
- Historical K-line data with multiple timeframes / 支持多时间周期的历史K线数据
- Customizable data collection parameters / 可自定义的数据采集参数

### AI Models / AI模型
- Machine learning-based market prediction / 基于机器学习的市场预测
- Multiple model architectures support / 支持多种模型架构
- Real-time model training and updating / 实时模型训练和更新
- Model performance evaluation metrics / 模型性能评估指标

### Technical Analysis / 技术分析
- Support for multiple technical indicators / 支持多种技术指标分析
  - Moving Averages / 移动平均线
  - RSI / 相对强弱指标
  - MACD / 移动平均收敛散度
  - Bollinger Bands / 布林带
  - Custom indicators / 自定义指标

### Backtesting System / 回测系统
- Comprehensive performance metrics / 完整的性能指标
  - Total Return / 总收益率
  - Maximum Drawdown / 最大回撤
  - Sharpe Ratio / 夏普比率
  - Win Rate / 交易胜率
  - Average Holding Time / 平均持仓时间
  - Risk-Adjusted Return / 风险调整后收益
- Detailed trade analysis / 详细的交易分析
  - Entry/Exit points / 入场/出场点
  - Stop Loss/Take Profit analysis / 止损/止盈分析
  - Trade duration statistics / 交易持续时间统计
- Visualization tools / 可视化工具
  - Equity curve / 资金曲线
  - Drawdown chart / 回撤图表
  - Trade distribution / 交易分布图

## Installation Guide / 安装指南

### Prerequisites / 系统要求
- Python 3.8 or higher / Python 3.8 或更高版本
- pip package manager / pip 包管理器
- Git / Git 版本控制工具

### Installation Steps / 安装步骤

1. Clone the repository / 克隆项目到本地：
```bash
git clone https://github.com/yourusername/BTC_AI_Trading_bot.git
cd BTC_AI_Trading_bot
```

2. Install dependencies / 安装依赖：
```bash
pip install -r requirements.txt
```

3. Configure environment variables / 配置环境变量：
Create a `.env` file and add your OKX API credentials / 创建 `.env` 文件并添加你的 OKX API 密钥：
```
OKX_API_KEY=your_api_key
OKX_SECRET_KEY=your_secret_key
OKX_PASSPHRASE=your_passphrase
```

## Usage Guide / 使用指南

### Basic Usage / 基本使用

1. Run backtesting / 运行回测：
```bash
python main.py
```

2. View results / 查看结果：
- Automatic display of backtest metrics / 自动显示回测指标
- Generation of performance charts / 生成性能图表
- Detailed trade analysis report / 详细的交易分析报告

### Advanced Features / 高级功能

1. Custom Strategy / 自定义策略
- Modify `strategy.py` to implement your own trading logic / 修改 `strategy.py` 实现自己的交易逻辑
- Add new technical indicators / 添加新的技术指标
- Adjust risk management parameters / 调整风险管理参数

2. Model Training / 模型训练
- Customize model parameters in `ai_models.py` / 在 `ai_models.py` 中自定义模型参数
- Add new features for prediction / 添加新的预测特征
- Implement different machine learning algorithms / 实现不同的机器学习算法

## Project Structure / 项目结构

```
BTC_AI_Trading_bot/
├── main.py              # Main program entry / 主程序入口
├── ai_models.py         # AI model training and prediction / AI模型训练和预测
├── backtest.py          # Backtesting engine / 回测引擎
├── strategy.py          # Trading strategy implementation / 交易策略实现
├── okx_api.py           # OKX exchange API interface / OKX交易所API接口
├── config.py            # Configuration file / 配置文件
├── requirements.txt     # Dependencies / 依赖包列表
└── README.md            # Documentation / 项目文档
```

## Technical Details / 技术细节

### Data Processing / 数据处理
- Data normalization and standardization / 数据标准化和归一化
- Feature engineering / 特征工程
- Time series analysis / 时间序列分析

### Machine Learning / 机器学习
- Model selection and optimization / 模型选择和优化
- Hyperparameter tuning / 超参数调优
- Cross-validation / 交叉验证
- Model performance evaluation / 模型性能评估

### Risk Management / 风险管理
- Position sizing / 仓位管理
- Stop loss and take profit strategies / 止损和止盈策略
- Risk-reward ratio calculation / 风险收益比计算
- Portfolio optimization / 投资组合优化

## Important Notes / 注意事项

- This project is for educational and research purposes only / 本项目仅用于学习和研究目的
- Not financial advice / 不构成任何投资建议
- Thorough testing required before live trading / 使用实盘交易前请充分测试
- Trading involves risk / 投资有风险，入市需谨慎

## Contributing / 贡献指南

We welcome contributions to improve this project / 欢迎提交改进建议：
1. Fork the repository / 克隆项目
2. Create your feature branch / 创建特性分支
3. Commit your changes / 提交更改
4. Push to the branch / 推送到分支
5. Create a Pull Request / 创建拉取请求

## License / 许可证

This project is licensed under the MIT License / 本项目采用 MIT 许可证
