import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import json
import os

class RestaurantDataProcessor:
    def __init__(self, csv_path=None):
        # Try multiple possible paths for the CSV file
        possible_paths = [
            'restaurant_dataset_with_4th_outlet.csv',  # New dataset with 4th outlet
            'restaurant_dataset_combined.csv',
            '../restaurant_dataset_with_4th_outlet.csv',
            '../restaurant_dataset_combined.csv',
            os.path.join(os.path.dirname(os.path.dirname(__file__)), 'restaurant_dataset_with_4th_outlet.csv'),
            os.path.join(os.path.dirname(os.path.dirname(__file__)), 'restaurant_dataset_combined.csv'),
            os.path.join(os.path.dirname(__file__), '..', 'restaurant_dataset_with_4th_outlet.csv'),
            os.path.join(os.path.dirname(__file__), '..', 'restaurant_dataset_combined.csv')
        ]
        
        self.csv_path = csv_path
        if not self.csv_path:
            for path in possible_paths:
                if os.path.exists(path):
                    self.csv_path = path
                    print(f"Found CSV file at: {path}")
                    break
        
        if not self.csv_path:
            self.csv_path = possible_paths[0]  # Default fallback
            print(f"Using fallback path: {self.csv_path}")
            
        self.df = None
        self.load_data()
    
    def load_data(self):
        """Load and preprocess the restaurant dataset"""
        try:
            print(f"Attempting to load CSV from: {self.csv_path}")
            
            if not os.path.exists(self.csv_path):
                print(f"CSV file not found at: {self.csv_path}")
                self.df = pd.DataFrame()
                return
            
            self.df = pd.read_csv(self.csv_path)
            print(f"Successfully loaded {len(self.df)} records from CSV")
            
            # Check if required columns exist
            required_columns = ['order_placed', 'served_time', 'join_date', 'total_price_lkr']
            missing_columns = [col for col in required_columns if col not in self.df.columns]
            
            if missing_columns:
                print(f"Warning: Missing columns: {missing_columns}")
                print(f"Available columns: {list(self.df.columns)}")
            
            # Convert datetime columns with error handling
            datetime_columns = ['order_placed', 'served_time', 'join_date']
            for col in datetime_columns:
                if col in self.df.columns:
                    try:
                        self.df[col] = pd.to_datetime(self.df[col], errors='coerce')
                        print(f"✓ Converted {col} to datetime")
                    except Exception as e:
                        print(f"Warning: Could not convert {col} to datetime: {e}")
            
            # Add derived columns
            if 'order_placed' in self.df.columns and not self.df['order_placed'].isna().all():
                self.df['hour'] = self.df['order_placed'].dt.hour
                self.df['day_of_week'] = self.df['order_placed'].dt.day_name()
                self.df['month'] = self.df['order_placed'].dt.month
                self.df['date'] = self.df['order_placed'].dt.date
                print("✓ Added derived time columns")
            
            print(f"✓ Data preprocessing completed. Final dataset: {len(self.df)} records")
            
        except Exception as e:
            print(f"Error loading data: {e}")
            print(f"Current working directory: {os.getcwd()}")
            print(f"Attempted CSV path: {self.csv_path}")
            self.df = pd.DataFrame()
    
    def get_outlets(self):
        """Get list of unique outlets from real data only"""
        if self.df.empty:
            return []
        
        outlets = self.df.groupby(['outlet_id', 'name_y']).first().reset_index()
        return [
            {
                'id': row['outlet_id'],
                'name': row['name_y'],
                'borough': row['borough'],
                'capacity': row['capacity']
            }
            for _, row in outlets.iterrows()
        ]
    
    def get_peak_dining_analysis(self, outlet_id=None, season=None, festival=None):
        """Analyze peak dining patterns"""
        df_filtered = self.filter_data(outlet_id, season, festival)
        
        if df_filtered.empty:
            return {'error': 'No data available for selected filters'}
        
        try:
            # Daily patterns
            daily_patterns = df_filtered.groupby('day_of_week').size().to_dict()
            
            # Hourly patterns
            hourly_patterns = df_filtered.groupby('hour').size().to_dict()
            
            # Hourly heatmap data by outlet
            hourly_heatmap = {}
            for outlet in df_filtered['name_y'].unique():
                outlet_data = df_filtered[df_filtered['name_y'] == outlet]
                hourly_counts = outlet_data.groupby('hour').size()
                hourly_heatmap[outlet] = {str(hour): int(count) for hour, count in hourly_counts.items()}
            
            # Peak hours table
            peak_hours_data = df_filtered.groupby('hour').size().reset_index(name='orderCount')
            peak_hours_data = peak_hours_data.sort_values('orderCount', ascending=False).head(10)
            
            peak_hour_tables = {
                'overallPeakHours': []
            }
            
            for _, row in peak_hours_data.iterrows():
                hour = int(row['hour'])
                count = int(row['orderCount'])
                time_range = f"{hour:02d}:00 - {(hour+1):02d}:00"
                peak_hour_tables['overallPeakHours'].append({
                    'hour': hour,
                    'orderCount': count,
                    'timeRange': time_range
                })
            
            # Branch-level summaries
            branch_summaries = {}
            for outlet in df_filtered['name_y'].unique():
                outlet_data = df_filtered[df_filtered['name_y'] == outlet]
                branch_summaries[outlet] = {
                    'totalOrders': len(outlet_data),
                    'totalRevenue': float(outlet_data['total_price_lkr'].sum()),
                    'uniqueCustomers': int(outlet_data['customer_id'].nunique()),
                    'avgOrderValue': float(outlet_data['total_price_lkr'].sum() / len(outlet_data)) if len(outlet_data) > 0 else 0,
                    'peakHour': int(outlet_data.groupby('hour').size().idxmax()) if len(outlet_data) > 0 else 0
                }
            
            return {
                'dailyPatterns': daily_patterns,
                'hourlyPatterns': hourly_patterns,
                'hourlyHeatmap': hourly_heatmap,
                'peakHourTables': peak_hour_tables,
                'branchSummaries': branch_summaries,
                'totalOrders': len(df_filtered)
            }
            
        except Exception as e:
            print(f"Error in peak dining analysis: {e}")
            return {'error': f'Error processing peak dining data: {str(e)}'}
    
    def get_customer_demographics(self, outlet_id=None, season=None, festival=None):
        """Analyze customer demographics"""
        df_filtered = self.filter_data(outlet_id, season, festival)
        
        if df_filtered.empty:
            return {'error': 'No data available for selected filters'}
        
        # Get unique customers
        customers = df_filtered.drop_duplicates('customer_id').copy()
        
        # Age distribution
        age_bins = [0, 25, 35, 45, 55, 100]
        age_labels = ['18-25', '26-35', '36-45', '46-55', '55+']
        customers.loc[:, 'age_group'] = pd.cut(customers['age'], bins=age_bins, labels=age_labels, right=False)
        age_distribution = customers['age_group'].value_counts().to_dict()
        
        # Convert keys to strings to avoid JSON serialization issues
        age_distribution = {str(k): int(v) for k, v in age_distribution.items() if pd.notna(k)}
        
        # Gender distribution
        gender_distribution = customers['gender'].value_counts().to_dict()
        gender_distribution = {str(k): int(v) for k, v in gender_distribution.items()}
        
        # Loyalty distribution
        loyalty_distribution = customers['loyalty_group'].value_counts().to_dict()
        loyalty_distribution = {str(k): int(v) for k, v in loyalty_distribution.items()}
        
        # Loyalty segmentation analysis
        loyalty_segmentation = {}
        for group in customers['loyalty_group'].unique():
            if pd.isna(group):  # Skip NaN values
                continue
            group_customers = customers[customers['loyalty_group'] == group]
            if len(group_customers) > 0:  # Only include groups with customers
                loyalty_segmentation[str(group)] = {
                    'count': len(group_customers),
                    'avgAge': float(group_customers['age'].mean()) if not group_customers['age'].isna().all() else 0,
                    'avgSpent': float(group_customers['estimated_total_spent_lkr'].mean()) if not group_customers['estimated_total_spent_lkr'].isna().all() else 0,
                    'genderDistribution': {str(k): int(v) for k, v in group_customers['gender'].value_counts().to_dict().items()}
                }
        
        return {
            'ageDistribution': age_distribution,
            'genderDistribution': gender_distribution,
            'loyaltyDistribution': loyalty_distribution,
            'loyaltySegmentation': loyalty_segmentation,
            'totalCustomers': len(customers)
        }
    
    def get_seasonal_behavior(self, outlet_id=None, season=None, festival=None):
        """Analyze seasonal customer behavior"""
        df_filtered = self.filter_data(outlet_id, season, festival)
        
        if df_filtered.empty:
            return {'error': 'No data available for selected filters'}
        
        try:
            # Monthly trends - fix the data structure
            monthly_orders_count = df_filtered.groupby('month')['order_id'].count().to_dict()
            monthly_revenue = df_filtered.groupby('month')['total_price_lkr'].sum().to_dict()
            
            # Convert month numbers to month names for better display
            month_names = {
                1: 'January', 2: 'February', 3: 'March', 4: 'April',
                5: 'May', 6: 'June', 7: 'July', 8: 'August',
                9: 'September', 10: 'October', 11: 'November', 12: 'December'
            }
            
            # Convert to proper format for charts
            monthly_orders_named = {}
            monthly_revenue_named = {}
            
            for month_num, count in monthly_orders_count.items():
                month_name = month_names.get(month_num, f'Month {month_num}')
                monthly_orders_named[month_name] = count
                
            for month_num, revenue in monthly_revenue.items():
                month_name = month_names.get(month_num, f'Month {month_num}')
                monthly_revenue_named[month_name] = float(revenue)
            
            # Seasonal retention (simplified)
            seasonal_retention = df_filtered.groupby('loyalty_group')['customer_id'].nunique().to_dict()
            seasonal_retention = {str(k): int(v) for k, v in seasonal_retention.items()}
            
            # Season-wise analysis
            season_mapping = {
                1: 'Winter', 2: 'Winter', 3: 'Spring',
                4: 'Spring', 5: 'Spring', 6: 'Summer',
                7: 'Summer', 8: 'Summer', 9: 'Autumn',
                10: 'Autumn', 11: 'Autumn', 12: 'Winter'
            }
            
            df_filtered_copy = df_filtered.copy()
            df_filtered_copy['season'] = df_filtered_copy['month'].map(season_mapping)
            seasonal_orders = df_filtered_copy.groupby('season')['order_id'].count().to_dict()
            seasonal_revenue = df_filtered_copy.groupby('season')['total_price_lkr'].sum().to_dict()
            
            return {
                'monthlyOrders': {
                    'order_id': monthly_orders_named,
                    'revenue': monthly_revenue_named
                },
                'seasonalRetention': seasonal_retention,
                'seasonalOrders': seasonal_orders,
                'seasonalRevenue': {str(k): float(v) for k, v in seasonal_revenue.items()},
                'totalOrders': len(df_filtered),
                'totalRevenue': float(df_filtered['total_price_lkr'].sum())
            }
        except Exception as e:
            print(f"Error in seasonal behavior analysis: {e}")
            return {'error': f'Error processing seasonal data: {str(e)}'}
    
    def get_menu_analysis(self, outlet_id=None, season=None, festival=None):
        """Analyze menu performance"""
        df_filtered = self.filter_data(outlet_id, season, festival)
        
        if df_filtered.empty:
            return {'error': 'No data available for selected filters'}
        
        try:
            # Popular items with more details
            popular_items = df_filtered.groupby('name').agg({
                'quantity': 'sum',
                'order_id': 'nunique',
                'price_lkr_y': ['mean', 'sum'],
                'category': 'first'
            }).reset_index()
            
            # Flatten column names
            popular_items.columns = ['itemName', 'totalQuantity', 'orderCount', 'price', 'totalRevenue', 'category']
            popular_items = popular_items.sort_values('orderCount', ascending=False).head(10)
            
            # Convert to proper data types
            popular_items_records = []
            for _, row in popular_items.iterrows():
                popular_items_records.append({
                    'itemName': str(row['itemName']),
                    'totalQuantity': int(row['totalQuantity']),
                    'orderCount': int(row['orderCount']),
                    'price': float(row['price']),
                    'totalRevenue': float(row['totalRevenue']),
                    'category': str(row['category'])
                })
            
            # Category analysis
            category_analysis = df_filtered.groupby('category').agg({
                'quantity': 'sum',
                'price_lkr_y': 'sum',
                'order_id': 'nunique'
            }).reset_index()
            category_analysis.columns = ['category', 'totalQuantity', 'totalRevenue', 'orderCount']
            
            # Spice level preferences
            spice_preferences = df_filtered['spice_level'].value_counts().to_dict()
            spice_preferences = {str(k): int(v) for k, v in spice_preferences.items()}
            
            # Vegetarian analysis
            veg_analysis = df_filtered['is_vegetarian'].value_counts().to_dict()
            veg_analysis = {str(k): int(v) for k, v in veg_analysis.items()}
            
            # Item combinations analysis (top item pairs in same orders)
            item_combinations = []
            order_items = df_filtered.groupby('order_id')['name'].apply(list).reset_index()
            combination_counts = {}
            
            for _, row in order_items.iterrows():
                items = row['name']
                if len(items) > 1:
                    for i in range(len(items)):
                        for j in range(i+1, len(items)):
                            combo = tuple(sorted([items[i], items[j]]))
                            combination_counts[combo] = combination_counts.get(combo, 0) + 1
            
            # Get top 5 combinations
            top_combinations = sorted(combination_counts.items(), key=lambda x: x[1], reverse=True)[:5]
            for combo, count in top_combinations:
                item_combinations.append({
                    'item1': combo[0],
                    'item2': combo[1],
                    'frequency': count
                })
            
            return {
                'popularItems': popular_items_records,
                'categoryAnalysis': category_analysis.to_dict('records'),
                'spicePreferences': spice_preferences,
                'vegetarianAnalysis': veg_analysis,
                'itemCombinations': item_combinations
            }
            
        except Exception as e:
            print(f"Error in menu analysis: {e}")
            return {'error': f'Error processing menu data: {str(e)}'}
    
    def get_revenue_analysis(self, outlet_id=None, season=None, festival=None):
        """Analyze revenue metrics"""
        df_filtered = self.filter_data(outlet_id, season, festival)
        
        if df_filtered.empty:
            return {'error': 'No data available for selected filters'}
        
        try:
            # Revenue summary
            total_revenue = float(df_filtered['total_price_lkr'].sum())
            total_orders = int(df_filtered['order_id'].nunique())
            avg_order_value = total_revenue / total_orders if total_orders > 0 else 0
            
            # Daily revenue
            daily_revenue = df_filtered.groupby('date')['total_price_lkr'].sum()
            daily_revenue = {str(k): float(v) for k, v in daily_revenue.items()}
            
            # Calculate growth rate from daily revenue
            growth_rate = "N/A"
            if len(daily_revenue) > 1:
                revenue_values = list(daily_revenue.values())
                if len(revenue_values) >= 2:
                    first_half = revenue_values[:len(revenue_values)//2]
                    second_half = revenue_values[len(revenue_values)//2:]
                    
                    avg_first = sum(first_half) / len(first_half) if first_half else 0
                    avg_second = sum(second_half) / len(second_half) if second_half else 0
                    
                    if avg_first > 0:
                        growth_rate = round(((avg_second - avg_first) / avg_first) * 100, 1)
            
            # Payment method analysis
            payment_methods = df_filtered.groupby('payment_method')['total_price_lkr'].sum()
            payment_methods = {str(k): float(v) for k, v in payment_methods.items()}
            
            # Outlet revenue comparison
            outlet_revenue = df_filtered.groupby('name_y').agg({
                'total_price_lkr': 'sum',
                'order_id': 'nunique'
            }).reset_index()
            outlet_revenue.columns = ['outletName', 'revenue', 'orderCount']
            outlet_revenue['avgOrderValue'] = outlet_revenue['revenue'] / outlet_revenue['orderCount']
            
            # Convert to proper data types
            outlet_revenue_records = []
            for _, row in outlet_revenue.iterrows():
                outlet_revenue_records.append({
                    'outletName': str(row['outletName']),
                    'revenue': float(row['revenue']),
                    'orderCount': int(row['orderCount']),
                    'avgOrderValue': float(row['avgOrderValue'])
                })
            
            return {
                'revenueSummary': {
                    'totalRevenue': total_revenue,
                    'totalOrders': total_orders,
                    'averageOrderValue': avg_order_value,
                    'revenueGrowthRate': growth_rate
                },
                'dailyRevenue': daily_revenue,
                'paymentMethods': payment_methods,
                'outletRevenue': outlet_revenue_records
            }
        except Exception as e:
            print(f"Error in revenue analysis: {e}")
            return {'error': f'Error processing revenue data: {str(e)}'}
    
    def get_branch_performance(self, outlet_id=None, season=None, festival=None):
        """Analyze branch performance"""
        df_filtered = self.filter_data(outlet_id, season, festival)
        
        if df_filtered.empty:
            return {'error': 'No data available for selected filters'}
        
        # Branch rankings
        branch_performance = df_filtered.groupby('name_y').agg({
            'total_price_lkr': 'sum',
            'order_id': 'nunique',
            'customer_id': 'nunique'
        }).reset_index()
        
        branch_performance.columns = ['branchName', 'revenue', 'orderCount', 'customerCount']
        branch_performance['averageOrderValue'] = branch_performance['revenue'] / branch_performance['orderCount']
        branch_performance = branch_performance.sort_values('revenue', ascending=False)
        
        return {
            'branchRankings': branch_performance.to_dict('records')
        }
    
    def get_anomaly_detection(self, outlet_id=None, season=None, festival=None):
        """Simple anomaly detection"""
        df_filtered = self.filter_data(outlet_id, season, festival)
        
        if df_filtered.empty:
            return {'error': 'No data available for selected filters'}
        
        alerts = []
        
        # Check for unusual order volumes
        daily_orders = df_filtered.groupby('date').size()
        mean_orders = daily_orders.mean()
        std_orders = daily_orders.std()
        
        for date, count in daily_orders.items():
            if count > mean_orders + 2 * std_orders:
                alerts.append({
                    'type': 'High Order Volume',
                    'message': f'Unusually high order volume on {date}: {count} orders',
                    'severity': 'HIGH',
                    'date': str(date)
                })
            elif count < mean_orders - 2 * std_orders:
                alerts.append({
                    'type': 'Low Order Volume',
                    'message': f'Unusually low order volume on {date}: {count} orders',
                    'severity': 'MEDIUM',
                    'date': str(date)
                })
        
        return {
            'alertLogs': alerts[-10:]  # Return last 10 alerts
        }
    
    def filter_data(self, outlet_id=None, season=None, festival=None):
        """Filter data based on parameters"""
        df_filtered = self.df.copy()
        
        if outlet_id:
            df_filtered = df_filtered[df_filtered['outlet_id'] == outlet_id]
        
        if season:
            season_months = {
                'spring': [3, 4, 5],
                'summer': [6, 7, 8],
                'autumn': [9, 10, 11],
                'winter': [12, 1, 2]
            }
            if season in season_months:
                df_filtered = df_filtered[df_filtered['month'].isin(season_months[season])]
        
        # Festival filtering would require additional date mapping
        # For now, we'll skip festival filtering
        
        return df_filtered
    
    def get_6_month_forecast(self, outlet_id=None):
        """Generate 6-month forecast based on historical data"""
        df_filtered = self.filter_data(outlet_id)
        
        if df_filtered.empty:
            return {'error': 'No data available for forecasting'}
        
        # Simple trend-based forecast
        monthly_revenue = df_filtered.groupby('month')['total_price_lkr'].sum()
        
        # Calculate average growth rate
        if len(monthly_revenue) > 1:
            growth_rate = monthly_revenue.pct_change().mean()
        else:
            growth_rate = 0.05  # Default 5% growth
        
        # Generate 6-month forecast
        last_month_revenue = monthly_revenue.iloc[-1] if len(monthly_revenue) > 0 else 100000
        forecast = []
        
        for i in range(1, 7):
            forecasted_revenue = last_month_revenue * (1 + growth_rate) ** i
            forecast.append({
                'month': f'Month +{i}',
                'forecastedRevenue': round(forecasted_revenue, 2),
                'confidence': max(0.6, 0.9 - i * 0.05)  # Decreasing confidence
            })
        
        return {
            'forecast': forecast,
            'growthRate': growth_rate,
            'baseRevenue': last_month_revenue
        }

# Global instance
data_processor = RestaurantDataProcessor()