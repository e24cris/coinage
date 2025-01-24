import os
import logging
import mlflow
import numpy as np
import pandas as pd
from datetime import datetime
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

class MLTrainingPipeline:
    def __init__(
        self, 
        data_path='backend/ml/data/investment_history.csv',
        model_save_path='backend/ml/models'
    ):
        """
        Initialize ML training pipeline
        
        Args:
            data_path: Path to training data
            model_save_path: Directory to save trained models
        """
        # Configure logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        
        # Ensure model directory exists
        os.makedirs(model_save_path, exist_ok=True)
        
        # Configuration
        self.data_path = data_path
        self.model_save_path = model_save_path
        
        # MLflow tracking
        mlflow.set_tracking_uri('file:///tmp/mlflow-tracking')
        mlflow.set_experiment('coinage_investment_prediction')
    
    def load_and_preprocess_data(self):
        """
        Load and preprocess training data
        
        Returns:
            Preprocessed training and testing datasets
        """
        # Load data
        data = pd.read_csv(self.data_path)
        
        # Select features and target
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
        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        X_test_scaled = scaler.transform(X_test)
        
        return {
            'X_train': X_train_scaled,
            'X_test': X_test_scaled,
            'y_train': y_train.values,
            'y_test': y_test.values,
            'scaler': scaler
        }
    
    def train_model(self, datasets):
        """
        Train RandomForest regression model
        
        Args:
            datasets: Preprocessed training datasets
        
        Returns:
            Trained model and performance metrics
        """
        # Start MLflow run
        with mlflow.start_run():
            # Initialize and train model
            model = RandomForestRegressor(
                n_estimators=100, 
                random_state=42
            )
            
            model.fit(
                datasets['X_train'], 
                datasets['y_train']
            )
            
            # Predict and evaluate
            y_pred = model.predict(datasets['X_test'])
            
            # Compute metrics
            metrics = {
                'mae': mean_absolute_error(datasets['y_test'], y_pred),
                'mse': mean_squared_error(datasets['y_test'], y_pred),
                'r2_score': r2_score(datasets['y_test'], y_pred)
            }
            
            # Log metrics to MLflow
            for metric_name, metric_value in metrics.items():
                mlflow.log_metric(metric_name, metric_value)
            
            # Log model parameters
            mlflow.log_params(model.get_params())
            
            return model, metrics
    
    def save_model(self, model, scaler):
        """
        Save trained model and scaler
        
        Args:
            model: Trained RandomForest model
            scaler: Feature scaler
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        model_filename = f'investment_predictor_{timestamp}.joblib'
        scaler_filename = f'feature_scaler_{timestamp}.joblib'
        
        model_path = os.path.join(self.model_save_path, model_filename)
        scaler_path = os.path.join(self.model_save_path, scaler_filename)
        
        import joblib
        joblib.dump(model, model_path)
        joblib.dump(scaler, scaler_path)
        
        self.logger.info(f"Model saved to {model_path}")
        self.logger.info(f"Scaler saved to {scaler_path}")
    
    def run_training_pipeline(self):
        """
        Execute complete ML training pipeline
        """
        self.logger.info("Starting ML Training Pipeline")
        
        # Load and preprocess data
        datasets = self.load_and_preprocess_data()
        
        # Train model
        model, metrics = self.train_model(datasets)
        
        # Save model and scaler
        self.save_model(model, datasets['scaler'])
        
        # Log training results
        self.logger.info("Model Training Metrics:")
        for metric, value in metrics.items():
            self.logger.info(f"{metric}: {value}")

def main():
    """
    Run ML training pipeline
    """
    training_pipeline = MLTrainingPipeline()
    training_pipeline.run_training_pipeline()

if __name__ == '__main__':
    main()
