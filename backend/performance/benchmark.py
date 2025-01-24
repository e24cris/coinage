import time
import statistics
import multiprocessing
import asyncio
import random
from typing import List, Dict, Any, Callable
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from memory_profiler import profile
from line_profiler import LineProfiler

class PerformanceBenchmark:
    """
    Comprehensive Performance Benchmarking Framework
    
    Features:
    - Execution Time Measurement
    - Memory Profiling
    - Concurrency Testing
    - Statistical Analysis
    - Visualization
    """
    
    @staticmethod
    def measure_execution_time(
        func: Callable, 
        *args, 
        iterations: int = 100, 
        **kwargs
    ) -> Dict[str, float]:
        """
        Measure function execution time with statistical analysis
        
        Args:
            func: Function to benchmark
            iterations: Number of times to run the function
            *args: Positional arguments for the function
            **kwargs: Keyword arguments for the function
        
        Returns:
            Performance metrics dictionary
        """
        execution_times = []
        
        for _ in range(iterations):
            start_time = time.perf_counter()
            func(*args, **kwargs)
            end_time = time.perf_counter()
            execution_times.append(end_time - start_time)
        
        return {
            'mean_time': statistics.mean(execution_times),
            'median_time': statistics.median(execution_times),
            'std_dev': statistics.stdev(execution_times),
            'min_time': min(execution_times),
            'max_time': max(execution_times)
        }
    
    @staticmethod
    @profile
    def memory_intensive_operation(data_size: int = 1_000_000):
        """
        Simulate memory-intensive operation
        
        Args:
            data_size: Size of data to process
        """
        large_list = [random.random() for _ in range(data_size)]
        large_array = np.array(large_list)
        large_df = pd.DataFrame(large_array)
        
        # Perform some computations
        large_df['squared'] = large_df[0] ** 2
        large_df['log'] = np.log(large_df[0] + 1)
        
        return large_df
    
    @staticmethod
    def concurrent_benchmark(
        func: Callable, 
        args_list: List[tuple], 
        max_workers: int = None
    ) -> List[Any]:
        """
        Benchmark concurrent function execution
        
        Args:
            func: Function to execute concurrently
            args_list: List of argument tuples
            max_workers: Maximum number of concurrent workers
        
        Returns:
            List of function results
        """
        max_workers = max_workers or multiprocessing.cpu_count()
        
        with multiprocessing.Pool(max_workers) as pool:
            start_time = time.perf_counter()
            results = pool.starmap(func, args_list)
            end_time = time.perf_counter()
        
        print(f"Concurrent Execution Time: {end_time - start_time} seconds")
        return results
    
    @staticmethod
    async def async_benchmark(
        func: Callable, 
        args_list: List[tuple]
    ) -> List[Any]:
        """
        Benchmark async function execution
        
        Args:
            func: Async function to execute
            args_list: List of argument tuples
        
        Returns:
            List of function results
        """
        async def run_func(*args):
            return await func(*args)
        
        start_time = time.perf_counter()
        results = await asyncio.gather(
            *[run_func(*args) for args in args_list]
        )
        end_time = time.perf_counter()
        
        print(f"Async Execution Time: {end_time - start_time} seconds")
        return results
    
    @staticmethod
    def line_profile(func: Callable, *args, **kwargs):
        """
        Perform line-by-line profiling
        
        Args:
            func: Function to profile
            *args: Positional arguments
            **kwargs: Keyword arguments
        
        Returns:
            Profiling results
        """
        profiler = LineProfiler(func)
        profiler.run(f"func(*{args}, **{kwargs})")
        profiler.print_stats()
    
    @staticmethod
    def visualize_performance(
        benchmark_results: Dict[str, List[float]], 
        title: str = 'Performance Benchmark'
    ):
        """
        Visualize performance benchmark results
        
        Args:
            benchmark_results: Dictionary of performance metrics
            title: Plot title
        """
        plt.figure(figsize=(10, 6))
        
        for method, times in benchmark_results.items():
            plt.plot(times, label=method)
        
        plt.title(title)
        plt.xlabel('Iteration')
        plt.ylabel('Execution Time (seconds)')
        plt.legend()
        plt.tight_layout()
        plt.savefig('performance_benchmark.png')
        plt.close()

def trading_performance_test(num_trades: int = 1000):
    """
    Simulate trading performance test
    
    Args:
        num_trades: Number of trades to simulate
    
    Returns:
        Trading performance metrics
    """
    from backend.trading_engine import TradingStrategy, TradingEngine
    
    trading_engine = TradingEngine('sqlite:///performance_test.db')
    
    def simulate_trade():
        price_history = [random.uniform(100, 200) for _ in range(20)]
        recommendation = trading_engine.analyze_trade_opportunity('AAPL', price_history)
        
        if recommendation['recommendation'] == 'buy':
            trading_engine.execute_trade(
                user_id=1,
                asset='AAPL',
                trade_type='buy',
                quantity=10,
                price=price_history[-1]
            )
    
    benchmark = PerformanceBenchmark()
    
    # Measure execution time
    performance_metrics = benchmark.measure_execution_time(
        simulate_trade,
        iterations=num_trades
    )
    
    # Concurrent benchmark
    args_list = [('AAPL',) for _ in range(num_trades)]
    benchmark.concurrent_benchmark(
        trading_engine.analyze_trade_opportunity, 
        args_list
    )
    
    return performance_metrics

def main():
    """
    Run comprehensive performance benchmarks
    """
    benchmark = PerformanceBenchmark()
    
    # Memory Intensive Operation Benchmark
    memory_metrics = benchmark.measure_execution_time(
        benchmark.memory_intensive_operation, 
        data_size=1_000_000
    )
    print("Memory Operation Metrics:", memory_metrics)
    
    # Trading Performance Test
    trading_metrics = trading_performance_test()
    print("Trading Performance Metrics:", trading_metrics)
    
    # Visualization
    benchmark.visualize_performance({
        'Memory Operation': [0.1, 0.2, 0.15],
        'Trading Performance': [0.05, 0.08, 0.06]
    })

if __name__ == '__main__':
    main()
