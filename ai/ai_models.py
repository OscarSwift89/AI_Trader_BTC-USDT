import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
import time

class AIModels:
    def __init__(self):
        self.rf_model = RandomForestClassifier(
            n_estimators=200,
            max_depth=15,
            min_samples_split=10,
            min_samples_leaf=5,
            random_state=42
        )
        self.scaler = StandardScaler()
        self.is_trained = False
        
    def _prepare_data(self, df):
        """Prepare features for training"""
        if len(df) < 10:  # Reduce minimum required data points
            return np.array([]), np.array([])
            
        features = []
        labels = []
        
        # Calculate returns for labeling
        returns = df['close'].pct_change()
        
        # Calculate additional features
        volatility = df['close'].rolling(window=10).std()  # Reduce window size
        volume_ma = df['volume'].rolling(window=10).mean()
        price_ma = df['close'].rolling(window=10).mean()
        
        for i in range(10, len(df)-5):  # Reduce lookback and prediction windows
            window = df.iloc[i-10:i]
            future_window = df.iloc[i:i+5]
            
            if len(window) < 10 or len(future_window) < 5:
                continue
                
            try:
                # Create more focused features
                feature = [
                    # Price momentum
                    window['close'].pct_change().mean(),
                    window['close'].pct_change().std(),
                    
                    # Volume analysis
                    window['volume'].pct_change().mean(),
                    
                    # Technical indicators
                    window['rsi'].iloc[-1],
                    window['macd'].iloc[-1],
                    window['macd_hist'].iloc[-1],
                    
                    # Price relative to moving averages
                    (window['close'].iloc[-1] - window['ma'].iloc[-1]) / window['ma'].iloc[-1],
                    
                    # Bollinger Bands
                    (window['close'].iloc[-1] - window['bb_middle'].iloc[-1]) / window['bb_std'].iloc[-1],
                    
                    # Volatility
                    volatility.iloc[i] / window['close'].iloc[-1]
                ]
                
                # Calculate future return for labeling
                future_return = (future_window['close'].iloc[-1] / window['close'].iloc[-1] - 1)
                
                # Create label based on future return with fixed threshold
                threshold = 0.01  # 1% threshold
                if future_return > threshold:
                    label = 1  # Buy
                elif future_return < -threshold:
                    label = 0  # Sell
                else:
                    label = 2  # Hold
                
                features.append(feature)
                labels.append(label)
                
            except (KeyError, IndexError, ZeroDivisionError) as e:
                continue
            
        if not features:  # No valid features
            return np.array([]), np.array([])
            
        X = np.array(features)
        y = np.array(labels)
        
        # Remove hold signals
        mask = y != 2
        X = X[mask]
        y = y[mask]
        
        if len(X) < 10:  # Ensure minimum number of samples
            return np.array([]), np.array([])
        
        return X, y
        
    def train_random_forest(self, df):
        """Train the random forest model"""
        start_time = time.time()
        
        X, y = self._prepare_data(df)
        if len(X) == 0 or len(y) == 0:
            print("Not enough data for training")
            return 0
            
        try:
            # Scale features
            X = self.scaler.fit_transform(X)
            
            # Split data with shuffle
            X_train, X_test, y_train, y_test = train_test_split(
                X, y, 
                test_size=0.2,
                shuffle=True,
                random_state=42
            )
            
            # Update model with simpler parameters
            self.rf_model = RandomForestClassifier(
                n_estimators=100,
                max_depth=5,
                min_samples_split=5,
                min_samples_leaf=2,
                random_state=42,
                n_jobs=-1
            )
            
            # Train model
            self.rf_model.fit(X_train, y_train)
            
            # Calculate accuracy
            accuracy = self.rf_model.score(X_test, y_test)
            self.is_trained = True
            
            training_time = time.time() - start_time
            print(f"Training completed in {training_time:.2f} seconds")
            print(f"Number of training samples: {len(X_train)}")
            print(f"Class distribution: Buy signals: {sum(y == 1)}, Sell signals: {sum(y == 0)}")
            
            return accuracy
            
        except Exception as e:
            print(f"Error during training: {e}")
            return 0
        
    def predict(self, df):
        """Make predictions"""
        if not self.is_trained:
            return 0
            
        try:
            X, _ = self._prepare_data(df.iloc[-11:])
            if len(X) == 0:
                return 0
                
            X = self.scaler.transform(X)
            pred = self.rf_model.predict(X)
            return pred[-1]
        except Exception as e:
            print(f"Error during prediction: {e}")
            return 0 