import logging
from datetime import datetime
from sqlalchemy import create_engine
from investment_plan_optimizer import InvestmentPlanPerformanceOptimizer

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def daily_portfolio_rebalancing():
    """Automated daily investment portfolio rebalancing"""
    try:
        optimizer = InvestmentPlanPerformanceOptimizer()
        plans = optimizer.get_active_investment_plans()
        
        for plan in plans:
            optimized_plan = optimizer.optimize_plan_performance(plan.id)
            logger.info(f"Rebalanced plan: {plan.name}")
        
        logger.info(f"Daily rebalancing completed at {datetime.now()}")
    except Exception as e:
        logger.error(f"Rebalancing failed: {e}")

if __name__ == "__main__":
    daily_portfolio_rebalancing()
