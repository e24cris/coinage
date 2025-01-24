import pytest
import numpy as np
from decimal import Decimal

from backend.trading_engine import (
    TradingStrategy, 
    RiskManagement, 
    TradingEngine
)

class TestTradingStrategy:
    def test_momentum_strategy(self):
        price_history_bullish = [100, 102, 104, 106, 108]
        price_history_bearish = [100, 98, 96, 94, 92]
        price_history_neutral = [100, 101, 100, 99, 100]

        assert TradingStrategy.momentum_strategy(price_history_bullish) == 'buy'
        assert TradingStrategy.momentum_strategy(price_history_bearish) == 'sell'
        assert TradingStrategy.momentum_strategy(price_history_neutral) == 'hold'

    def test_mean_reversion_strategy(self):
        price_history_buy = [100, 95, 90, 85, 80]
        price_history_sell = [100, 105, 110, 115, 120]
        price_history_hold = [100, 98, 99, 101, 100]

        assert TradingStrategy.mean_reversion_strategy(price_history_buy) == 'buy'
        assert TradingStrategy.mean_reversion_strategy(price_history_sell) == 'sell'
        assert TradingStrategy.mean_reversion_strategy(price_history_hold) == 'hold'

class TestRiskManagement:
    def test_position_size_calculation(self):
        account_balance = Decimal('10000')
        risk_percentage = 0.02

        position_size = RiskManagement.calculate_position_size(
            account_balance, 
            risk_percentage
        )

        assert position_size == Decimal('200')
        assert position_size <= account_balance

    def test_stop_loss_price(self):
        entry_price = Decimal('100')
        risk_percentage = 0.02

        stop_loss = RiskManagement.stop_loss_price(
            entry_price, 
            risk_percentage
        )

        assert stop_loss == Decimal('98')

class TestTradingEngine:
    @pytest.fixture
    def trading_engine(self):
        return TradingEngine('sqlite:///test_trading.db')

    def test_trade_execution(self, trading_engine):
        trade_result = trading_engine.execute_trade(
            user_id=1,
            asset='AAPL',
            trade_type='buy',
            quantity=10,
            price=150.50
        )

        assert trade_result['status'] == 'success'
        assert 'trade_id' in trade_result

    def test_trade_analysis(self, trading_engine):
        price_history = [100, 102, 101, 103, 104]
        
        trade_analysis = trading_engine.analyze_trade_opportunity(
            'AAPL', 
            price_history
        )

        assert 'asset' in trade_analysis
        assert 'recommendation' in trade_analysis
        assert trade_analysis['recommendation'] in ['buy', 'sell', 'hold']

    def test_invalid_trade_execution(self, trading_engine):
        with pytest.raises(ValueError):
            trading_engine.execute_trade(
                user_id=None,
                asset='',
                trade_type='invalid',
                quantity=-1,
                price=0
            )

def test_random_trade_strategy():
    """Property-based testing for trading strategies"""
    np.random.seed(42)
    
    for _ in range(100):
        price_history = np.random.normal(100, 10, 20).tolist()
        
        momentum_result = TradingStrategy.momentum_strategy(price_history)
        mean_reversion_result = TradingStrategy.mean_reversion_strategy(price_history)
        
        assert momentum_result in ['buy', 'sell', 'hold']
        assert mean_reversion_result in ['buy', 'sell', 'hold']
