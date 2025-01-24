import os
import numpy as np
import pandas as pd
import joblib
from typing import Dict, List, Any

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

class InvestmentPredictionModel:
    def __init__(
        self, 
        model_path='models/investment_predictor.joblib',
        data_path='data/investment_history.csv'
    ):
        """
        Initialize investment prediction model
        
        Args:
            model_path: Path to save/load trained model
            data_path: Path to investment historical data
        """
        self.model_path = model_path
        self.data_path = data_path
        self.model = None
        self.scaler = StandardScaler()
        
        # Ensure model directory exists
        os.makedirs(os.path.dirname(model_path), exist_ok=True)
    
    def load_data(self) -> pd.DataFrame:
        """
        Load investment historical data
        
        Returns:
            Preprocessed investment data
        """
        data = pd.read_csv(self.data_path)
        
        # Basic preprocessing
        data.dropna(inplace=True)
        
        return data
    
    def prepare_features(
        self, 
        data: pd.DataFrame
    ) -> Dict[str, np.ndarray]:
        """
        Prepare features and target for model training
        
        Args:
            data: Investment historical data
        
        Returns:
            Dictionary of training and testing datasets
        """
        # Select relevant features
        features = [
            'market_volatility', 
            'historical_returns', 
            'risk_level', 
            'investment_duration'
        ]
        target = 'expected_return'
        
        X = data[features]
        y = data[target]
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
        
        # Scale features
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)
        
        return {
            'X_train': X_train_scaled,
            'X_test': X_test_scaled,
            'y_train': y_train.values,
            'y_test': y_test.values
        }
    
    def train_model(self) -> Dict[str, Any]:
        """
        Train RandomForest investment prediction model
        
        Returns:
            Model training metrics
        """
        data = self.load_data()
        datasets = self.prepare_features(data)
        
        # Initialize and train model
        self.model = RandomForestRegressor(
            n_estimators=100, 
            random_state=42
        )
        
        self.model.fit(
            datasets['X_train'], 
            datasets['y_train']
        )
        
        # Predict and evaluate
        y_pred = self.model.predict(datasets['X_test'])
        
        metrics = {
            'mae': mean_absolute_error(datasets['y_test'], y_pred),
            'mse': mean_squared_error(datasets['y_test'], y_pred),
            'r2_score': r2_score(datasets['y_test'], y_pred)
        }
        
        # Save model
        joblib.dump(self.model, self.model_path)
        
        return metrics
    
    def predict_investment_return(
        self, 
        investment_features: List[float]
    ) -> float:
        """
        Predict investment return
        
        Args:
            investment_features: List of feature values
        
        Returns:
            Predicted investment return
        """
        # Load model if not already loaded
        if self.model is None:
            self.model = joblib.load(self.model_path)
        
        # Scale features
        scaled_features = self.scaler.transform([investment_features])
        
        # Predict
        return float(self.model.predict(scaled_features)[0])

def main():
    """
    Demonstrate investment prediction model
    """
    model = InvestmentPredictionModel()
    
    # Train model
    training_metrics = model.train_model()
    print("Model Training Metrics:")
    print(training_metrics)
    
    # Example prediction
    sample_investment = [
        0.5,   # market_volatility
        0.07,  # historical_returns
        3,     # risk_level
        5      # investment_duration
    ]
    
    predicted_return = model.predict_investment_return(sample_investment)
    print(f"\nPredicted Investment Return: {predicted_return:.2%}")

if __name__ == '__main__':
    main()
