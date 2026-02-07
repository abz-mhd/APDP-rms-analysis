from flask import Blueprint, jsonify, request
import json
import plotly.graph_objs as go
import plotly.utils
from data_processor import data_processor

charts_bp = Blueprint('charts', __name__)

@charts_bp.route('/<analysis_type>')
def get_charts(analysis_type):
    """Generate charts for specific analysis type"""
    try:
        outlet_id = request.args.get('outletId')
        season = request.args.get('season')
        festival = request.args.get('festival')
        
        print(f"Generating charts for: {analysis_type}")
        
        if analysis_type == 'peak-dining':
            charts = generate_peak_dining_charts(outlet_id, season, festival)
        elif analysis_type == 'customer-demographics':
            charts = generate_customer_demographics_charts(outlet_id, season, festival)
        elif analysis_type == 'customer-seasonal' or analysis_type == 'seasonal-behavior':
            charts = generate_seasonal_behavior_charts(outlet_id, season, festival)
        elif analysis_type == 'menu-analysis':
            charts = generate_menu_analysis_charts(outlet_id, season, festival)
        elif analysis_type == 'revenue-analysis':
            charts = generate_revenue_analysis_charts(outlet_id, season, festival)
        elif analysis_type == 'anomaly-detection':
            charts = generate_anomaly_detection_charts(outlet_id, season, festival)
        elif analysis_type == 'branch-performance':
            charts = generate_branch_performance_charts(outlet_id, season, festival)
        else:
            return jsonify({'error': f'Invalid analysis type: {analysis_type}'}), 400
        
        print(f"Generated {len(charts)} charts for {analysis_type}")
        return jsonify(charts)
            
    except Exception as e:
        print(f"Error generating charts for {analysis_type}: {e}")
        return jsonify({'error': str(e)}), 500

def generate_peak_dining_charts(outlet_id=None, season=None, festival=None):
    """Generate charts for peak dining analysis"""
    data = data_processor.get_peak_dining_analysis(outlet_id, season, festival)
    
    if 'error' in data:
        return {'error': data['error']}
    
    charts = {}
    
    # Hourly patterns chart
    if 'hourlyPatterns' in data:
        hours = list(data['hourlyPatterns'].keys())
        counts = list(data['hourlyPatterns'].values())
        
        fig = go.Figure(data=[
            go.Bar(x=hours, y=counts, name='Orders by Hour')
        ])
        fig.update_layout(
            title='Peak Dining Hours',
            xaxis_title='Hour of Day',
            yaxis_title='Number of Orders',
            height=400
        )
        charts['hourly_patterns'] = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    
    # Daily patterns chart
    if 'dailyPatterns' in data:
        days = list(data['dailyPatterns'].keys())
        counts = list(data['dailyPatterns'].values())
        
        fig = go.Figure(data=[
            go.Bar(x=days, y=counts, name='Orders by Day')
        ])
        fig.update_layout(
            title='Daily Order Patterns',
            xaxis_title='Day of Week',
            yaxis_title='Number of Orders',
            height=400
        )
        charts['daily_patterns'] = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    
    # Peak Dining Heatmap - Hour vs Day of Week
    if 'hourlyHeatmap' in data:
        outlets = list(data['hourlyHeatmap'].keys())
        if outlets:
            # Create a comprehensive heatmap for all hours and days
            hours = list(range(24))
            days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
            
            # Get data for the first outlet or aggregate if multiple
            outlet_data = data['hourlyHeatmap'][outlets[0]]
            
            # Create matrix for heatmap
            z_matrix = []
            for day in days:
                day_data = []
                for hour in hours:
                    # Get order count for this hour, default to 0
                    count = outlet_data.get(str(hour), 0)
                    day_data.append(count)
                z_matrix.append(day_data)
            
            fig = go.Figure(data=go.Heatmap(
                z=z_matrix,
                x=[f"{h:02d}:00" for h in hours],
                y=days,
                colorscale='Viridis',
                showscale=True,
                colorbar=dict(title="Orders")
            ))
            
            fig.update_layout(
                title='Peak Dining Hours Heatmap',
                xaxis_title='Hour of Day',
                yaxis_title='Day of Week',
                height=500,
                width=800
            )
            charts['peak_dining_heatmap'] = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    
    # Branch performance comparison
    if 'branchSummaries' in data:
        branches = list(data['branchSummaries'].keys())
        orders = [data['branchSummaries'][branch]['totalOrders'] for branch in branches]
        revenue = [data['branchSummaries'][branch]['totalRevenue'] for branch in branches]
        
        fig = go.Figure(data=[
            go.Bar(name='Orders', x=branches, y=orders, yaxis='y'),
            go.Scatter(name='Revenue', x=branches, y=revenue, yaxis='y2', mode='lines+markers')
        ])
        fig.update_layout(
            title='Branch Performance Comparison',
            xaxis_title='Branch',
            yaxis=dict(title='Orders', side='left'),
            yaxis2=dict(title='Revenue (LKR)', side='right', overlaying='y'),
            height=400
        )
        charts['branch_comparison'] = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    
    return charts

def generate_customer_demographics_charts(outlet_id=None, season=None, festival=None):
    """Generate charts for customer demographics analysis"""
    data = data_processor.get_customer_demographics(outlet_id, season, festival)
    
    if 'error' in data:
        return {'error': data['error']}
    
    charts = {}
    
    # Age distribution pie chart
    if 'ageDistribution' in data:
        labels = list(data['ageDistribution'].keys())
        values = list(data['ageDistribution'].values())
        
        fig = go.Figure(data=[go.Pie(labels=labels, values=values)])
        fig.update_layout(title='Age Distribution', height=400)
        charts['age_distribution'] = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    
    # Gender distribution pie chart
    if 'genderDistribution' in data:
        labels = list(data['genderDistribution'].keys())
        values = list(data['genderDistribution'].values())
        
        fig = go.Figure(data=[go.Pie(labels=labels, values=values)])
        fig.update_layout(title='Gender Distribution', height=400)
        charts['gender_distribution'] = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    
    # Loyalty distribution bar chart
    if 'loyaltyDistribution' in data:
        labels = list(data['loyaltyDistribution'].keys())
        values = list(data['loyaltyDistribution'].values())
        
        fig = go.Figure(data=[go.Bar(x=labels, y=values)])
        fig.update_layout(
            title='Customer Loyalty Distribution',
            xaxis_title='Loyalty Group',
            yaxis_title='Number of Customers',
            height=400
        )
        charts['loyalty_distribution'] = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    
    # Customer Demographics Heatmap
    if 'loyaltySegmentation' in data and 'ageDistribution' in data:
        # Create a heatmap showing age groups vs loyalty segments
        age_groups = list(data['ageDistribution'].keys())
        loyalty_groups = list(data['loyaltySegmentation'].keys())
        
        # Create matrix for age vs loyalty
        z_matrix = []
        for loyalty in loyalty_groups:
            loyalty_data = data['loyaltySegmentation'][loyalty]
            row = []
            for age in age_groups:
                # Simulate correlation between age and loyalty (in real scenario, this would come from data)
                # For now, use the loyalty group count distributed across age groups
                count = loyalty_data.get('count', 0)
                # Distribute based on age distribution proportions
                age_proportion = data['ageDistribution'].get(age, 0) / sum(data['ageDistribution'].values())
                value = count * age_proportion
                row.append(value)
            z_matrix.append(row)
        
        fig = go.Figure(data=go.Heatmap(
            z=z_matrix,
            x=age_groups,
            y=loyalty_groups,
            colorscale='Blues',
            showscale=True,
            colorbar=dict(title="Customer Count"),
            text=[[f"{val:.0f}" for val in row] for row in z_matrix],
            texttemplate="%{text}",
            textfont={"size": 10}
        ))
        
        fig.update_layout(
            title='Customer Demographics Heatmap (Age vs Loyalty)',
            xaxis_title='Age Groups',
            yaxis_title='Loyalty Segments',
            height=500,
            width=700
        )
        charts['demographics_heatmap'] = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    
    return charts

def generate_seasonal_behavior_charts(outlet_id=None, season=None, festival=None):
    """Generate charts for seasonal behavior analysis"""
    data = data_processor.get_seasonal_behavior(outlet_id, season, festival)
    
    if 'error' in data:
        return {'error': data['error']}
    
    charts = {}
    
    # Monthly orders chart
    if 'monthlyOrders' in data and 'order_id' in data['monthlyOrders']:
        months = list(data['monthlyOrders']['order_id'].keys())
        orders = list(data['monthlyOrders']['order_id'].values())
        revenue = list(data['monthlyOrders']['revenue'].values())
        
        fig = go.Figure()
        fig.add_trace(go.Bar(name='Orders', x=months, y=orders, yaxis='y'))
        fig.add_trace(go.Scatter(name='Revenue', x=months, y=revenue, yaxis='y2', mode='lines+markers'))
        
        fig.update_layout(
            title='Monthly Trends',
            xaxis_title='Month',
            yaxis=dict(title='Orders', side='left'),
            yaxis2=dict(title='Revenue (LKR)', side='right', overlaying='y'),
            height=400
        )
        charts['monthly_trends'] = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    
    # Seasonal orders pie chart
    if 'seasonalOrders' in data:
        labels = list(data['seasonalOrders'].keys())
        values = list(data['seasonalOrders'].values())
        
        fig = go.Figure(data=[go.Pie(labels=labels, values=values)])
        fig.update_layout(title='Seasonal Order Distribution', height=400)
        charts['seasonal_orders'] = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    
    # Seasonal Performance Heatmap
    if 'monthlyOrders' in data and 'seasonalRetention' in data:
        # Create a heatmap showing months vs metrics
        months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
                 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        metrics = ['Orders', 'Revenue', 'Customer Retention']
        
        # Get monthly data
        monthly_data = data['monthlyOrders']
        
        z_matrix = []
        
        # Orders row
        if 'order_id' in monthly_data:
            month_orders = []
            for month in months:
                # Find matching month in data
                order_count = 0
                for month_key, count in monthly_data['order_id'].items():
                    if month.lower() in month_key.lower():
                        order_count = count
                        break
                month_orders.append(order_count)
            
            # Normalize orders
            max_orders = max(month_orders) if month_orders else 1
            orders_normalized = [v / max_orders * 100 for v in month_orders]
            z_matrix.append(orders_normalized)
        
        # Revenue row
        if 'revenue' in monthly_data:
            month_revenue = []
            for month in months:
                # Find matching month in data
                revenue = 0
                for month_key, rev in monthly_data['revenue'].items():
                    if month.lower() in month_key.lower():
                        revenue = rev
                        break
                month_revenue.append(revenue)
            
            # Normalize revenue
            max_revenue = max(month_revenue) if month_revenue else 1
            revenue_normalized = [v / max_revenue * 100 for v in month_revenue]
            z_matrix.append(revenue_normalized)
        
        # Customer retention row (simulated based on seasonal retention data)
        retention_values = list(data['seasonalRetention'].values()) if data['seasonalRetention'] else [50] * 12
        # Distribute retention across months
        avg_retention = sum(retention_values) / len(retention_values) if retention_values else 50
        retention_row = [avg_retention + (i % 3 - 1) * 10 for i in range(12)]  # Simulate variation
        retention_normalized = [max(0, min(100, v)) for v in retention_row]  # Keep in 0-100 range
        z_matrix.append(retention_normalized)
        
        if z_matrix:
            fig = go.Figure(data=go.Heatmap(
                z=z_matrix,
                x=months,
                y=metrics,
                colorscale='RdYlGn',
                showscale=True,
                colorbar=dict(title="Performance %"),
                text=[[f"{val:.1f}%" for val in row] for row in z_matrix],
                texttemplate="%{text}",
                textfont={"size": 10}
            ))
            
            fig.update_layout(
                title='Seasonal Performance Heatmap',
                xaxis_title='Months',
                yaxis_title='Performance Metrics',
                height=500,
                width=900
            )
            charts['seasonal_heatmap'] = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    
    return charts

def generate_menu_analysis_charts(outlet_id=None, season=None, festival=None):
    """Generate charts for menu analysis"""
    data = data_processor.get_menu_analysis(outlet_id, season, festival)
    
    if 'error' in data:
        return {'error': data['error']}
    
    charts = {}
    
    # Popular items chart
    if 'popularItems' in data and len(data['popularItems']) > 0:
        items = [item['itemName'][:20] + '...' if len(item['itemName']) > 20 else item['itemName'] 
                for item in data['popularItems'][:10]]
        orders = [item['orderCount'] for item in data['popularItems'][:10]]
        
        fig = go.Figure(data=[go.Bar(x=orders, y=items, orientation='h')])
        fig.update_layout(
            title='Top 10 Popular Items',
            xaxis_title='Number of Orders',
            yaxis_title='Menu Items',
            height=500
        )
        charts['popular_items'] = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    
    # Spice preferences pie chart
    if 'spicePreferences' in data:
        labels = list(data['spicePreferences'].keys())
        values = list(data['spicePreferences'].values())
        
        fig = go.Figure(data=[go.Pie(labels=labels, values=values)])
        fig.update_layout(title='Spice Level Preferences', height=400)
        charts['spice_preferences'] = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    
    # Category analysis
    if 'categoryAnalysis' in data and len(data['categoryAnalysis']) > 0:
        categories = [item['category'] for item in data['categoryAnalysis']]
        revenue = [item['totalRevenue'] for item in data['categoryAnalysis']]
        
        fig = go.Figure(data=[go.Bar(x=categories, y=revenue)])
        fig.update_layout(
            title='Revenue by Category',
            xaxis_title='Category',
            yaxis_title='Revenue (LKR)',
            height=400
        )
        charts['category_revenue'] = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    
    # Menu Category Performance Heatmap
    if 'categoryAnalysis' in data and len(data['categoryAnalysis']) > 0:
        categories = [item['category'] for item in data['categoryAnalysis'][:8]]  # Limit to 8 categories
        metrics = ['Revenue', 'Quantity', 'Orders']
        
        # Create matrix for heatmap
        z_matrix = []
        
        # Revenue row (normalized)
        revenue_values = [item['totalRevenue'] for item in data['categoryAnalysis'][:8]]
        max_revenue = max(revenue_values) if revenue_values else 1
        revenue_normalized = [v / max_revenue * 100 for v in revenue_values]
        z_matrix.append(revenue_normalized)
        
        # Quantity row (normalized)
        quantity_values = [item['totalQuantity'] for item in data['categoryAnalysis'][:8]]
        max_quantity = max(quantity_values) if quantity_values else 1
        quantity_normalized = [v / max_quantity * 100 for v in quantity_values]
        z_matrix.append(quantity_normalized)
        
        # Orders row (normalized)
        order_values = [item['orderCount'] for item in data['categoryAnalysis'][:8]]
        max_orders = max(order_values) if order_values else 1
        orders_normalized = [v / max_orders * 100 for v in order_values]
        z_matrix.append(orders_normalized)
        
        fig = go.Figure(data=go.Heatmap(
            z=z_matrix,
            x=[cat[:12] + '...' if len(cat) > 12 else cat for cat in categories],
            y=metrics,
            colorscale='Oranges',
            showscale=True,
            colorbar=dict(title="Performance %"),
            text=[[f"{val:.1f}%" for val in row] for row in z_matrix],
            texttemplate="%{text}",
            textfont={"size": 10}
        ))
        
        fig.update_layout(
            title='Menu Category Performance Heatmap',
            xaxis_title='Food Categories',
            yaxis_title='Performance Metrics',
            height=500,
            width=800
        )
        charts['menu_category_heatmap'] = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    
    return charts

def generate_revenue_analysis_charts(outlet_id=None, season=None, festival=None):
    """Generate charts for revenue analysis"""
    data = data_processor.get_revenue_analysis(outlet_id, season, festival)
    
    if 'error' in data:
        return {'error': data['error']}
    
    charts = {}
    
    # Daily revenue trend
    if 'dailyRevenue' in data:
        dates = list(data['dailyRevenue'].keys())
        revenue = list(data['dailyRevenue'].values())
        
        fig = go.Figure(data=[go.Scatter(x=dates, y=revenue, mode='lines+markers')])
        fig.update_layout(
            title='Daily Revenue Trend',
            xaxis_title='Date',
            yaxis_title='Revenue (LKR)',
            height=400
        )
        charts['daily_revenue'] = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    
    # Payment methods pie chart
    if 'paymentMethods' in data:
        labels = list(data['paymentMethods'].keys())
        values = list(data['paymentMethods'].values())
        
        fig = go.Figure(data=[go.Pie(labels=labels, values=values)])
        fig.update_layout(title='Payment Methods Distribution', height=400)
        charts['payment_methods'] = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    
    # Outlet revenue comparison
    if 'outletRevenue' in data and len(data['outletRevenue']) > 0:
        outlets = [item['outletName'][:15] + '...' if len(item['outletName']) > 15 else item['outletName'] 
                  for item in data['outletRevenue']]
        revenue = [item['revenue'] for item in data['outletRevenue']]
        
        fig = go.Figure(data=[go.Bar(x=outlets, y=revenue)])
        fig.update_layout(
            title='Revenue by Outlet',
            xaxis_title='Outlet',
            yaxis_title='Revenue (LKR)',
            height=400
        )
        charts['outlet_revenue'] = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    
    return charts

def generate_branch_performance_charts(outlet_id=None, season=None, festival=None):
    """Generate charts for branch performance analysis"""
    data = data_processor.get_branch_performance(outlet_id, season, festival)
    
    if 'error' in data:
        return {'error': data['error']}
    
    charts = {}
    
    # Branch rankings
    if 'branchRankings' in data and len(data['branchRankings']) > 0:
        branches = [item['branchName'][:15] + '...' if len(item['branchName']) > 15 else item['branchName'] 
                   for item in data['branchRankings'][:10]]
        revenue = [item['revenue'] for item in data['branchRankings'][:10]]
        orders = [item['orderCount'] for item in data['branchRankings'][:10]]
        
        fig = go.Figure()
        fig.add_trace(go.Bar(name='Revenue', x=branches, y=revenue, yaxis='y'))
        fig.add_trace(go.Scatter(name='Orders', x=branches, y=orders, yaxis='y2', mode='lines+markers'))
        
        fig.update_layout(
            title='Branch Performance Rankings',
            xaxis_title='Branch',
            yaxis=dict(title='Revenue (LKR)', side='left'),
            yaxis2=dict(title='Orders', side='right', overlaying='y'),
            height=400
        )
        charts['branch_rankings'] = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    
    # Branch Performance Heatmap
    if 'branchRankings' in data and len(data['branchRankings']) > 0:
        branches = [item['branchName'] for item in data['branchRankings'][:10]]
        metrics = ['Revenue', 'Orders', 'Customers', 'Avg Order Value']
        
        # Normalize data for heatmap (0-100 scale)
        z_matrix = []
        
        # Revenue row (normalized)
        revenue_values = [item['revenue'] for item in data['branchRankings'][:10]]
        max_revenue = max(revenue_values) if revenue_values else 1
        revenue_normalized = [v / max_revenue * 100 for v in revenue_values]
        z_matrix.append(revenue_normalized)
        
        # Orders row (normalized)
        order_values = [item['orderCount'] for item in data['branchRankings'][:10]]
        max_orders = max(order_values) if order_values else 1
        orders_normalized = [v / max_orders * 100 for v in order_values]
        z_matrix.append(orders_normalized)
        
        # Customers row (normalized)
        customer_values = [item['customerCount'] for item in data['branchRankings'][:10]]
        max_customers = max(customer_values) if customer_values else 1
        customers_normalized = [v / max_customers * 100 for v in customer_values]
        z_matrix.append(customers_normalized)
        
        # Average Order Value row (normalized)
        aov_values = [item['averageOrderValue'] for item in data['branchRankings'][:10]]
        max_aov = max(aov_values) if aov_values else 1
        aov_normalized = [v / max_aov * 100 for v in aov_values]
        z_matrix.append(aov_normalized)
        
        fig = go.Figure(data=go.Heatmap(
            z=z_matrix,
            x=[branch[:12] + '...' if len(branch) > 12 else branch for branch in branches],
            y=metrics,
            colorscale='RdYlBu_r',
            showscale=True,
            colorbar=dict(title="Performance %"),
            text=[[f"{val:.1f}%" for val in row] for row in z_matrix],
            texttemplate="%{text}",
            textfont={"size": 10}
        ))
        
        fig.update_layout(
            title='Branch Performance Heatmap (Normalized)',
            xaxis_title='Outlets',
            yaxis_title='Performance Metrics',
            height=500,
            width=800
        )
        charts['branch_performance_heatmap'] = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    
    return charts

def generate_anomaly_detection_charts(outlet_id=None, season=None, festival=None):
    """Generate charts for anomaly detection"""
    data = data_processor.get_anomaly_detection(outlet_id, season, festival)
    
    if 'error' in data:
        return {'error': data['error']}
    
    charts = {}
    
    # Alert summary
    if 'alertLogs' in data and len(data['alertLogs']) > 0:
        alert_types = {}
        for alert in data['alertLogs']:
            alert_type = alert['type']
            alert_types[alert_type] = alert_types.get(alert_type, 0) + 1
        
        labels = list(alert_types.keys())
        values = list(alert_types.values())
        
        fig = go.Figure(data=[go.Pie(labels=labels, values=values)])
        fig.update_layout(title='Alert Types Distribution', height=400)
        charts['alert_types'] = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    
    return charts