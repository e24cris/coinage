import os
import time
import logging
import asyncio
import multiprocessing
from typing import Dict, Any, List, Callable
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
import psutil
import redis
import prometheus_client

class AdvancedPerformanceManager:
    def __init__(
        self, 
        redis_host: str = 'localhost', 
        redis_port: int = 6379,
        log_level: int = logging.INFO
    ):
        """
        Initialize Advanced Performance Manager
        
        Args:
            redis_host: Redis server host
            redis_port: Redis server port
            log_level: Logging level
        """
        # Configure logging
        logging.basicConfig(
            level=log_level,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)
        
        # Redis connection for caching
        self.redis_client = redis.Redis(host=redis_host, port=redis_port)
        
        # Prometheus metrics
        self.request_processing_time = prometheus_client.Histogram(
            'request_processing_seconds', 
            'Time spent processing requests'
        )
        self.system_load_gauge = prometheus_client.Gauge(
            'system_load', 
            'Current system load'
        )
        
        # Performance tracking
        self.performance_metrics = {
            'cpu_bound_tasks': [],
            'io_bound_tasks': [],
            'cache_hits': 0,
            'cache_misses': 0
        }
    
    def cache_decorator(self, ttl: int = 300):
        """
        Caching decorator for expensive computations
        
        Args:
            ttl: Cache time-to-live in seconds
        """
        def decorator(func):
            def wrapper(*args, **kwargs):
                # Generate cache key
                cache_key = f"{func.__name__}:{hash(str(args) + str(kwargs))}"
                
                # Check cache
                cached_result = self.redis_client.get(cache_key)
                
                if cached_result:
                    self.performance_metrics['cache_hits'] += 1
                    return eval(cached_result)
                
                # Compute result
                result = func(*args, **kwargs)
                
                # Cache result
                self.redis_client.setex(
                    cache_key, 
                    ttl, 
                    str(result)
                )
                
                self.performance_metrics['cache_misses'] += 1
                return result
            
            return wrapper
        return decorator
    
    def parallel_processing_decorator(self, max_workers: int = None):
        """
        Parallel processing decorator for CPU-bound tasks
        
        Args:
            max_workers: Maximum number of workers
        """
        def decorator(func):
            def wrapper(*args, **kwargs):
                workers = max_workers or (multiprocessing.cpu_count() - 1)
                
                start_time = time.time()
                
                with ProcessPoolExecutor(max_workers=workers) as executor:
                    result = executor.submit(func, *args, **kwargs)
                    result = result.result()
                
                execution_time = time.time() - start_time
                
                self.performance_metrics['cpu_bound_tasks'].append({
                    'function_name': func.__name__,
                    'execution_time': execution_time,
                    'workers_used': workers
                })
                
                return result
            
            return wrapper
        return decorator
    
    def async_io_processing(self, func: Callable):
        """
        Async processing decorator for I/O-bound tasks
        
        Args:
            func: Function to be processed asynchronously
        """
        async def async_wrapper(*args, **kwargs):
            start_time = time.time()
            
            with ThreadPoolExecutor() as executor:
                loop = asyncio.get_event_loop()
                result = await loop.run_in_executor(
                    executor, 
                    func, 
                    *args, 
                    **kwargs
                )
            
            execution_time = time.time() - start_time
            
            self.performance_metrics['io_bound_tasks'].append({
                'function_name': func.__name__,
                'execution_time': execution_time
            })
            
            return result
        
        return async_wrapper
    
    def monitor_system_performance(self) -> Dict[str, Any]:
        """
        Monitor system performance metrics
        
        Returns:
            System performance metrics
        """
        cpu_usage = psutil.cpu_percent(interval=1)
        memory_usage = psutil.virtual_memory().percent
        disk_usage = psutil.disk_usage('/').percent
        
        # Update Prometheus metrics
        self.system_load_gauge.set(cpu_usage)
        
        system_metrics = {
            'cpu_usage': cpu_usage,
            'memory_usage': memory_usage,
            'disk_usage': disk_usage,
            'num_cpus': multiprocessing.cpu_count()
        }
        
        self.logger.info(f"System Performance: {system_metrics}")
        return system_metrics
    
    def generate_performance_report(self) -> Dict[str, Any]:
        """
        Generate comprehensive performance report
        
        Returns:
            Performance metrics and insights
        """
        def calculate_average(metric_list: List[Dict], key: str) -> float:
            return sum(task[key] for task in metric_list) / len(metric_list) if metric_list else 0
        
        performance_report = {
            'system_metrics': self.monitor_system_performance(),
            'task_performance': {
                'cpu_bound_tasks': {
                    'total_tasks': len(self.performance_metrics['cpu_bound_tasks']),
                    'avg_execution_time': calculate_average(
                        self.performance_metrics['cpu_bound_tasks'], 
                        'execution_time'
                    )
                },
                'io_bound_tasks': {
                    'total_tasks': len(self.performance_metrics['io_bound_tasks']),
                    'avg_execution_time': calculate_average(
                        self.performance_metrics['io_bound_tasks'], 
                        'execution_time'
                    )
                }
            },
            'cache_performance': {
                'total_hits': self.performance_metrics['cache_hits'],
                'total_misses': self.performance_metrics['cache_misses'],
                'hit_rate': (self.performance_metrics['cache_hits'] / 
                             (self.performance_metrics['cache_hits'] + 
                              self.performance_metrics['cache_misses'] + 1)) * 100
            }
        }
        
        self.logger.info(f"Performance Report: {performance_report}")
        return performance_report

def main():
    """
    Demonstrate Advanced Performance Manager
    """
    perf_manager = AdvancedPerformanceManager()
    
    # Example CPU-bound task with parallel processing
    @perf_manager.parallel_processing_decorator()
    def complex_calculation(n):
        return sum(i**2 for i in range(n))
    
    # Example I/O-bound task with async processing
    @perf_manager.async_io_processing
    def fetch_data(url):
        import requests
        return requests.get(url).text
    
    # Example cached computation
    @perf_manager.cache_decorator(ttl=60)
    def expensive_computation(x, y):
        time.sleep(2)  # Simulate expensive computation
        return x * y
    
    # Run example tasks
    complex_calculation(1000000)
    expensive_computation(10, 20)
    expensive_computation(10, 20)  # Second call should be cached
    
    # Generate performance report
    performance_report = perf_manager.generate_performance_report()
    
    # Save performance report
    import json
    with open('performance_report.json', 'w') as f:
        json.dump(performance_report, f, indent=2)

if __name__ == '__main__':
    main()
