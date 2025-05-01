import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
import time

class AIModels:
    def __init__(self):
        self.rf_model = RandomForestClassifier(
            n_estimators=100,
            max_depth=10,
            min_samples_split=5
        )
        self.scaler = StandardScaler()
        self.is_trained = False
        
    def _prepare_data(self, df):
        """Prepare features for training"""
        if len(df) < 20:  # Need at least 20 data points
            return np.array([]), np.array([])
            
        features = []
        for i in range(len(df)-10):
            window = df.iloc[i:i+10]
            if len(window) < 10:  # Skip if window is too small
                continue
                
            try:
                feature = [
                    window['close'].pct_change().mean(),
                    window['volume'].pct_change().mean(),
                    window['rsi'].iloc[-1],
                    window['macd'].iloc[-1],
                    window['macd_hist'].iloc[-1],
                    (window['close'].iloc[-1] - window['ma'].iloc[-1]) / window['ma'].iloc[-1],
                    (window['close'].iloc[-1] - window['bb_middle'].iloc[-1]) / window['bb_middle'].iloc[-1]
                ]
                features.append(feature)
            except (KeyError, IndexError, ZeroDivisionError):
                continue
            
        if not features:  # No valid features
            return np.array([]), np.array([])
            
        X = np.array(features)
        y = np.where(df['close'].pct_change().shift(-1).iloc[10:] > 0, 1, 0)
        
        # Make sure X and y have the same length
        min_len = min(len(X), len(y))
        X = X[:min_len]
        y = y[:min_len]
        
        return X, y
        
    def train_random_forest(self, df):
        """Train the random forest model"""
        start_time = time.time()
        
        X, y = self._prepare_data(df)
        if len(X) == 0 or len(y) == 0:
            print("Not enough data for training")
            return 0
            
        if len(X) < 20:  # Need at least 20 samples for meaningful training
            print("Not enough samples for training")
            return 0
            
        try:
            X = self.scaler.fit_transform(X)
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=False)
            
            self.rf_model.fit(X_train, y_train)
            accuracy = self.rf_model.score(X_test, y_test)
            self.is_trained = True
            
            training_time = time.time() - start_time
            print(f"Training completed in {training_time:.2f} seconds")
            
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