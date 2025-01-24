import os
import logging
import mlflow
import joblib
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
import numpy as np
import pandas as pd

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MLModelDeployment:
    def __init__(self, model_dir='backend/ml/models'):
        """
        Initialize ML Model Deployment
        
        Args:
            model_dir: Directory to save models
        """
        os.makedirs(model_dir, exist_ok=True)
        self.model_dir = model_dir
        
        # MLflow tracking setup
        mlflow.set_tracking_uri('file:///mlflow-tracking')
        mlflow.set_experiment('Coinage Investment Prediction')
    
    def prepare_training_data(self):
        """
        Prepare synthetic training data for investment prediction
        
        Returns:
            Training and testing datasets
        """
        np.random.seed(42)
        
        # Simulate investment features
        n_samples = 1000
        features = {
            'age': np.random.normal(35, 10, n_samples),
            'income': np.random.normal(75000, 25000, n_samples),
            'risk_tolerance': np.random.uniform(0, 1, n_samples),
            'investment_history': np.random.randint(0, 20, n_samples)
        }
        
        df = pd.DataFrame(features)
        
        # Synthetic target: investment return
        df['investment_return'] = (
            0.5 * df['age'] + 
            0.3 * df['income'] / 10000 + 
            20 * df['risk_tolerance'] - 
            0.2 * df['investment_history'] + 
            np.random.normal(0, 5, n_samples)
        )
        
        return train_test_split(
            df.drop('investment_return', axis=1), 
            df['investment_return'], 
            test_size=0.2
        )
    
    def train_model(self):
        """
        Train investment prediction model
        
        Returns:
            Trained model and performance metrics
        """
        X_train, X_test, y_train, y_test = self.prepare_training_data()
        
        with mlflow.start_run():
            # Train Random Forest Regressor
            model = RandomForestRegressor(
                n_estimators=100, 
                random_state=42
            )
            model.fit(X_train, y_train)
            
            # Predict and evaluate
            y_pred = model.predict(X_test)
            mse = mean_squared_error(y_test, y_pred)
            r2 = r2_score(y_test, y_pred)
            
            # Log metrics
            mlflow.log_metrics({
                'mse': mse,
                'r2_score': r2
            })
            
            # Log model
            mlflow.sklearn.log_model(
                model, 
                'investment_predictor',
                registered_model_name='CoinageInvestmentPredictor'
            )
        
        return model, {'mse': mse, 'r2_score': r2}
    
    def save_model(self, model):
        """
        Save model to local file
        
        Args:
            model: Trained ML model
        """
        model_path = os.path.join(self.model_dir, 'investment_predictor.pkl')
        joblib.dump(model, model_path)
        logger.info(f"Model saved to {model_path}")
    
    def deploy_ml_service(self):
        """
        Deploy machine learning service
        
        Returns:
            Boolean indicating successful deployment
        """
        logger.info("Starting ML Model Deployment")
        
        try:
            # Train model
            model, metrics = self.train_model()
            
            # Save model
            self.save_model(model)
            
            logger.info("ML Model Deployment Successful")
            logger.info(f"Model Performance - MSE: {metrics['mse']}, R2: {metrics['r2_score']}")
            
            return True
        except Exception as e:
            logger.error(f"ML Model Deployment Failed: {e}")
            return False

def main():
    """
    Main ML service deployment script
    """
    ml_deployer = MLModelDeployment()
    result = ml_deployer.deploy_ml_service()
    
    return result

if __name__ == '__main__':
    main()
