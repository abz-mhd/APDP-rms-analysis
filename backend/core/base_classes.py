"""
SOLID Principles - Single Responsibility Principle (SRP)
Base classes with single, well-defined responsibilities
"""

from abc import ABC
from typing import Dict, Any, List
import pandas as pd
from datetime import datetime


class BaseEntity:
    """Base entity class - Domain Driven Design"""
    
    def __init__(self, id: str):
        self._id = id
        self._created_at = datetime.now()
        self._updated_at = datetime.now()
    
    @property
    def id(self) -> str:
        return self._id
    
    @property
    def created_at(self) -> datetime:
        return self._created_at
    
    @property
    def updated_at(self) -> datetime:
        return self._updated_at
    
    def update_timestamp(self):
        """Update the last modified timestamp"""
        self._updated_at = datetime.now()


class Outlet(BaseEntity):
    """Outlet entity - Clean Domain Model"""
    
    def __init__(self, id: str, name: str, borough: str, capacity: int):
        super().__init__(id)
        self._name = name
        self._borough = borough
        self._capacity = capacity
        self._status = "Active"
    
    @property
    def name(self) -> str:
        return self._name
    
    @property
    def borough(self) -> str:
        return self._borough
    
    @property
    def capacity(self) -> int:
        return self._capacity
    
    @property
    def status(self) -> str:
        return self._status
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary - Data Transfer Object (DTO)"""
        return {
            'id': self.id,
            'name': self.name,
            'borough': self.borough,
            'capacity': self.capacity,
            'status': self.status
        }
    
    def __repr__(self) -> str:
        return f"Outlet(id={self.id}, name={self.name}, borough={self.borough})"


class Order(BaseEntity):
    """Order entity - Clean Domain Model"""
    
    def __init__(self, id: str, outlet_id: str, customer_id: str, 
                 total_price: float, order_date: datetime):
        super().__init__(id)
        self._outlet_id = outlet_id
        self._customer_id = customer_id
        self._total_price = total_price
        self._order_date = order_date
    
    @property
    def outlet_id(self) -> str:
        return self._outlet_id
    
    @property
    def customer_id(self) -> str:
        return self._customer_id
    
    @property
    def total_price(self) -> float:
        return self._total_price
    
    @property
    def order_date(self) -> datetime:
        return self._order_date
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary - DTO"""
        return {
            'id': self.id,
            'outlet_id': self.outlet_id,
            'customer_id': self.customer_id,
            'total_price': self.total_price,
            'order_date': self.order_date.isoformat()
        }


class AnalysisResult:
    """Value Object for analysis results - Immutable"""
    
    def __init__(self, analysis_type: str, data: Dict[str, Any], 
                 metadata: Dict[str, Any] = None):
        self._analysis_type = analysis_type
        self._data = data
        self._metadata = metadata or {}
        self._timestamp = datetime.now()
    
    @property
    def analysis_type(self) -> str:
        return self._analysis_type
    
    @property
    def data(self) -> Dict[str, Any]:
        return self._data.copy()  # Return copy to maintain immutability
    
    @property
    def metadata(self) -> Dict[str, Any]:
        return self._metadata.copy()
    
    @property
    def timestamp(self) -> datetime:
        return self._timestamp
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            'analysis_type': self.analysis_type,
            'data': self.data,
            'metadata': self.metadata,
            'timestamp': self.timestamp.isoformat()
        }


class FilterCriteria:
    """Value Object for filter criteria - Builder Pattern"""
    
    def __init__(self):
        self._outlet_id: Optional[str] = None
        self._season: Optional[str] = None
        self._festival: Optional[str] = None
        self._start_date: Optional[datetime] = None
        self._end_date: Optional[datetime] = None
    
    def with_outlet(self, outlet_id: str) -> 'FilterCriteria':
        """Fluent interface for building filters"""
        self._outlet_id = outlet_id
        return self
    
    def with_season(self, season: str) -> 'FilterCriteria':
        """Fluent interface for building filters"""
        self._season = season
        return self
    
    def with_festival(self, festival: str) -> 'FilterCriteria':
        """Fluent interface for building filters"""
        self._festival = festival
        return self
    
    def with_date_range(self, start_date: datetime, end_date: datetime) -> 'FilterCriteria':
        """Fluent interface for building filters"""
        self._start_date = start_date
        self._end_date = end_date
        return self
    
    @property
    def outlet_id(self) -> Optional[str]:
        return self._outlet_id
    
    @property
    def season(self) -> Optional[str]:
        return self._season
    
    @property
    def festival(self) -> Optional[str]:
        return self._festival
    
    @property
    def start_date(self) -> Optional[datetime]:
        return self._start_date
    
    @property
    def end_date(self) -> Optional[datetime]:
        return self._end_date
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            'outlet_id': self.outlet_id,
            'season': self.season,
            'festival': self.festival,
            'start_date': self.start_date.isoformat() if self.start_date else None,
            'end_date': self.end_date.isoformat() if self.end_date else None
        }
