import logging
from datetime import datetime
from market_data_service import MarketDataService

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def hourly_market_sync():
    """Synchronize market data hourly"""
    try:
        market_service = MarketDataService()
        market_data = market_service.fetch_latest_market_data()
        market_service.update_market_data(market_data)
        
        logger.info(f"Market data synchronized at {datetime.now()}")
    except Exception as e:
        logger.error(f"Market sync failed: {e}")

if __name__ == "__main__":
    hourly_market_sync()
