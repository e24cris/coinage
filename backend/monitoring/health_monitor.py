import os
import sys
import psutil
import logging
import time
from prometheus_client import start_http_server, Gauge

class SystemHealthMonitor:
    def __init__(self):
        # CPU Metrics
        self.cpu_usage = Gauge('cpu_usage_percent', 'CPU Usage Percentage')
        self.memory_usage = Gauge('memory_usage_percent', 'Memory Usage Percentage')
        self.disk_usage = Gauge('disk_usage_percent', 'Disk Usage Percentage')
        
        # Application Metrics
        self.active_connections = Gauge('active_connections', 'Number of Active Connections')
        self.error_count = Gauge('error_count', 'Total Number of Errors')
        
        # Logging setup
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('system_health.log'),
                logging.StreamHandler(sys.stdout)
            ]
        )
        self.logger = logging.getLogger(__name__)

    def monitor_system_resources(self):
        """
        Continuously monitor system resources
        """
        while True:
            try:
                # CPU Usage
                cpu_percent = psutil.cpu_percent(interval=1)
                self.cpu_usage.set(cpu_percent)
                
                # Memory Usage
                memory = psutil.virtual_memory()
                self.memory_usage.set(memory.percent)
                
                # Disk Usage
                disk = psutil.disk_usage('/')
                self.disk_usage.set(disk.percent)
                
                # Log high resource usage
                if cpu_percent > 80:
                    self.logger.warning(f"High CPU Usage: {cpu_percent}%")
                
                if memory.percent > 85:
                    self.logger.warning(f"High Memory Usage: {memory.percent}%")
                
                time.sleep(60)  # Check every minute
            
            except Exception as e:
                self.logger.error(f"Monitoring error: {e}")
                time.sleep(60)

    def start_prometheus_server(self, port=8000):
        """
        Start Prometheus metrics server
        """
        start_http_server(port)
        self.logger.info(f"Prometheus metrics server started on port {port}")

    def log_application_event(self, event_type, details):
        """
        Log application-specific events
        """
        self.logger.info(f"EVENT: {event_type} - {details}")
        
        # Optional: Update metrics based on event
        if event_type == 'ERROR':
            self.error_count.inc()

def main():
    monitor = SystemHealthMonitor()
    
    # Start Prometheus metrics server
    monitor.start_prometheus_server()
    
    # Start system resource monitoring
    monitor.monitor_system_resources()

if __name__ == '__main__':
    main()
