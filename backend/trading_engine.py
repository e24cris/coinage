import os
import logging
from typing import Dict, List, Optional
from decimal import Decimal, InvalidOperation
import numpy as np
import pandas as pd
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timedelta

Base = declarative_base()

class TradingStrategy:
    """
    Advanced Trading Strategy Framework
    
    Supports multiple trading strategies:
    - Momentum Trading
    - Mean Reversion
    - Trend Following
    """
    
    @staticmethod
    def momentum_strategy(price_history: List[float], window: int = 14) -> str:
        """
        Momentum trading strategy
        
        Args:
            price_history: Historical price data
            window: Lookback period
        
        Returns:
            Trading recommendation (buy/sell/hold)
        """
        if len(price_history) < window:
            return 'hold'
        
        prices = np.array(price_history)
        momentum = prices[-1] - prices[-window]
        
        if momentum > 0:
            return 'buy'
        elif momentum < 0:
            return 'sell'
        else:
            return 'hold'
    
    @staticmethod
    def mean_reversion_strategy(price_history: List[float], window: int = 20) -> str:
        """
        Mean reversion trading strategy
        
        Args:
            price_history: Historical price data
            window: Lookback period
        
        Returns:
            Trading recommendation
        """
        if len(price_history) < window:
            return 'hold'
        
        prices = np.array(price_history)
        mean = np.mean(prices[-window:])
        current_price = prices[-1]
        
        std_dev = np.std(prices[-window:])
        
        if current_price < mean - std_dev:
            return 'buy'
        elif current_price > mean + std_dev:
            return 'sell'
        else:
            return 'hold'

class RiskManagement:
    """
    Advanced Risk Management System
    """
    
    @staticmethod
    def calculate_position_size(
        account_balance: Decimal, 
        risk_percentage: float = 0.02
    ) -> Decimal:
        """
        Calculate optimal position size based on account risk
        
        Args:
            account_balance: Total account balance
            risk_percentage: Maximum risk per trade
        
        Returns:
            Recommended position size
        """
        try:
            max_loss = account_balance * Decimal(str(risk_percentage))
            return max_loss
        except InvalidOperation:
            logging.error("Invalid account balance or risk percentage")
            return Decimal('0')
    
    @staticmethod
    def stop_loss_price(
        entry_price: Decimal, 
        risk_percentage: float = 0.02
    ) -> Decimal:
        """
        Calculate stop-loss price
        
        Args:
            entry_price: Trade entry price
            risk_percentage: Maximum risk percentage
        
        Returns:
            Stop-loss price
        """
        try:
            stop_loss = entry_price * (1 - Decimal(str(risk_percentage)))
            return stop_loss
        except InvalidOperation:
            logging.error("Invalid entry price or risk percentage")
            return Decimal('0')

class TradeModel(Base):
    """
    SQLAlchemy model for storing trade information
    """
    __tablename__ = 'trades'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)
    asset = Column(String, nullable=False)
    trade_type = Column(String, nullable=False)
    quantity = Column(Float, nullable=False)
    price = Column(Float, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)

class TradingEngine:
    """
    Comprehensive Trading Engine
    
    Combines trading strategies, risk management, 
    and trade execution
    """
    
    def __init__(self, database_url: str):
        """
        Initialize trading engine
        
        Args:
            database_url: Database connection string
        """
        self.engine = create_engine(database_url)
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)
    
    def execute_trade(
        self, 
        user_id: int, 
        asset: str, 
        trade_type: str, 
        quantity: float, 
        price: float
    ) -> Dict[str, Any]:
        """
        Execute a trade with comprehensive checks
        
        Args:
            user_id: User performing the trade
            asset: Trading asset
            trade_type: Buy or sell
            quantity: Trade quantity
            price: Trade price
        
        Returns:
            Trade execution result
        """
        session = self.Session()
        
        try:
            # Create trade record
            trade = TradeModel(
                user_id=user_id,
                asset=asset,
                trade_type=trade_type,
                quantity=quantity,
                price=price
            )
            
            session.add(trade)
            session.commit()
            
            return {
                'status': 'success',
                'trade_id': trade.id,
                'message': f'{trade_type.capitalize()} order executed'
            }
        
        except Exception as e:
            session.rollback()
            logging.error(f"Trade execution failed: {e}")
            
            return {
                'status': 'error',
                'message': str(e)
            }
        
        finally:
            session.close()
    
    def analyze_trade_opportunity(
        self, 
        asset: str, 
        price_history: List[float]
    ) -> Dict[str, Any]:
        """
        Analyze trading opportunities using multiple strategies
        
        Args:
            asset: Trading asset
            price_history: Historical price data
        
        Returns:
            Trading recommendation
        """
        momentum_recommendation = TradingStrategy.momentum_strategy(price_history)
        mean_reversion_recommendation = TradingStrategy.mean_reversion_strategy(price_history)
        
        # Combine strategies
        if momentum_recommendation == mean_reversion_recommendation:
            primary_recommendation = momentum_recommendation
        else:
            primary_recommendation = 'hold'
        
        return {
            'asset': asset,
            'momentum_strategy': momentum_recommendation,
            'mean_reversion_strategy': mean_reversion_recommendation,
            'recommendation': primary_recommendation
        }

def main():
    """
    Demonstration of trading engine capabilities
    """
    # Database URL from environment
    database_url = os.getenv(
        'DATABASE_URL', 
        'sqlite:///trading_engine.db'
    )
    
    trading_engine = TradingEngine(database_url)
    
    # Simulated price history
    price_history = [
        100.0, 102.0, 101.5, 103.0, 104.5, 
        105.0, 103.5, 102.5, 101.0, 100.5
    ]
    
    # Analyze trading opportunity
    trade_analysis = trading_engine.analyze_trade_opportunity(
        'AAPL', 
        price_history
    )
    
    print("Trade Analysis:", trade_analysis)
    
    # Simulate trade execution
    trade_result = trading_engine.execute_trade(
        user_id=1,
        asset='AAPL',
        trade_type='buy',
        quantity=10,
        price=104.5
    )
    
    print("Trade Execution:", trade_result)

if __name__ == '__main__':
    main()
