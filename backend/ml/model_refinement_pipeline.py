import os
import logging
import numpy as np
import pandas as pd
import mlflow
import mlflow.sklearn
from typing import Dict, Any, List

from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

class ModelRefinementPipeline:
    def __init__(
        self, 
        data_path: str = 'backend/ml/data/investment_history.csv',
        model_save_dir: str = 'backend/ml/models/refined'
    ):
        """
        Initialize Model Refinement Pipeline
        
        Args:
            data_path: Path to investment history dataset
            model_save_dir: Directory to save refined models
        """
        # Configure logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)
        
        # Ensure model save directory exists
        os.makedirs(model_save_dir, exist_ok=True)
        
        # Configuration
        self.data_path = data_path
        self.model_save_dir = model_save_dir
        
        # MLflow tracking
        mlflow.set_tracking_uri('file:///tmp/mlflow-tracking')
        mlflow.set_experiment('coinage_model_refinement')
    
    def load_and_preprocess_data(self) -> Dict[str, Any]:
        """
        Load and preprocess investment history data
        
        Returns:
            Preprocessed dataset with train/test splits
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
        
        return {
            'X_train': X_train,
            'X_test': X_test,
            'y_train': y_train,
            'y_test': y_test
        }
    
    def create_model_pipeline(self) -> Pipeline:
        """
        Create machine learning model pipeline
        
        Returns:
            Scikit-learn pipeline with preprocessing and model
        """
        pipeline = Pipeline([
            ('scaler', StandardScaler()),
            ('regressor', RandomForestRegressor(random_state=42))
        ])
        
        return pipeline
    
    def hyperparameter_tuning(self, pipeline: Pipeline, X_train, y_train) -> Dict[str, Any]:
        """
        Perform hyperparameter tuning using GridSearchCV
        
        Args:
            pipeline: Scikit-learn pipeline
            X_train: Training features
            y_train: Training target
        
        Returns:
            Best hyperparameters and model
        """
        param_grid = {
            'regressor__n_estimators': [50, 100, 200],
            'regressor__max_depth': [None, 10, 20],
            'regressor__min_samples_split': [2, 5, 10]
        }
        
        grid_search = GridSearchCV(
            pipeline, 
            param_grid, 
            cv=5, 
            scoring='neg_mean_absolute_error'
        )
        
        grid_search.fit(X_train, y_train)
        
        return {
            'best_params': grid_search.best_params_,
            'best_model': grid_search.best_estimator_
        }
    
    def evaluate_model(self, model, X_test, y_test) -> Dict[str, float]:
        """
        Evaluate model performance
        
        Args:
            model: Trained model
            X_test: Test features
            y_test: Test target
        
        Returns:
            Performance metrics
        """
        y_pred = model.predict(X_test)
        
        metrics = {
            'mae': mean_absolute_error(y_test, y_pred),
            'mse': mean_squared_error(y_test, y_pred),
            'r2_score': r2_score(y_test, y_pred)
        }
        
        return metrics
    
    def cross_validation(self, model, X, y) -> Dict[str, Any]:
        """
        Perform cross-validation
        
        Args:
            model: Trained model
            X: Features
            y: Target
        
        Returns:
            Cross-validation results
        """
        cv_scores = cross_val_score(
            model, 
            X, 
            y, 
            cv=5, 
            scoring='neg_mean_absolute_error'
        )
        
        return {
            'cv_scores': cv_scores.tolist(),
            'mean_cv_score': np.mean(cv_scores),
            'std_cv_score': np.std(cv_scores)
        }
    
    def save_model(self, model, metrics: Dict[str, float]):
        """
        Save refined model with performance metrics
        
        Args:
            model: Trained model
            metrics: Model performance metrics
        """
        import joblib
        from datetime import datetime
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        model_filename = f'refined_investment_predictor_{timestamp}.joblib'
        model_path = os.path.join(self.model_save_dir, model_filename)
        
        # Save model
        joblib.dump(model, model_path)
        
        # Log model with MLflow
        with mlflow.start_run():
            mlflow.log_metrics(metrics)
            mlflow.log_params(model.named_steps['regressor'].get_params())
            mlflow.sklearn.log_model(model, "refined_model")
        
        self.logger.info(f"Refined model saved to {model_path}")
    
    def run_refinement_pipeline(self) -> Dict[str, Any]:
        """
        Execute complete model refinement pipeline
        
        Returns:
            Refinement results and metrics
        """
        self.logger.info("Starting Model Refinement Pipeline")
        
        # Load and preprocess data
        datasets = self.load_and_preprocess_data()
        
        # Create model pipeline
        model_pipeline = self.create_model_pipeline()
        
        # Hyperparameter tuning
        tuning_results = self.hyperparameter_tuning(
            model_pipeline, 
            datasets['X_train'], 
            datasets['y_train']
        )
        
        # Evaluate model
        performance_metrics = self.evaluate_model(
            tuning_results['best_model'],
            datasets['X_test'], 
            datasets['y_test']
        )
        
        # Cross-validation
        cv_results = self.cross_validation(
            tuning_results['best_model'], 
            pd.concat([datasets['X_train'], datasets['X_test']]),
            pd.concat([datasets['y_train'], datasets['y_test']])
        )
        
        # Save refined model
        self.save_model(
            tuning_results['best_model'], 
            performance_metrics
        )
        
        refinement_report = {
            'best_hyperparameters': tuning_results['best_params'],
            'performance_metrics': performance_metrics,
            'cross_validation_results': cv_results
        }
        
        # Log refinement results
        self.logger.info("Model Refinement Completed")
        self.logger.info(f"Refinement Report: {refinement_report}")
        
        return refinement_report

def main():
    """
    Run model refinement pipeline
    """
    refinement_pipeline = ModelRefinementPipeline()
    refinement_results = refinement_pipeline.run_refinement_pipeline()
    
    # Generate refinement report
    with open('model_refinement_report.json', 'w') as f:
        import json
        json.dump(refinement_results, f, indent=2)

if __name__ == '__main__':
    main()
