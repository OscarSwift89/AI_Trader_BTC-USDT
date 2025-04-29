import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
from tensorflow.keras.optimizers import Adam
import tensorflow as tf
from collections import deque
import random

class AIModels:
    def __init__(self):
        self.rf_model = None
        self.lstm_model = None
        self.rl_model = None
        self.scaler = StandardScaler()
        self.memory = deque(maxlen=10000)  # 经验回放缓冲区
        
    def prepare_features(self, df):
        """准备特征数据"""
        # 计算技术指标
        features = pd.DataFrame()
        
        # 价格特征
        features['returns'] = df['close'].pct_change()
        features['log_returns'] = np.log(df['close']).diff()
        
        # 波动率特征
        features['volatility'] = df['close'].pct_change().rolling(window=20).std()
        features['atr'] = df['atr']
        
        # 趋势特征
        features['ma_diff'] = df['ma_fast'] - df['ma_slow']
        features['macd'] = df['macd']
        features['macd_signal'] = df['macd_signal']
        
        # 动量特征
        features['rsi'] = df['rsi']
        features['bb_position'] = (df['close'] - df['bb_middle']) / (df['bb_upper'] - df['bb_lower'])
        
        # 成交量特征
        features['volume_change'] = df['volume'].pct_change()
        features['volume_ma'] = df['volume'].rolling(window=20).mean()
        
        # 清理数据
        features = features.dropna()
        
        return features
    
    def prepare_labels(self, df, horizon=1):
        """准备标签数据"""
        # 计算未来价格变化
        future_returns = df['close'].shift(-horizon).pct_change()
        
        # 将价格变化转换为分类标签
        labels = np.zeros(len(future_returns))
        labels[future_returns > 0.001] = 1  # 上涨
        labels[future_returns < -0.001] = 2  # 下跌
        
        return labels[:-horizon]  # 移除最后horizon个样本
    
    def train_random_forest(self, df):
        """训练随机森林模型"""
        features = self.prepare_features(df)
        labels = self.prepare_labels(df)
        
        # 标准化特征
        X = self.scaler.fit_transform(features)
        y = labels
        
        # 训练模型
        self.rf_model = RandomForestClassifier(
            n_estimators=100,
            max_depth=10,
            min_samples_split=5,
            random_state=42
        )
        self.rf_model.fit(X, y)
        
        return self.rf_model.score(X, y)
    
    def train_lstm(self, df):
        """训练LSTM模型"""
        features = self.prepare_features(df)
        labels = self.prepare_labels(df)
        
        # 标准化特征
        X = self.scaler.fit_transform(features)
        y = labels
        
        # 准备序列数据
        X_sequences = []
        y_sequences = []
        for i in range(len(X) - 60):
            X_sequences.append(X[i:i+60])
            y_sequences.append(y[i+59])
        
        X_sequences = np.array(X_sequences)
        y_sequences = np.array(y_sequences)
        
        # 构建LSTM模型
        self.lstm_model = Sequential([
            LSTM(64, input_shape=(60, X.shape[1]), return_sequences=True),
            Dropout(0.2),
            LSTM(32),
            Dropout(0.2),
            Dense(3, activation='softmax')
        ])
        
        self.lstm_model.compile(
            optimizer=Adam(learning_rate=0.001),
            loss='sparse_categorical_crossentropy',
            metrics=['accuracy']
        )
        
        # 训练模型
        history = self.lstm_model.fit(
            X_sequences,
            y_sequences,
            batch_size=32,
            epochs=50,
            validation_split=0.2,
            verbose=0
        )
        
        return history.history['accuracy'][-1]
    
    def build_rl_model(self):
        """构建强化学习模型"""
        model = Sequential([
            Dense(64, activation='relu', input_shape=(10,)),
            Dense(32, activation='relu'),
            Dense(3, activation='linear')
        ])
        
        model.compile(
            optimizer=Adam(learning_rate=0.001),
            loss='mse'
        )
        
        return model
    
    def train_rl(self, df, episodes=100):
        """训练强化学习模型"""
        self.rl_model = self.build_rl_model()
        features = self.prepare_features(df)
        
        for episode in range(episodes):
            state = self._get_state(features, 0)
            total_reward = 0
            done = False
            step = 0
            
            while not done and step < len(features) - 1:
                # 选择动作
                action = self._choose_action(state)
                
                # 执行动作并获取奖励
                next_state = self._get_state(features, step + 1)
                reward = self._get_reward(action, features, step)
                
                # 存储经验
                self.memory.append((state, action, reward, next_state, done))
                
                # 训练模型
                if len(self.memory) > 32:
                    self._train_batch()
                
                state = next_state
                total_reward += reward
                step += 1
                
                if step >= len(features) - 1:
                    done = True
            
            print(f"Episode: {episode}, Total Reward: {total_reward}")
    
    def _get_state(self, features, step):
        """获取状态"""
        return features.iloc[step].values
    
    def _choose_action(self, state):
        """选择动作"""
        if random.random() < 0.1:  # 探索
            return random.randint(0, 2)
        else:  # 利用
            q_values = self.rl_model.predict(state.reshape(1, -1))
            return np.argmax(q_values[0])
    
    def _get_reward(self, action, features, step):
        """计算奖励"""
        if step >= len(features) - 1:
            return 0
            
        current_price = features.iloc[step]['close']
        next_price = features.iloc[step + 1]['close']
        price_change = (next_price - current_price) / current_price
        
        if action == 0:  # 买入
            return price_change
        elif action == 1:  # 卖出
            return -price_change
        else:  # 持有
            return 0
    
    def _train_batch(self):
        """训练批次"""
        batch = random.sample(self.memory, 32)
        states = np.array([x[0] for x in batch])
        actions = np.array([x[1] for x in batch])
        rewards = np.array([x[2] for x in batch])
        next_states = np.array([x[3] for x in batch])
        dones = np.array([x[4] for x in batch])
        
        # 计算目标Q值
        target_q = self.rl_model.predict(states)
        next_q = self.rl_model.predict(next_states)
        
        for i in range(32):
            if dones[i]:
                target_q[i][actions[i]] = rewards[i]
            else:
                target_q[i][actions[i]] = rewards[i] + 0.95 * np.max(next_q[i])
        
        # 训练模型
        self.rl_model.fit(states, target_q, verbose=0)
    
    def predict(self, df, model_type='ensemble'):
        """使用AI模型进行预测"""
        features = self.prepare_features(df)
        X = self.scaler.transform(features)
        
        if model_type == 'rf':
            return self.rf_model.predict(X)
        elif model_type == 'lstm':
            X_sequences = np.array([X[-60:]])
            return np.argmax(self.lstm_model.predict(X_sequences)[0])
        elif model_type == 'rl':
            state = self._get_state(features, -1)
            return self._choose_action(state)
        else:  # ensemble
            rf_pred = self.rf_model.predict(X)
            lstm_pred = np.argmax(self.lstm_model.predict(np.array([X[-60:]]))[0])
            rl_pred = self._choose_action(self._get_state(features, -1))
            
            # 投票决定最终预测
            predictions = [rf_pred[-1], lstm_pred, rl_pred]
            return max(set(predictions), key=predictions.count) 