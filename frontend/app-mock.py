from flask import Flask, render_template, request, jsonify, send_file
import json
import random
from datetime import datetime, timedelta
import pandas as pd
import plotly.graph_objs as go
import plotly.utils

app = Flask(__name__)
app.secret_key = 'restaurant-analytics-secret-key'

# Mock data
MOCK_OUTLETS = [
    {"outletId": "OUT01", "outletName": "Ocean View - Galle", "borough": "Galle", "capacity": 80},
    {"outletId": "OUT02", "outletName": "City Center - Colombo", "borough": "Colombo", "capacity": 120},
    {"outletId": "OUT03", "outletName": "Beach Side - Negombo", "borough": "Negombo", "capacity": 60},
    {"outletId": "OUT04", "outletName": "Hill Station - Kandy", "borough": "Kandy", "capacity": 90}
]

def generate_mock_peak_dining_data():
    return {
        "hourlyHeatmap": {
            "OUT01": {str(i): random.randint(5, 50) for i in range(24)},
            "OUT02": {str(i): random.randint(10, 80) for i in range(24)},
            "OUT03": {str(i): random.randint(3, 40) for i in range(24)},
            "OUT04": {str(i): random.randint(8, 60) for i in range(24)}
        },
        "peakHourTables": {
            "overallPeakHours": [
                {"hour": 12, "orderCount": 245, "timeRange": "12:00 - 12:59"},
                {"hour": 19, "orderCount": 198, "timeRange": "19:00 - 19:59"},
                {"hour": 13, "orderCount": 167, "timeRange": "13:00 - 13:59"},
                {"hour": 20, "orderCount": 145, "timeRange": "20:00 - 20:59"},
                {"hour": 18, "orderCount": 132, "timeRange": "18:00 - 18:59"}
            ]
        },
        "dailyPatterns": {
            "MONDAY": 850, "TUESDAY": 920, "WEDNESDAY": 880, 
            "THURSDAY": 950, "FRIDAY": 1200, "SATURDAY": 1350, "SUNDAY": 1100
        },
        "branchSummaries": {
            outlet["outletId"]: {
                "totalOrders": random.randint(800, 1500),
                "totalRevenue": random.randint(50000, 120000),
                "averageOrderValue": random.randint(2000, 4000),
                "uniqueCustomers": random.randint(300, 800),
                "outletName": outlet["outletName"],
                "borough": outlet["borough"],
                "peakHour": random.randint(11, 21),
                "peakHourOrders": random.randint(40, 80)
            } for outlet in MOCK_OUTLETS
        }
    }

def generate_mock_customer_demographics():
    return {
        "ageDistribution": {
            "18-24": 245, "25-34": 456, "35-44": 389, 
            "45-54": 298, "55-64": 167, "65+": 89
        },
        "genderDistribution": {
            "Male": 892, "Female": 756, "Other": 96
        },
        "loyaltyGroupAnalysis": {
            "distribution": {
                "Occasional": 678, "Regular": 543, "VIP": 123
            },
            "averageSpending": {
                "Occasional": 2150.50, "Regular": 3240.75, "VIP": 5890.25
            }
        },
        "customerSegmentation": {
            "segmentDistribution": {
                "VIP": 123, "Loyal": 234, "Regular": 456, "Occasional": 531
            }
        },
        "spendingPatterns": {
            "spendingByAge": {
                "18-24": 1850.25, "25-34": 2340.50, "35-44": 2890.75,
                "45-54": 3120.00, "55-64": 2650.25, "65+": 2100.50
            },
            "spendingByGender": {
                "Male": 2450.75, "Female": 2380.50, "Other": 2200.25
            }
        }
    }

def generate_mock_menu_analysis():
    return {
        "popularItems": [
            {"itemName": "Grilled Chicken Rice", "orderCount": 234, "totalRevenue": 351000, "category": "Main Course", "price": 1500, "isVegetarian": False, "spiceLevel": "Medium"},
            {"itemName": "Vegetable Fried Rice", "orderCount": 198, "totalRevenue": 237600, "category": "Main Course", "price": 1200, "isVegetarian": True, "spiceLevel": "Mild"},
            {"itemName": "Fish Curry", "orderCount": 167, "totalRevenue": 300600, "category": "Main Course", "price": 1800, "isVegetarian": False, "spiceLevel": "Hot"},
            {"itemName": "Mango Juice", "orderCount": 145, "totalRevenue": 87000, "category": "Beverage", "price": 600, "isVegetarian": True, "spiceLevel": "None"},
            {"itemName": "Chocolate Cake", "orderCount": 132, "totalRevenue": 105600, "category": "Dessert", "price": 800, "isVegetarian": True, "spiceLevel": "None"}
        ],
        "categoryAnalysis": {
            "ordersByCategory": {
                "Main Course": 1245, "Beverage": 892, "Dessert": 456, "Starter": 234, "Fast Food": 567
            },
            "revenueByCategory": {
                "Main Course": 1867500, "Beverage": 534600, "Dessert": 364800, "Starter": 140400, "Fast Food": 453600
            }
        },
        "spiceLevelPreferences": {
            "Mild": 567, "Medium": 892, "Hot": 345, "None": 234
        },
        "vegetarianAnalysis": {
            "distribution": {True: 678, False: 1366},
            "revenue": {True: 813600, False: 2547300}
        }
    }

def generate_mock_revenue_analysis():
    return {
        "revenueSummary": {
            "totalRevenue": 3360900,
            "reconciledRevenue": 3360900,
            "averageOrderValue": 2456.75,
            "totalOrders": 1369,
            "revenueGrowthRate": 12.5
        },
        "dailyRevenue": {
            f"2025-01-{i:02d}": random.randint(80000, 150000) for i in range(1, 14)
        },
        "monthlyRevenue": {
            "2024-11": 2890000, "2024-12": 3120000, "2025-01": 3360900
        },
        "paymentMethodAnalysis": {
            "ordersByPaymentMethod": {"Card": 1089, "Cash": 280},
            "revenueByPaymentMethod": {"Card": 2688720, "Cash": 672180}
        },
        "outletRevenue": {
            outlet["outletId"]: {
                "revenue": random.randint(600000, 1200000),
                "orderCount": random.randint(300, 600),
                "averageOrderValue": random.randint(2000, 3000),
                "outletName": outlet["outletName"],
                "borough": outlet["borough"]
            } for outlet in MOCK_OUTLETS
        }
    }

def create_charts_for_analysis(analysis_type, data):
    """Create Plotly charts for different analysis types with custom color palette"""
    charts = {}
    
    # Custom color palette
    PRIMARY_DARK = '#3d766d'
    PRIMARY_MEDIUM = '#8f9192'
    PRIMARY_LIGHT = '#bdc2c7'
    BACKGROUND_LIGHT = '#d6d9df'
    BACKGROUND_LIGHTER = '#f0f3f5'
    BACKGROUND_WHITE = '#fdfdfe'
    
    # Custom color schemes for different chart types
    CUSTOM_COLORS = [PRIMARY_DARK, PRIMARY_MEDIUM, PRIMARY_LIGHT, '#a8b5b3', '#7a8584']
    GRADIENT_COLORS = [[0, PRIMARY_DARK], [0.5, PRIMARY_MEDIUM], [1, PRIMARY_LIGHT]]
    
    if analysis_type == 'peak-dining':
        # Hourly heatmap
        if 'hourlyHeatmap' in data:
            heatmap_data = data['hourlyHeatmap']
            outlets = list(heatmap_data.keys())
            hours = list(range(24))
            z_data = []
            
            for outlet in outlets:
                outlet_data = heatmap_data[outlet]
                row = [outlet_data.get(str(hour), 0) for hour in hours]
                z_data.append(row)
            
            heatmap = go.Figure(data=go.Heatmap(
                z=z_data,
                x=hours,
                y=outlets,
                colorscale=[[0, BACKGROUND_LIGHTER], [0.3, PRIMARY_LIGHT], [0.7, PRIMARY_MEDIUM], [1, PRIMARY_DARK]],
                hoverongaps=False
            ))
            heatmap.update_layout(
                title={'text': 'Order Volume Heatmap by Hour', 'font': {'color': PRIMARY_DARK, 'size': 16}},
                xaxis_title='Hour of Day',
                yaxis_title='Outlet',
                height=400,
                paper_bgcolor=BACKGROUND_WHITE,
                plot_bgcolor=BACKGROUND_WHITE,
                font={'color': PRIMARY_DARK}
            )
            charts['heatmap'] = json.dumps(heatmap, cls=plotly.utils.PlotlyJSONEncoder)
        
        # Daily patterns
        if 'dailyPatterns' in data:
            daily_data = data['dailyPatterns']
            days = list(daily_data.keys())
            counts = list(daily_data.values())
            
            daily_chart = go.Figure(data=go.Bar(
                x=days,
                y=counts,
                marker_color=PRIMARY_DARK,
                marker_line=dict(color=PRIMARY_MEDIUM, width=1)
            ))
            daily_chart.update_layout(
                title={'text': 'Orders by Day of Week', 'font': {'color': PRIMARY_DARK, 'size': 16}},
                xaxis_title='Day',
                yaxis_title='Order Count',
                height=400,
                paper_bgcolor=BACKGROUND_WHITE,
                plot_bgcolor=BACKGROUND_WHITE,
                font={'color': PRIMARY_DARK}
            )
            charts['daily_patterns'] = json.dumps(daily_chart, cls=plotly.utils.PlotlyJSONEncoder)
    
    elif analysis_type == 'customer-demographics' or analysis_type == 'customer-seasonal':
        # Age distribution
        if 'ageDistribution' in data:
            age_data = data['ageDistribution']
            labels = list(age_data.keys())
            values = list(age_data.values())
            
            age_chart = go.Figure(data=go.Pie(
                labels=labels,
                values=values,
                hole=0.3,
                marker_colors=CUSTOM_COLORS
            ))
            age_chart.update_layout(
                title={'text': 'Customer Age Distribution', 'font': {'color': PRIMARY_DARK, 'size': 16}},
                height=400,
                paper_bgcolor=BACKGROUND_WHITE,
                font={'color': PRIMARY_DARK}
            )
            charts['age_distribution'] = json.dumps(age_chart, cls=plotly.utils.PlotlyJSONEncoder)
        
        # Gender distribution
        if 'genderDistribution' in data:
            gender_data = data['genderDistribution']
            genders = list(gender_data.keys())
            counts = list(gender_data.values())
            
            gender_chart = go.Figure(data=go.Bar(
                x=genders,
                y=counts,
                marker_color=[PRIMARY_DARK, PRIMARY_MEDIUM, PRIMARY_LIGHT]
            ))
            gender_chart.update_layout(
                title={'text': 'Customer Gender Distribution', 'font': {'color': PRIMARY_DARK, 'size': 16}},
                xaxis_title='Gender',
                yaxis_title='Count',
                height=400,
                paper_bgcolor=BACKGROUND_WHITE,
                plot_bgcolor=BACKGROUND_WHITE,
                font={'color': PRIMARY_DARK}
            )
            charts['gender_distribution'] = json.dumps(gender_chart, cls=plotly.utils.PlotlyJSONEncoder)
        
        # Loyalty distribution
        if 'loyaltyGroupAnalysis' in data and 'distribution' in data['loyaltyGroupAnalysis']:
            loyalty_data = data['loyaltyGroupAnalysis']['distribution']
            groups = list(loyalty_data.keys())
            counts = list(loyalty_data.values())
            
            loyalty_chart = go.Figure(data=go.Pie(
                labels=groups,
                values=counts,
                marker_colors=CUSTOM_COLORS
            ))
            loyalty_chart.update_layout(
                title={'text': 'Customer Loyalty Distribution', 'font': {'color': PRIMARY_DARK, 'size': 16}},
                height=400,
                paper_bgcolor=BACKGROUND_WHITE,
                font={'color': PRIMARY_DARK}
            )
            charts['loyalty_distribution'] = json.dumps(loyalty_chart, cls=plotly.utils.PlotlyJSONEncoder)
    
    elif analysis_type == 'menu-analysis':
        # Popular items
        if 'popularItems' in data:
            items = data['popularItems'][:10]
            item_names = [item['itemName'] for item in items]
            order_counts = [item['orderCount'] for item in items]
            
            popular_chart = go.Figure(data=go.Bar(
                x=order_counts,
                y=item_names,
                orientation='h',
                marker_color='lightcoral'
            ))
            popular_chart.update_layout(
                title='Top 10 Popular Menu Items',
                xaxis_title='Order Count',
                yaxis_title='Menu Item',
                height=500
            )
            charts['popular_items'] = json.dumps(popular_chart, cls=plotly.utils.PlotlyJSONEncoder)
        
        # Category analysis
        if 'categoryAnalysis' in data and 'ordersByCategory' in data['categoryAnalysis']:
            category_data = data['categoryAnalysis']['ordersByCategory']
            categories = list(category_data.keys())
            counts = list(category_data.values())
            
            category_chart = go.Figure(data=go.Pie(
                labels=categories,
                values=counts
            ))
            category_chart.update_layout(
                title='Orders by Menu Category',
                height=400
            )
            charts['category_analysis'] = json.dumps(category_chart, cls=plotly.utils.PlotlyJSONEncoder)
        
        # Spice level preferences
        if 'spiceLevelPreferences' in data:
            spice_data = data['spiceLevelPreferences']
            spice_levels = list(spice_data.keys())
            counts = list(spice_data.values())
            
            spice_chart = go.Figure(data=go.Bar(
                x=spice_levels,
                y=counts,
                marker_color='red'
            ))
            spice_chart.update_layout(
                title='Spice Level Preferences',
                xaxis_title='Spice Level',
                yaxis_title='Order Count',
                height=400
            )
            charts['spice_preferences'] = json.dumps(spice_chart, cls=plotly.utils.PlotlyJSONEncoder)
    
    elif analysis_type == 'revenue-analysis':
        # Daily revenue
        if 'dailyRevenue' in data:
            daily_revenue = data['dailyRevenue']
            dates = list(daily_revenue.keys())
            revenues = list(daily_revenue.values())
            
            daily_chart = go.Figure(data=go.Scatter(
                x=dates,
                y=revenues,
                mode='lines+markers',
                line=dict(color='green')
            ))
            daily_chart.update_layout(
                title='Daily Revenue Trend',
                xaxis_title='Date',
                yaxis_title='Revenue (LKR)',
                height=400
            )
            charts['daily_revenue'] = json.dumps(daily_chart, cls=plotly.utils.PlotlyJSONEncoder)
        
        # Payment methods
        if 'paymentMethodAnalysis' in data and 'ordersByPaymentMethod' in data['paymentMethodAnalysis']:
            payment_data = data['paymentMethodAnalysis']['ordersByPaymentMethod']
            methods = list(payment_data.keys())
            counts = list(payment_data.values())
            
            payment_chart = go.Figure(data=go.Pie(
                labels=methods,
                values=counts
            ))
            payment_chart.update_layout(
                title='Orders by Payment Method',
                height=400
            )
            charts['payment_methods'] = json.dumps(payment_chart, cls=plotly.utils.PlotlyJSONEncoder)
        
        # Outlet revenue comparison
        if 'outletRevenue' in data:
            outlet_data = data['outletRevenue']
            outlets = list(outlet_data.keys())
            revenues = [outlet_data[outlet]['revenue'] for outlet in outlets]
            
            outlet_chart = go.Figure(data=go.Bar(
                x=outlets,
                y=revenues,
                marker_color='gold'
            ))
            outlet_chart.update_layout(
                title='Revenue by Outlet',
                xaxis_title='Outlet',
                yaxis_title='Revenue (LKR)',
                height=400
            )
            charts['outlet_revenue'] = json.dumps(outlet_chart, cls=plotly.utils.PlotlyJSONEncoder)
    
    elif analysis_type == 'anomaly-detection':
        # Severity distribution pie chart
        if 'severityDistribution' in data:
            severity_data = data['severityDistribution']
            labels = list(severity_data.keys())
            values = list(severity_data.values())
            colors = ['#dc3545', '#ffc107', '#28a745']  # Red, Yellow, Green
            
            severity_chart = go.Figure(data=go.Pie(
                labels=labels,
                values=values,
                marker_colors=colors
            ))
            severity_chart.update_layout(
                title='Anomaly Severity Distribution',
                height=400
            )
            charts['severity_distribution'] = json.dumps(severity_chart, cls=plotly.utils.PlotlyJSONEncoder)
        
        # Anomaly trends over time
        if 'anomalyTrends' in data:
            trends_data = data['anomalyTrends']
            dates = list(trends_data.keys())
            counts = list(trends_data.values())
            
            trends_chart = go.Figure(data=go.Scatter(
                x=dates,
                y=counts,
                mode='lines+markers',
                line=dict(color='red', width=3),
                marker=dict(size=8)
            ))
            trends_chart.update_layout(
                title='Anomaly Detection Trends',
                xaxis_title='Date',
                yaxis_title='Number of Anomalies',
                height=400
            )
            charts['anomaly_trends'] = json.dumps(trends_chart, cls=plotly.utils.PlotlyJSONEncoder)
        
        # Preparation time anomalies scatter plot
        if 'preparationTimeAnomalies' in data:
            prep_anomalies = data['preparationTimeAnomalies']
            order_ids = [anomaly['orderId'] for anomaly in prep_anomalies]
            prep_times = [anomaly['preparationTime'] for anomaly in prep_anomalies]
            expected_times = [anomaly['expectedTime'] for anomaly in prep_anomalies]
            severities = [anomaly['severity'] for anomaly in prep_anomalies]
            
            # Color mapping for severity
            color_map = {'HIGH': 'red', 'MEDIUM': 'orange', 'LOW': 'yellow'}
            colors = [color_map.get(sev, 'blue') for sev in severities]
            
            prep_chart = go.Figure()
            prep_chart.add_trace(go.Scatter(
                x=order_ids,
                y=prep_times,
                mode='markers',
                marker=dict(color=colors, size=12),
                name='Actual Prep Time',
                text=[f'Severity: {sev}' for sev in severities],
                hovertemplate='Order: %{x}<br>Prep Time: %{y} min<br>%{text}<extra></extra>'
            ))
            prep_chart.add_trace(go.Scatter(
                x=order_ids,
                y=expected_times,
                mode='markers',
                marker=dict(color='green', size=8),
                name='Expected Prep Time'
            ))
            prep_chart.update_layout(
                title='Preparation Time Anomalies',
                xaxis_title='Order ID',
                yaxis_title='Preparation Time (minutes)',
                height=400
            )
            charts['prep_time_anomalies'] = json.dumps(prep_chart, cls=plotly.utils.PlotlyJSONEncoder)
    
    elif analysis_type == 'branch-performance':
        # Branch revenue comparison
        if 'branchRankings' in data:
            rankings = data['branchRankings']
            branch_names = [branch['branchName'] for branch in rankings]
            revenues = [branch['revenue'] for branch in rankings]
            
            revenue_chart = go.Figure(data=go.Bar(
                x=branch_names,
                y=revenues,
                marker_color=['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728']
            ))
            revenue_chart.update_layout(
                title='Branch Revenue Comparison',
                xaxis_title='Branch',
                yaxis_title='Revenue (LKR)',
                height=400,
                xaxis_tickangle=-45
            )
            charts['branch_revenue'] = json.dumps(revenue_chart, cls=plotly.utils.PlotlyJSONEncoder)
        
        # Performance metrics radar chart
        if 'performanceMetrics' in data:
            metrics = data['performanceMetrics']
            outlets = list(metrics.keys())
            
            # Create radar chart data
            categories = ['Order Completion Rate', 'Customer Retention Rate', 'Avg Order Value (scaled)', 'Revenue (scaled)']
            
            radar_chart = go.Figure()
            
            colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728']
            for i, outlet in enumerate(outlets):
                outlet_metrics = metrics[outlet]
                values = [
                    outlet_metrics['orderCompletionRate'],
                    outlet_metrics['customerRetentionRate'],
                    outlet_metrics['averageOrderValue'] / 50,  # Scale down for radar
                    outlet_metrics['totalRevenue'] / 20000    # Scale down for radar
                ]
                
                radar_chart.add_trace(go.Scatterpolar(
                    r=values,
                    theta=categories,
                    fill='toself',
                    name=f'Outlet {outlet}',
                    line_color=colors[i % len(colors)]
                ))
            
            radar_chart.update_layout(
                polar=dict(
                    radialaxis=dict(
                        visible=True,
                        range=[0, 100]
                    )),
                title='Branch Performance Metrics Comparison',
                height=500
            )
            charts['performance_radar'] = json.dumps(radar_chart, cls=plotly.utils.PlotlyJSONEncoder)
        
        # Efficiency analysis
        if 'efficiencyAnalysis' in data:
            efficiency = data['efficiencyAnalysis']
            outlets = list(efficiency.keys())
            service_times = [efficiency[outlet]['averageServiceTime'] for outlet in outlets]
            capacity_utilization = [efficiency[outlet]['capacityUtilization'] for outlet in outlets]
            
            efficiency_chart = go.Figure()
            efficiency_chart.add_trace(go.Bar(
                name='Avg Service Time',
                x=outlets,
                y=service_times,
                yaxis='y',
                marker_color='lightblue'
            ))
            efficiency_chart.add_trace(go.Scatter(
                name='Capacity Utilization %',
                x=outlets,
                y=capacity_utilization,
                yaxis='y2',
                mode='lines+markers',
                line=dict(color='red', width=3),
                marker=dict(size=8)
            ))
            
            efficiency_chart.update_layout(
                title='Branch Efficiency Analysis',
                xaxis_title='Outlet',
                yaxis=dict(title='Service Time (minutes)', side='left'),
                yaxis2=dict(title='Capacity Utilization (%)', side='right', overlaying='y'),
                height=400
            )
            charts['efficiency_analysis'] = json.dumps(efficiency_chart, cls=plotly.utils.PlotlyJSONEncoder)
        
        # Monthly trends
        if 'monthlyTrends' in data:
            trends = data['monthlyTrends']
            months = ['Nov', 'Dec', 'Jan']
            
            trends_chart = go.Figure()
            colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728']
            
            for i, outlet in enumerate(trends.keys()):
                outlet_name = f'Outlet {outlet}'
                revenues = [trends[outlet][month] for month in months]
                
                trends_chart.add_trace(go.Scatter(
                    x=months,
                    y=revenues,
                    mode='lines+markers',
                    name=outlet_name,
                    line=dict(color=colors[i % len(colors)], width=3),
                    marker=dict(size=8)
                ))
            
            trends_chart.update_layout(
                title='Monthly Revenue Trends by Branch',
                xaxis_title='Month',
                yaxis_title='Revenue (LKR)',
                height=400
            )
            charts['monthly_trends'] = json.dumps(trends_chart, cls=plotly.utils.PlotlyJSONEncoder)
    
    return charts

@app.route('/overview')
def overview():
    """Overview dashboard page"""
    return render_template('dashboard_overview.html', outlets=MOCK_OUTLETS)

@app.route('/')
def index():
    """Home page with module selection"""
    return render_template('index.html', outlets=MOCK_OUTLETS)

@app.route('/api/outlets')
def get_outlets():
    """Get list of outlets"""
    return jsonify(MOCK_OUTLETS)

@app.route('/api/analytics/<analysis_type>')
def get_analytics(analysis_type):
    """Mock analytics data"""
    try:
        if analysis_type == 'peak-dining':
            data = generate_mock_peak_dining_data()
        elif analysis_type == 'customer-demographics':
            data = generate_mock_customer_demographics()
        elif analysis_type == 'customer-seasonal':
            data = generate_mock_customer_demographics()
        elif analysis_type == 'menu-analysis':
            data = generate_mock_menu_analysis()
        elif analysis_type == 'revenue-analysis':
            data = generate_mock_revenue_analysis()
        elif analysis_type == 'anomaly-detection':
            data = {
                "preparationTimeAnomalies": [
                    {"orderId": "O1234", "outletId": "OUT01", "preparationTime": 85, "expectedTime": 25, "severity": "HIGH", "zScore": 3.2},
                    {"orderId": "O1235", "outletId": "OUT02", "preparationTime": 65, "expectedTime": 30, "severity": "MEDIUM", "zScore": 2.8},
                    {"orderId": "O1236", "outletId": "OUT01", "preparationTime": 75, "expectedTime": 25, "severity": "HIGH", "zScore": 3.0},
                    {"orderId": "O1237", "outletId": "OUT03", "preparationTime": 55, "expectedTime": 28, "severity": "MEDIUM", "zScore": 2.5},
                    {"orderId": "O1238", "outletId": "OUT04", "preparationTime": 45, "expectedTime": 22, "severity": "LOW", "zScore": 2.1}
                ],
                "orderVolumeAnomalies": [
                    {"outletId": "OUT01", "hour": 14, "orderCount": 85, "expectedCount": 45, "severity": "HIGH"},
                    {"outletId": "OUT02", "hour": 19, "orderCount": 120, "expectedCount": 80, "severity": "MEDIUM"},
                    {"outletId": "OUT03", "hour": 12, "orderCount": 15, "expectedCount": 35, "severity": "MEDIUM"}
                ],
                "revenueAnomalies": [
                    {"outletId": "OUT01", "date": "2025-01-15", "revenue": 185000, "expectedRevenue": 95000, "severity": "HIGH"},
                    {"outletId": "OUT02", "date": "2025-01-14", "revenue": 45000, "expectedRevenue": 110000, "severity": "MEDIUM"}
                ],
                "alertLogs": [
                    {"alertId": "PREP_TIME_O1234", "type": "LONG_PREPARATION_TIME", "severity": "HIGH", "message": "Order O1234 took 85 minutes to prepare", "timestamp": "2025-01-17 14:30:00"},
                    {"alertId": "HIGH_VALUE_O1236", "type": "HIGH_VALUE_ORDER", "severity": "LOW", "message": "High value order: 8500 LKR", "timestamp": "2025-01-17 13:45:00"},
                    {"alertId": "VOLUME_SPIKE_OUT01", "type": "ORDER_VOLUME_SPIKE", "severity": "MEDIUM", "message": "Unusual order volume spike at OUT01", "timestamp": "2025-01-17 12:15:00"},
                    {"alertId": "REVENUE_DROP_OUT02", "type": "REVENUE_ANOMALY", "severity": "HIGH", "message": "Significant revenue drop detected", "timestamp": "2025-01-17 11:30:00"}
                ],
                "severityDistribution": {
                    "HIGH": 8, "MEDIUM": 12, "LOW": 5
                },
                "anomalyTrends": {
                    "2025-01-10": 3, "2025-01-11": 5, "2025-01-12": 2, "2025-01-13": 7, 
                    "2025-01-14": 9, "2025-01-15": 4, "2025-01-16": 6, "2025-01-17": 8
                }
            }
        elif analysis_type == 'branch-performance':
            data = {
                "branchRankings": [
                    {"outletId": "OUT02", "branchName": "City Center - Colombo", "revenue": 1200000, "orderCount": 580, "averageOrderValue": 2068, "customerCount": 420, "efficiency": 85},
                    {"outletId": "OUT01", "branchName": "Ocean View - Galle", "revenue": 980000, "orderCount": 450, "averageOrderValue": 2177, "customerCount": 380, "efficiency": 78},
                    {"outletId": "OUT04", "branchName": "Hill Station - Kandy", "revenue": 850000, "orderCount": 380, "averageOrderValue": 2236, "customerCount": 320, "efficiency": 72},
                    {"outletId": "OUT03", "branchName": "Beach Side - Negombo", "revenue": 720000, "orderCount": 320, "averageOrderValue": 2250, "customerCount": 280, "efficiency": 68}
                ],
                "performanceMetrics": {
                    "OUT01": {"totalRevenue": 980000, "averageOrderValue": 2177, "averagePreparationTime": 28.5, "orderCompletionRate": 94.2, "customerRetentionRate": 76.8},
                    "OUT02": {"totalRevenue": 1200000, "averageOrderValue": 2068, "averagePreparationTime": 25.3, "orderCompletionRate": 96.8, "customerRetentionRate": 82.1},
                    "OUT03": {"totalRevenue": 720000, "averageOrderValue": 2250, "averagePreparationTime": 32.1, "orderCompletionRate": 91.5, "customerRetentionRate": 71.3},
                    "OUT04": {"totalRevenue": 850000, "averageOrderValue": 2236, "averagePreparationTime": 29.8, "orderCompletionRate": 93.7, "customerRetentionRate": 74.9}
                },
                "efficiencyAnalysis": {
                    "OUT01": {"averageServiceTime": 45.2, "capacityUtilization": 67.5, "peakHourPerformance": {"peakHour": 19, "peakHourOrders": 45}},
                    "OUT02": {"averageServiceTime": 42.8, "capacityUtilization": 78.3, "peakHourPerformance": {"peakHour": 12, "peakHourOrders": 62}},
                    "OUT03": {"averageServiceTime": 48.9, "capacityUtilization": 58.2, "peakHourPerformance": {"peakHour": 20, "peakHourOrders": 38}},
                    "OUT04": {"averageServiceTime": 46.7, "capacityUtilization": 65.1, "peakHourPerformance": {"peakHour": 18, "peakHourOrders": 42}}
                },
                "monthlyTrends": {
                    "OUT01": {"Nov": 890000, "Dec": 920000, "Jan": 980000},
                    "OUT02": {"Nov": 1150000, "Dec": 1180000, "Jan": 1200000},
                    "OUT03": {"Nov": 680000, "Dec": 700000, "Jan": 720000},
                    "OUT04": {"Nov": 820000, "Dec": 835000, "Jan": 850000}
                }
            }
        else:
            data = {"error": "Unknown analysis type"}
        
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/charts/<analysis_type>')
def get_charts(analysis_type):
    """Generate charts for analysis"""
    try:
        print(f"Charts requested for: {analysis_type}")  # Debug log
        
        # Get the data first
        if analysis_type == 'peak-dining':
            data = generate_mock_peak_dining_data()
        elif analysis_type == 'customer-demographics':
            data = generate_mock_customer_demographics()
        elif analysis_type == 'menu-analysis':
            data = generate_mock_menu_analysis()
        elif analysis_type == 'revenue-analysis':
            data = generate_mock_revenue_analysis()
        elif analysis_type == 'customer-seasonal':
            data = generate_mock_customer_demographics()  # Reuse for seasonal
        elif analysis_type == 'anomaly-detection':
            # Get anomaly data for charts
            response = get_analytics('anomaly-detection')
            data = response.get_json()
        elif analysis_type == 'branch-performance':
            # Get branch performance data for charts
            response = get_analytics('branch-performance')
            data = response.get_json()
        else:
            return jsonify({"error": "Charts not available for this analysis type"})
        
        # Create charts
        charts = create_charts_for_analysis(analysis_type, data)
        print(f"Generated {len(charts)} charts for {analysis_type}")  # Debug log
        return jsonify(charts)
    except Exception as e:
        print(f"Error generating charts: {str(e)}")  # Debug log
        return jsonify({"error": str(e)}), 500

@app.route('/analysis/<analysis_type>')
def analysis_page(analysis_type):
    """Individual analysis pages"""
    return render_template('analysis.html', analysis_type=analysis_type, outlets=MOCK_OUTLETS)

@app.route('/reports/')
def reports():
    """Reports page"""
    return render_template('reports.html', outlets=MOCK_OUTLETS)

@app.route('/test-charts')
def test_charts():
    """Test page for debugging charts"""
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Chart Test</title>
        <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
    </head>
    <body>
        <h1>Chart Test</h1>
        <div id="testChart" style="height: 400px;"></div>
        
        <script>
        fetch('/charts/peak-dining')
            .then(response => response.json())
            .then(charts => {
                console.log('Charts received:', charts);
                if (charts.heatmap) {
                    const chartData = JSON.parse(charts.heatmap);
                    Plotly.newPlot('testChart', chartData.data, chartData.layout);
                }
            })
            .catch(error => console.error('Error:', error));
        </script>
    </body>
    </html>
    '''

@app.route('/home')
def home():
    """Home page with module selection"""
    return render_template('index.html', outlets=MOCK_OUTLETS)

@app.route('/dashboard/')
def dashboard():
    """Dashboard page"""
    return render_template('dashboard_overview.html', outlets=MOCK_OUTLETS)

if __name__ == '__main__':
    print("="*60)
    print("RESTAURANT ANALYTICS SYSTEM - ENHANCED DEMO")
    print("="*60)
    print("✅ Interactive Charts & Visualizations")
    print("✅ All 7 Analytics Modules")
    print("✅ Responsive Dashboard")
    print("✅ Real-time Data Display")
    print("="*60)
    print("Frontend running at: http://localhost:5000")
    print("="*60)
    app.run(debug=True, host='0.0.0.0', port=5000)