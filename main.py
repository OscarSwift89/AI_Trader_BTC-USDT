import pandas as pd
from okx_api import OKXAPI
from backtest import BacktestEngine
from config import BACKTEST_START_DATE, BACKTEST_END_DATE, TIMEFRAME

def main():
    # 初始化API
    api = OKXAPI()
    
    # 获取历史数据
    print("获取历史数据...")
    klines = api.get_klines(timeframe=TIMEFRAME, limit=1000)
    
    # 转换数据格式
    df = pd.DataFrame(klines['data'], columns=['timestamp', 'open', 'high', 'low', 'close', 'volume', 'volCcy'])
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    df.set_index('timestamp', inplace=True)
    for col in ['open', 'high', 'low', 'close', 'volume', 'volCcy']:
        df[col] = df[col].astype(float)
    
    # 运行回测
    print("运行回测...")
    backtest = BacktestEngine()
    
    # 训练AI模型
    print("\n训练AI模型...")
    backtest.strategy.train_ai_models(df)
    
    # 运行回测
    results = backtest.run_backtest(df)
    
    # 计算并显示回测指标
    metrics = backtest.calculate_metrics(results)
    print("\n回测结果:")
    print(f"总收益率: {metrics['total_return']:.2f}%")
    print(f"最大回撤: {metrics['max_drawdown']:.2f}%")
    print(f"夏普比率: {metrics['sharpe_ratio']:.2f}")
    print(f"胜率: {metrics['win_rate']:.2f}%")
    print(f"总交易次数: {metrics['total_trades']}")
    print(f"平均持仓时间: {metrics['avg_holding_time']:.2f}小时")
    
    # 分析交易记录
    trades = backtest.trades
    if trades:
        print("\n交易分析:")
        buy_trades = [t for t in trades if t['type'] == 'buy']
        sell_trades = [t for t in trades if t['type'] == 'sell']
        stop_loss_trades = [t for t in trades if t['type'] == 'stop_loss']
        take_profit_trades = [t for t in trades if t['type'] == 'take_profit']
        max_drawdown_trades = [t for t in trades if t['type'] == 'max_drawdown']
        
        print(f"买入交易次数: {len(buy_trades)}")
        print(f"卖出交易次数: {len(sell_trades)}")
        print(f"止损交易次数: {len(stop_loss_trades)}")
        print(f"止盈交易次数: {len(take_profit_trades)}")
        print(f"最大回撤平仓次数: {len(max_drawdown_trades)}")
        
        # 计算平均交易价格
        if buy_trades:
            avg_buy_price = sum(t['price'] for t in buy_trades) / len(buy_trades)
            print(f"平均买入价格: {avg_buy_price:.2f}")
        if sell_trades:
            avg_sell_price = sum(t['price'] for t in sell_trades) / len(sell_trades)
            print(f"平均卖出价格: {avg_sell_price:.2f}")
        
        # 分析AI预测效果
        print("\nAI预测分析:")
        ai_correct = 0
        ai_total = 0
        
        for i in range(1, len(results)):
            if results['signal'].iloc[i] != 0:  # 有交易信号
                ai_total += 1
                if (results['signal'].iloc[i] == 1 and results['close'].iloc[i] < results['close'].iloc[i+1]) or \
                   (results['signal'].iloc[i] == -1 and results['close'].iloc[i] > results['close'].iloc[i+1]):
                    ai_correct += 1
        
        if ai_total > 0:
            ai_accuracy = ai_correct / ai_total * 100
            print(f"AI预测准确率: {ai_accuracy:.2f}%")
    
    # 绘制回测结果
    print("\n绘制回测结果图表...")
    backtest.plot_results(results)

if __name__ == "__main__":
    main() 