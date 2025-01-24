import os
import uuid
import time
import logging
from typing import Dict, Any

from opentelemetry import trace
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.instrumentation.sqlalchemy import SQLAlchemyInstrumentor

class DistributedTracingSystem:
    def __init__(
        self, 
        service_name='coinage-platform', 
        jaeger_host='localhost', 
        jaeger_port=6831
    ):
        """
        Initialize distributed tracing system
        
        Args:
            service_name: Name of the service being traced
            jaeger_host: Jaeger collector host
            jaeger_port: Jaeger collector port
        """
        # Configure logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        
        # Trace provider configuration
        trace.set_tracer_provider(TracerProvider())
        self.tracer = trace.get_tracer(__name__)
        
        # Jaeger exporter setup
        self.jaeger_exporter = JaegerExporter(
            agent_host_name=jaeger_host,
            agent_port=jaeger_port
        )
        
        # Span processor
        trace.get_tracer_provider().add_span_processor(
            BatchSpanProcessor(self.jaeger_exporter)
        )
    
    def instrument_flask_app(self, app):
        """
        Instrument Flask application for tracing
        
        Args:
            app: Flask application instance
        """
        FlaskInstrumentor().instrument_app(app)
    
    def instrument_sqlalchemy(self, engine):
        """
        Instrument SQLAlchemy for database tracing
        
        Args:
            engine: SQLAlchemy engine
        """
        SQLAlchemyInstrumentor().instrument(engine=engine)
    
    def start_trace(self, name: str, attributes: Dict[str, Any] = None) -> trace.Span:
        """
        Start a new trace span
        
        Args:
            name: Name of the trace span
            attributes: Additional trace attributes
        
        Returns:
            Active trace span
        """
        attributes = attributes or {}
        return self.tracer.start_span(name, attributes=attributes)
    
    def end_trace(self, span: trace.Span, status: str = 'OK'):
        """
        End a trace span
        
        Args:
            span: Trace span to end
            status: Span status (OK/ERROR)
        """
        if status == 'ERROR':
            span.set_status(trace.Status(trace.StatusCode.ERROR))
        span.end()
    
    def trace_function(self, func):
        """
        Decorator to trace function execution
        
        Args:
            func: Function to trace
        
        Returns:
            Wrapped function with tracing
        """
        def wrapper(*args, **kwargs):
            trace_name = f"{func.__module__}.{func.__name__}"
            with self.start_trace(trace_name) as span:
                try:
                    result = func(*args, **kwargs)
                    self.end_trace(span)
                    return result
                except Exception as e:
                    self.end_trace(span, status='ERROR')
                    self.logger.error(f"Trace error in {trace_name}: {e}")
                    raise
        return wrapper

def main():
    """
    Demonstrate distributed tracing capabilities
    """
    tracing_system = DistributedTracingSystem()
    
    @tracing_system.trace_function
    def example_trading_function(trade_id):
        """Example function to demonstrate tracing"""
        time.sleep(0.1)  # Simulate processing
        return {"trade_id": trade_id, "status": "completed"}
    
    # Simulate multiple traces
    for i in range(5):
        trade_result = example_trading_function(str(uuid.uuid4()))
        print(f"Trade processed: {trade_result}")

if __name__ == '__main__':
    main()
