import logging
from datetime import datetime, timedelta
from reporting_service import PerformanceReportGenerator

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def generate_daily_performance_report():
    """Generate comprehensive daily performance report"""
    try:
        report_generator = PerformanceReportGenerator()
        start_date = datetime.now() - timedelta(days=1)
        end_date = datetime.now()
        
        performance_report = report_generator.generate_report(start_date, end_date)
        report_generator.save_report(performance_report)
        report_generator.distribute_report(performance_report)
        
        logger.info(f"Daily performance report generated at {datetime.now()}")
    except Exception as e:
        logger.error(f"Report generation failed: {e}")

if __name__ == "__main__":
    generate_daily_performance_report()
