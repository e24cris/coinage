import os
import uuid
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta

from sqlalchemy import Column, Integer, String, Float, DateTime, JSON, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

Base = declarative_base()

class InvestmentPlan(Base):
    """
    Comprehensive Investment Plan Model
    
    Supports various investment strategies and configurations
    """
    __tablename__ = 'investment_plans'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    description = Column(String(500))
    
    # Plan Configuration
    risk_level = Column(String(20))  # low, medium, high
    min_investment = Column(Float, default=0)
    max_investment = Column(Float, nullable=True)
    
    # Asset Allocation
    asset_allocation = Column(JSON)  # Flexible JSON for asset distribution
    
    # Performance Metrics
    expected_return = Column(Float)
    volatility = Column(Float)
    
    # Temporal Configurations
    investment_duration = Column(Integer)  # in months
    rebalancing_frequency = Column(String(20))  # monthly, quarterly, annually
    
    # Compliance and Restrictions
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class InvestmentPlanManager:
    """
    Investment Plan Management Service
    
    Handles creation, modification, and management of investment plans
    """
    
    def __init__(self, database_url: Optional[str] = None):
        """
        Initialize Investment Plan Manager
        
        Args:
            database_url: Database connection string
        """
        self.database_url = database_url or os.getenv(
            'DATABASE_URL', 
            'sqlite:///investment_plans.db'
        )
        
        # Create engine and session
        self.engine = create_engine(self.database_url)
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)
    
    def create_investment_plan(
        self, 
        name: str, 
        description: str,
        risk_level: str = 'medium',
        min_investment: float = 1000.0,
        max_investment: Optional[float] = None,
        asset_allocation: Dict[str, float] = None,
        expected_return: float = 0.05,
        volatility: float = 0.1,
        investment_duration: int = 12,
        rebalancing_frequency: str = 'quarterly'
    ) -> Dict[str, Any]:
        """
        Create a new investment plan
        
        Args:
            name: Plan name
            description: Plan description
            risk_level: Risk classification
            min_investment: Minimum investment amount
            max_investment: Maximum investment amount
            asset_allocation: Distribution across assets
            expected_return: Projected annual return
            volatility: Expected price fluctuation
            investment_duration: Plan duration in months
            rebalancing_frequency: Portfolio rebalancing interval
        
        Returns:
            Created investment plan details
        """
        # Default asset allocation if not provided
        if asset_allocation is None:
            asset_allocation = {
                'stocks': 0.6,
                'bonds': 0.3,
                'cash': 0.1
            }
        
        # Validate inputs
        if not (0 <= sum(asset_allocation.values()) <= 1):
            raise ValueError("Asset allocation must total 1.0 or less")
        
        # Create investment plan
        investment_plan = InvestmentPlan(
            name=name,
            description=description,
            risk_level=risk_level,
            min_investment=min_investment,
            max_investment=max_investment,
            asset_allocation=asset_allocation,
            expected_return=expected_return,
            volatility=volatility,
            investment_duration=investment_duration,
            rebalancing_frequency=rebalancing_frequency
        )
        
        # Save to database
        session = self.Session()
        try:
            session.add(investment_plan)
            session.commit()
            
            return {
                'id': investment_plan.id,
                'name': investment_plan.name,
                'status': 'created',
                'created_at': investment_plan.created_at.isoformat()
            }
        except Exception as e:
            session.rollback()
            raise ValueError(f"Failed to create investment plan: {e}")
        finally:
            session.close()
    
    def get_investment_plans(
        self, 
        risk_level: Optional[str] = None,
        min_investment: Optional[float] = None
    ) -> List[Dict[str, Any]]:
        """
        Retrieve investment plans
        
        Args:
            risk_level: Filter by risk level
            min_investment: Minimum investment threshold
        
        Returns:
            List of investment plans
        """
        session = self.Session()
        try:
            query = session.query(InvestmentPlan)
            
            if risk_level:
                query = query.filter(InvestmentPlan.risk_level == risk_level)
            
            if min_investment is not None:
                query = query.filter(
                    InvestmentPlan.min_investment <= min_investment
                )
            
            plans = query.all()
            
            return [
                {
                    'id': plan.id,
                    'name': plan.name,
                    'description': plan.description,
                    'risk_level': plan.risk_level,
                    'min_investment': plan.min_investment,
                    'expected_return': plan.expected_return,
                    'asset_allocation': plan.asset_allocation
                }
                for plan in plans
            ]
        finally:
            session.close()
    
    def update_investment_plan(
        self, 
        plan_id: int, 
        **kwargs
    ) -> Dict[str, Any]:
        """
        Update an existing investment plan
        
        Args:
            plan_id: Investment plan identifier
            **kwargs: Fields to update
        
        Returns:
            Updated investment plan details
        """
        session = self.Session()
        try:
            plan = session.query(InvestmentPlan).get(plan_id)
            
            if not plan:
                raise ValueError(f"Investment plan {plan_id} not found")
            
            # Update allowed fields
            allowed_fields = [
                'name', 'description', 'risk_level', 
                'min_investment', 'max_investment',
                'asset_allocation', 'expected_return',
                'volatility', 'investment_duration',
                'rebalancing_frequency', 'is_active'
            ]
            
            for key, value in kwargs.items():
                if key in allowed_fields:
                    setattr(plan, key, value)
            
            session.commit()
            
            return {
                'id': plan.id,
                'name': plan.name,
                'status': 'updated',
                'updated_at': plan.updated_at.isoformat()
            }
        except Exception as e:
            session.rollback()
            raise ValueError(f"Failed to update investment plan: {e}")
        finally:
            session.close()

def main():
    """
    Demonstrate investment plan management
    """
    # Initialize investment plan manager
    plan_manager = InvestmentPlanManager()
    
    # Create an investment plan
    growth_plan = plan_manager.create_investment_plan(
        name='Aggressive Growth Plan',
        description='High-risk plan targeting maximum returns',
        risk_level='high',
        min_investment=5000.0,
        asset_allocation={
            'stocks': 0.8,
            'crypto': 0.15,
            'cash': 0.05
        },
        expected_return=0.12,
        volatility=0.25,
        investment_duration=24,
        rebalancing_frequency='quarterly'
    )
    
    print("Created Investment Plan:", growth_plan)
    
    # Retrieve investment plans
    plans = plan_manager.get_investment_plans(
        risk_level='high',
        min_investment=3000.0
    )
    
    print("\nAvailable High-Risk Plans:")
    for plan in plans:
        print(plan)

if __name__ == '__main__':
    main()
