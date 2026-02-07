"""
Strategy Pattern - Different analytics strategies
SOLID: Open/Closed Principle - Easy to add new analytics without modifying existing code
"""

from abc import ABC
from typing import Dict, Any
import pandas as pd
from backend.core.interfaces import IAnalyticsService
from backend.core.base_classes import AnalysisResult


class BaseAnalyticsService(IAnalyticsService, ABC):
    """
    Base class for analytics services
    Template Method Pattern: Defines skeleton of algorithm
    """
    
    def analyze(self, data: pd.DataFrame, **kwargs) -> Dict[str, Any]:
        """
        Template method for analysis
        Clean Code: Consistent interface across all analytics
        """
        if data.empty:
            return {'error': 'No data available for analysis'}
        
        try:
            # Validate data
            if not self._validate_data(data):
                return {'error': 'Data validation failed'}
            
            # Perform analysis
            result = self._perform_analysis(data, **kwargs)
            
            # Post-process results
            processed_result = self._post_process(result)
            
            return processed_result
            
        except Exception as e:
            return {'error': f'Analysis failed: {str(e)}'}
    
    def _validate_data(self, data: pd.DataFrame) -> bool:
        """
        Validate input data
        Clean Code: Protected method for subclass override
        """
        return not data.empty
    
    def _perform_analysis(self, data: pd.DataFrame, **kwargs) -> Dict[str, Any]:
        """
        Perform the actual analysis
        Clean Code: Must be implemented by subclasses
        """
        raise NotImplementedError("Subclasses must implement _perform_analysis")
    
    def _post_process(self, result: Dict[str, Any]) -> Dict[str, Any]:
        """
        Post-process analysis results
        Clean Code: Hook method for optional customization
        """
        return result


class PeakDiningAnalyticsService(BaseAnalyticsService):
    """
    Concrete strategy for peak dining analysis
    Single Responsibility: Only handles peak dining analytics
    """
    
    def get_analysis_type(self) -> str:
        return "peak-dining"
    
    def _validate_data(self, data: pd.DataFrame) -> bool:
        """Validate required columns for peak dining analysis"""
        required_columns = ['hour', 'day_of_week', 'order_id']
        return all(col in data.columns for col in required_columns)
    
    def _perform_analysis(self, data: pd.DataFrame, **kwargs) -> Dict[str, Any]:
        """
        Perform peak dining analysis
        Clean Code: Clear, focused implementation
        """
        result = {}
        
        # Hourly patterns
        hourly_patterns = data.groupby('hour').size().to_dict()
        result['hourlyPatterns'] = hourly_patterns
        
        # Daily patterns
        daily_patterns = data.groupby('day_of_week').size().to_dict()
        result['dailyPatterns'] = daily_patterns
        
        # Peak hours table
        peak_hours = data.groupby('hour').size().reset_index(name='orderCount')
        peak_hours = peak_hours.sort_values('orderCount', ascending=False).head(10)
        
        result['peakHourTables'] = {
            'overallPeakHours': [
                {
                    'hour': int(row['hour']),
                    'orderCount': int(row['orderCount']),
                    'timeRange': f"{int(row['hour']):02d}:00 - {(int(row['hour'])+1):02d}:00"
                }
                for _, row in peak_hours.iterrows()
            ]
        }
        
        # Branch summaries
        if 'name_y' in data.columns:
            branch_summaries = {}
            for outlet in data['name_y'].unique():
                outlet_data = data[data['name_y'] == outlet]
                branch_summaries[outlet] = {
                    'totalOrders': len(outlet_data),
                    'totalRevenue': float(outlet_data['total_price_lkr'].sum()) if 'total_price_lkr' in outlet_data.columns else 0,
                    'uniqueCustomers': int(outlet_data['customer_id'].nunique()) if 'customer_id' in outlet_data.columns else 0,
                    'peakHour': int(outlet_data.groupby('hour').size().idxmax()) if len(outlet_data) > 0 else 0
                }
            result['branchSummaries'] = branch_summaries
        
        result['totalOrders'] = len(data)
        
        return result


class RevenueAnalyticsService(BaseAnalyticsService):
    """
    Concrete strategy for revenue analysis
    Single Responsibility: Only handles revenue analytics
    """
    
    def get_analysis_type(self) -> str:
        return "revenue-analysis"
    
    def _validate_data(self, data: pd.DataFrame) -> bool:
        """Validate required columns for revenue analysis"""
        required_columns = ['total_price_lkr', 'order_id']
        return all(col in data.columns for col in required_columns)
    
    def _perform_analysis(self, data: pd.DataFrame, **kwargs) -> Dict[str, Any]:
        """
        Perform revenue analysis
        Clean Code: Focused on revenue metrics
        """
        result = {}
        
        # Revenue summary
        total_revenue = float(data['total_price_lkr'].sum())
        total_orders = int(data['order_id'].nunique())
        avg_order_value = total_revenue / total_orders if total_orders > 0 else 0
        
        result['revenueSummary'] = {
            'totalRevenue': total_revenue,
            'totalOrders': total_orders,
            'averageOrderValue': avg_order_value,
            'revenueGrowthRate': 'N/A'  # Would need historical data
        }
        
        # Daily revenue
        if 'date' in data.columns:
            daily_revenue = data.groupby('date')['total_price_lkr'].sum()
            result['dailyRevenue'] = {str(k): float(v) for k, v in daily_revenue.items()}
        
        # Payment methods
        if 'payment_method' in data.columns:
            payment_methods = data.groupby('payment_method')['total_price_lkr'].sum()
            result['paymentMethods'] = {str(k): float(v) for k, v in payment_methods.items()}
        
        # Outlet revenue
        if 'name_y' in data.columns:
            outlet_revenue = data.groupby('name_y').agg({
                'total_price_lkr': 'sum',
                'order_id': 'nunique'
            }).reset_index()
            outlet_revenue.columns = ['outletName', 'revenue', 'orderCount']
            outlet_revenue['avgOrderValue'] = outlet_revenue['revenue'] / outlet_revenue['orderCount']
            
            result['outletRevenue'] = [
                {
                    'outletName': str(row['outletName']),
                    'revenue': float(row['revenue']),
                    'orderCount': int(row['orderCount']),
                    'avgOrderValue': float(row['avgOrderValue'])
                }
                for _, row in outlet_revenue.iterrows()
            ]
        
        return result


class CustomerDemographicsService(BaseAnalyticsService):
    """
    Concrete strategy for customer demographics analysis
    Single Responsibility: Only handles customer demographics
    """
    
    def get_analysis_type(self) -> str:
        return "customer-demographics"
    
    def _validate_data(self, data: pd.DataFrame) -> bool:
        """Validate required columns"""
        required_columns = ['customer_id', 'age', 'gender']
        return all(col in data.columns for col in required_columns)
    
    def _perform_analysis(self, data: pd.DataFrame, **kwargs) -> Dict[str, Any]:
        """
        Perform customer demographics analysis
        Clean Code: Clear demographic calculations
        """
        result = {}
        
        # Get unique customers
        customers = data.drop_duplicates('customer_id').copy()
        
        # Age distribution
        age_bins = [0, 25, 35, 45, 55, 100]
        age_labels = ['18-25', '26-35', '36-45', '46-55', '55+']
        customers.loc[:, 'age_group'] = pd.cut(customers['age'], bins=age_bins, labels=age_labels, right=False)
        age_distribution = customers['age_group'].value_counts().to_dict()
        result['ageDistribution'] = {str(k): int(v) for k, v in age_distribution.items() if pd.notna(k)}
        
        # Gender distribution
        gender_distribution = customers['gender'].value_counts().to_dict()
        result['genderDistribution'] = {str(k): int(v) for k, v in gender_distribution.items()}
        
        # Loyalty distribution
        if 'loyalty_group' in customers.columns:
            loyalty_distribution = customers['loyalty_group'].value_counts().to_dict()
            result['loyaltyDistribution'] = {str(k): int(v) for k, v in loyalty_distribution.items()}
            
            # Loyalty segmentation
            loyalty_segmentation = {}
            for group in customers['loyalty_group'].unique():
                if pd.isna(group):
                    continue
                group_customers = customers[customers['loyalty_group'] == group]
                if len(group_customers) > 0:
                    loyalty_segmentation[str(group)] = {
                        'count': len(group_customers),
                        'avgAge': float(group_customers['age'].mean()) if not group_customers['age'].isna().all() else 0,
                        'genderDistribution': {str(k): int(v) for k, v in group_customers['gender'].value_counts().to_dict().items()}
                    }
            result['loyaltySegmentation'] = loyalty_segmentation
        
        result['totalCustomers'] = len(customers)
        
        return result


class AnalyticsServiceFactory:
    """
    Factory Pattern: Creates appropriate analytics service
    SOLID: Dependency Inversion - Clients depend on abstraction
    """
    
    _services = {
        'peak-dining': PeakDiningAnalyticsService,
        'revenue-analysis': RevenueAnalyticsService,
        'customer-demographics': CustomerDemographicsService,
    }
    
    @classmethod
    def create(cls, analysis_type: str) -> IAnalyticsService:
        """
        Create analytics service by type
        Clean Code: Factory method with clear intent
        """
        service_class = cls._services.get(analysis_type)
        
        if service_class is None:
            raise ValueError(f"Unknown analysis type: {analysis_type}")
        
        return service_class()
    
    @classmethod
    def register(cls, analysis_type: str, service_class: type) -> None:
        """
        Register new analytics service
        Open/Closed: Open for extension
        """
        cls._services[analysis_type] = service_class
    
    @classmethod
    def get_available_types(cls) -> list:
        """Get list of available analysis types"""
        return list(cls._services.keys())
