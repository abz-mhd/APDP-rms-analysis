"""
SOLID Principles - Interface Segregation Principle (ISP)
Define clear interfaces for different responsibilities
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional
import pandas as pd


class IDataRepository(ABC):
    """Interface for data access - Repository Pattern"""
    
    @abstractmethod
    def load_data(self) -> pd.DataFrame:
        """Load data from source"""
        pass
    
    @abstractmethod
    def get_outlets(self) -> List[Dict[str, Any]]:
        """Get list of outlets"""
        pass
    
    @abstractmethod
    def filter_by_outlet(self, outlet_id: str) -> pd.DataFrame:
        """Filter data by outlet"""
        pass
    
    @abstractmethod
    def filter_by_date_range(self, start_date: str, end_date: str) -> pd.DataFrame:
        """Filter data by date range"""
        pass


class IAnalyticsService(ABC):
    """Interface for analytics operations - Strategy Pattern"""
    
    @abstractmethod
    def analyze(self, data: pd.DataFrame, **kwargs) -> Dict[str, Any]:
        """Perform analysis on data"""
        pass
    
    @abstractmethod
    def get_analysis_type(self) -> str:
        """Get the type of analysis"""
        pass


class IChartGenerator(ABC):
    """Interface for chart generation - Factory Pattern"""
    
    @abstractmethod
    def generate(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate chart from data"""
        pass
    
    @abstractmethod
    def get_chart_type(self) -> str:
        """Get the type of chart"""
        pass


class IDataValidator(ABC):
    """Interface for data validation - Chain of Responsibility Pattern"""
    
    @abstractmethod
    def validate(self, data: pd.DataFrame) -> bool:
        """Validate data"""
        pass
    
    @abstractmethod
    def get_validation_errors(self) -> List[str]:
        """Get validation errors"""
        pass


class ICacheService(ABC):
    """Interface for caching - Proxy Pattern"""
    
    @abstractmethod
    def get(self, key: str) -> Optional[Any]:
        """Get cached value"""
        pass
    
    @abstractmethod
    def set(self, key: str, value: Any, ttl: int = 300) -> None:
        """Set cached value with TTL"""
        pass
    
    @abstractmethod
    def clear(self, pattern: str = None) -> None:
        """Clear cache"""
        pass


class ILogger(ABC):
    """Interface for logging - Observer Pattern"""
    
    @abstractmethod
    def log_info(self, message: str) -> None:
        """Log info message"""
        pass
    
    @abstractmethod
    def log_error(self, message: str, exception: Exception = None) -> None:
        """Log error message"""
        pass
    
    @abstractmethod
    def log_warning(self, message: str) -> None:
        """Log warning message"""
        pass


class IMetricsCalculator(ABC):
    """Interface for metrics calculation - Strategy Pattern"""
    
    @abstractmethod
    def calculate(self, data: pd.DataFrame) -> Dict[str, float]:
        """Calculate metrics"""
        pass
    
    @abstractmethod
    def get_metric_names(self) -> List[str]:
        """Get list of metric names"""
        pass
