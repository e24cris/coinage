import os
import time
import json
import threading
import psutil
import redis
import prometheus_client
from prometheus_client import start_http_server, Gauge, Counter
from flask import Flask, jsonify
import requests

class MonitoringDashboard:
    """
    Comprehensive System and Application Monitoring Dashboard
    
    Features:
    - Real-time system metrics
    - Application performance tracking
    - Prometheus metrics export
    - Redis cache monitoring
    - External service health checks
    """
    
    def __init__(self, app_name='coinage', metrics_port=8000):
        """
        Initialize monitoring dashboard
        
        Args:
            app_name: Name of the application
            metrics_port: Port for Prometheus metrics server
        """
        self.app_name = app_name
        self.metrics_port = metrics_port
        
        # Prometheus Metrics
        self.cpu_usage = Gauge(
            'system_cpu_usage_percent', 
            'System CPU Usage Percentage'
        )
        self.memory_usage = Gauge(
            'system_memory_usage_percent', 
            'System Memory Usage Percentage'
        )
        self.disk_usage = Gauge(
            'system_disk_usage_percent', 
            'System Disk Usage Percentage'
        )
        
        # Application-specific metrics
        self.request_count = Counter(
            'app_request_total', 
            'Total Application Requests'
        )
        self.error_count = Counter(
            'app_error_total', 
            'Total Application Errors'
        )
        
        # Redis metrics
        self.redis_connected_clients = Gauge(
            'redis_connected_clients', 
            'Number of Redis Connected Clients'
        )
        
        # External service health metrics
        self.service_health = Gauge(
            'service_health_status', 
            'External Service Health Status',
            ['service_name']
        )
        
        # Redis connection
        self.redis_client = self._setup_redis()
    
    def _setup_redis(self):
        """
        Setup Redis client for monitoring
        
        Returns:
            Redis client or None
        """
        try:
            return redis.Redis(
                host=os.getenv('REDIS_HOST', 'localhost'),
                port=int(os.getenv('REDIS_PORT', 6379)),
                db=0
            )
        except Exception as e:
            print(f"Redis connection failed: {e}")
            return None
    
    def start_metrics_server(self):
        """
        Start Prometheus metrics server
        """
        print(f"Starting Prometheus metrics server on port {self.metrics_port}")
        start_http_server(self.metrics_port)
    
    def collect_system_metrics(self):
        """
        Collect and update system metrics
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
                
                # Redis Metrics
                if self.redis_client:
                    redis_info = self.redis_client.info()
                    self.redis_connected_clients.set(
                        redis_info.get('connected_clients', 0)
                    )
                
                time.sleep(60)  # Update every minute
            
            except Exception as e:
                print(f"Metrics collection error: {e}")
                time.sleep(60)
    
    def check_external_services(self, services):
        """
        Check health of external services
        
        Args:
            services: List of service URLs to check
        """
        while True:
            for service in services:
                try:
                    response = requests.get(service, timeout=5)
                    health_status = 1 if response.status_code == 200 else 0
                    self.service_health.labels(service_name=service).set(health_status)
                except Exception:
                    self.service_health.labels(service_name=service).set(0)
            
            time.sleep(300)  # Check every 5 minutes
    
    def create_flask_monitoring_app(self):
        """
        Create Flask app for additional monitoring endpoints
        
        Returns:
            Flask application
        """
        app = Flask(__name__)
        
        @app.route('/health')
        def health_check():
            """
            Comprehensive health check endpoint
            """
            system_metrics = {
                'cpu_usage': psutil.cpu_percent(),
                'memory_usage': psutil.virtual_memory().percent,
                'disk_usage': psutil.disk_usage('/').percent
            }
            
            return jsonify({
                'status': 'healthy',
                'system_metrics': system_metrics,
                'timestamp': time.time()
            })
        
        @app.route('/metrics')
        def metrics():
            """
            Expose metrics for Prometheus
            """
            return prometheus_client.generate_latest()
        
        return app
    
    def start_monitoring(self, external_services=None):
        """
        Start all monitoring threads
        
        Args:
            external_services: List of external service URLs to monitor
        """
        # Start Prometheus metrics server
        metrics_thread = threading.Thread(
            target=self.start_metrics_server, 
            daemon=True
        )
        metrics_thread.start()
        
        # System metrics collection
        system_metrics_thread = threading.Thread(
            target=self.collect_system_metrics, 
            daemon=True
        )
        system_metrics_thread.start()
        
        # External services health check
        if external_services:
            services_thread = threading.Thread(
                target=self.check_external_services, 
                args=(external_services,), 
                daemon=True
            )
            services_thread.start()

def main():
    """
    Demonstrate monitoring dashboard
    """
    # External services to monitor
    external_services = [
        'https://api.coinage.com/health',
        'https://database.coinage.com/status',
        'https://auth.coinage.com/ping'
    ]
    
    # Initialize monitoring dashboard
    dashboard = MonitoringDashboard()
    
    # Start monitoring
    dashboard.start_monitoring(external_services)
    
    # Start Flask monitoring app
    flask_app = dashboard.create_flask_monitoring_app()
    flask_app.run(port=5001)

if __name__ == '__main__':
    main()
