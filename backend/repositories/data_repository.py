"""
Repository Pattern - Data Access Layer
SOLID: Single Responsibility - Only handles data access
"""

import pandas as pd
import os
from typing import List, Dict, Any, Optional
from backend.core.interfaces import IDataRepository
from backend.core.base_classes import Outlet


class CSVDataRepository(IDataRepository):
    """
    Concrete implementation of data repository for CSV files
    Dependency Inversion Principle: Depends on abstraction (IDataRepository)
    """
    
    def __init__(self, csv_path: str):
        self._csv_path = csv_path
        self._df: Optional[pd.DataFrame] = None
        self._outlets_cache: Optional[List[Outlet]] = None
    
    def load_data(self) -> pd.DataFrame:
        """
        Load data from CSV file
        Clean Code: Single responsibility, clear method name
        """
        if self._df is not None:
            return self._df
        
        if not os.path.exists(self._csv_path):
            raise FileNotFoundError(f"CSV file not found: {self._csv_path}")
        
        try:
            self._df = pd.read_csv(self._csv_path)
            self._preprocess_data()
            return self._df
        except Exception as e:
            raise RuntimeError(f"Error loading CSV data: {str(e)}")
    
    def _preprocess_data(self) -> None:
        """
        Preprocess loaded data
        Clean Code: Private method for internal logic
        """
        if self._df is None:
            return
        
        # Convert datetime columns
        datetime_columns = ['order_placed', 'served_time', 'join_date']
        for col in datetime_columns:
            if col in self._df.columns:
                self._df[col] = pd.to_datetime(self._df[col], errors='coerce')
        
        # Add derived columns
        if 'order_placed' in self._df.columns:
            self._df['hour'] = self._df['order_placed'].dt.hour
            self._df['day_of_week'] = self._df['order_placed'].dt.day_name()
            self._df['month'] = self._df['order_placed'].dt.month
            self._df['date'] = self._df['order_placed'].dt.date
    
    def get_outlets(self) -> List[Dict[str, Any]]:
        """
        Get list of outlets
        Clean Code: Clear, descriptive method name
        """
        if self._outlets_cache is not None:
            return [outlet.to_dict() for outlet in self._outlets_cache]
        
        df = self.load_data()
        
        if df.empty:
            return []
        
        # Get unique outlets
        outlets_df = df.groupby(['outlet_id', 'name_y']).first().reset_index()
        
        self._outlets_cache = []
        for _, row in outlets_df.iterrows():
            outlet = Outlet(
                id=row['outlet_id'],
                name=row['name_y'],
                borough=row['borough'],
                capacity=int(row['capacity'])
            )
            self._outlets_cache.append(outlet)
        
        return [outlet.to_dict() for outlet in self._outlets_cache]
    
    def filter_by_outlet(self, outlet_id: str) -> pd.DataFrame:
        """
        Filter data by outlet ID
        Clean Code: Single responsibility, clear intent
        """
        df = self.load_data()
        
        if outlet_id:
            return df[df['outlet_id'] == outlet_id].copy()
        
        return df.copy()
    
    def filter_by_date_range(self, start_date: str, end_date: str) -> pd.DataFrame:
        """
        Filter data by date range
        Clean Code: Descriptive parameters
        """
        df = self.load_data()
        
        if 'order_placed' not in df.columns:
            return df.copy()
        
        filtered_df = df.copy()
        
        if start_date:
            filtered_df = filtered_df[filtered_df['order_placed'] >= start_date]
        
        if end_date:
            filtered_df = filtered_df[filtered_df['order_placed'] <= end_date]
        
        return filtered_df
    
    def filter_by_season(self, season: str) -> pd.DataFrame:
        """
        Filter data by season
        Clean Code: Additional helper method
        """
        df = self.load_data()
        
        season_months = {
            'spring': [3, 4, 5],
            'summer': [6, 7, 8],
            'autumn': [9, 10, 11],
            'winter': [12, 1, 2]
        }
        
        if season and season.lower() in season_months:
            months = season_months[season.lower()]
            return df[df['month'].isin(months)].copy()
        
        return df.copy()
    
    def get_data_summary(self) -> Dict[str, Any]:
        """
        Get summary statistics of the data
        Clean Code: Informative method for data overview
        """
        df = self.load_data()
        
        return {
            'total_records': len(df),
            'date_range': {
                'start': df['order_placed'].min().isoformat() if 'order_placed' in df.columns else None,
                'end': df['order_placed'].max().isoformat() if 'order_placed' in df.columns else None
            },
            'outlets_count': df['outlet_id'].nunique() if 'outlet_id' in df.columns else 0,
            'customers_count': df['customer_id'].nunique() if 'customer_id' in df.columns else 0,
            'columns': list(df.columns)
        }


class CachedDataRepository(IDataRepository):
    """
    Decorator Pattern: Adds caching to any data repository
    Open/Closed Principle: Open for extension, closed for modification
    """
    
    def __init__(self, repository: IDataRepository, cache_ttl: int = 300):
        self._repository = repository
        self._cache_ttl = cache_ttl
        self._cache: Dict[str, Any] = {}
        self._cache_timestamps: Dict[str, float] = {}
    
    def load_data(self) -> pd.DataFrame:
        """Load data with caching"""
        cache_key = 'data'
        
        if self._is_cache_valid(cache_key):
            return self._cache[cache_key]
        
        data = self._repository.load_data()
        self._set_cache(cache_key, data)
        return data
    
    def get_outlets(self) -> List[Dict[str, Any]]:
        """Get outlets with caching"""
        cache_key = 'outlets'
        
        if self._is_cache_valid(cache_key):
            return self._cache[cache_key]
        
        outlets = self._repository.get_outlets()
        self._set_cache(cache_key, outlets)
        return outlets
    
    def filter_by_outlet(self, outlet_id: str) -> pd.DataFrame:
        """Filter by outlet with caching"""
        cache_key = f'outlet_{outlet_id}'
        
        if self._is_cache_valid(cache_key):
            return self._cache[cache_key]
        
        data = self._repository.filter_by_outlet(outlet_id)
        self._set_cache(cache_key, data)
        return data
    
    def filter_by_date_range(self, start_date: str, end_date: str) -> pd.DataFrame:
        """Filter by date range with caching"""
        cache_key = f'date_{start_date}_{end_date}'
        
        if self._is_cache_valid(cache_key):
            return self._cache[cache_key]
        
        data = self._repository.filter_by_date_range(start_date, end_date)
        self._set_cache(cache_key, data)
        return data
    
    def _is_cache_valid(self, key: str) -> bool:
        """Check if cache is still valid"""
        import time
        
        if key not in self._cache:
            return False
        
        if key not in self._cache_timestamps:
            return False
        
        age = time.time() - self._cache_timestamps[key]
        return age < self._cache_ttl
    
    def _set_cache(self, key: str, value: Any) -> None:
        """Set cache value with timestamp"""
        import time
        
        self._cache[key] = value
        self._cache_timestamps[key] = time.time()
    
    def clear_cache(self) -> None:
        """Clear all cached data"""
        self._cache.clear()
        self._cache_timestamps.clear()
