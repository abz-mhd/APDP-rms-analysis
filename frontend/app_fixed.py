#!/usr/bin/env python3
"""Fixed Flask application for Restaurant Analytics System"""

from flask import Flask, render_template, request, jsonify, send_file
import requests
import json
import os
import sys

# Add current directory to Python path
sys.path.insert(0, os.path.dirname(__file__))

# Import data processor first
from data_processor import data_processor

# Import blueprints
from routes.dashboard import dashboard_bp
from routes.reports import reports_bp
from routes.charts import charts_bp

app = Flask(__name__)
app.secret_key = 'restaurant-analytics-secret-key'

# Register blueprints
app.register_blueprint(dashboard_bp, url_prefix='/dashboard')
app.register_blueprint(reports_bp, url_prefix='/reports')
app.register_blueprint(charts_bp, url_prefix='/charts')

@app.route('/')
def index():
    """Main dashboard page - redirect to dashboard overview"""
    try:
        outlets = data_processor.get_outlets()
        return render_template('dashboard_ultra.html', outlets=outlets)
    except Exception as e:
        return render_template('dashboard_ultra.html', outlets=[], error=str(e))

@app.route('/dashboard-overview')
def dashboard_overview():
    """Dashboard overview page"""
    try:
        outlets = data_processor.get_outlets()
        return render_template('dashboard_ultra.html', outlets=outlets)
    except Exception as e:
        return render_template('dashboard_ultra.html', outlets=[], error=str(e))

@app.route('/analysis')
def analysis():
    """Analysis page"""
    try:
        outlets = data_processor.get_outlets()
        return render_template('analysis.html', outlets=outlets)
    except Exception as e:
        return render_template('analysis.html', outlets=[], error=str(e))

@app.route('/analysis/<analysis_type>')
def analysis_specific(analysis_type):
    """Specific analysis page"""
    try:
        outlets = data_processor.get_outlets()
        
        # Validate analysis type
        valid_types = [
            'peak-dining', 'customer-demographics', 'customer-seasonal', 'seasonal-behavior',
            'menu-analysis', 'revenue-analysis', 'anomaly-detection', 'branch-performance'
        ]
        
        if analysis_type not in valid_types:
            return render_template('analysis_complete.html', outlets=outlets, analysis_type='general', error=f'Invalid analysis type: {analysis_type}')
        
        return render_template('analysis_complete.html', outlets=outlets, analysis_type=analysis_type)
        
    except Exception as e:
        return render_template('analysis_complete.html', outlets=[], analysis_type='general', error=str(e))

# Reports route is handled by the reports blueprint

@app.route('/api/outlets')
def get_outlets():
    """Get list of outlets from real data"""
    try:
        outlets = data_processor.get_outlets()
        return jsonify(outlets)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/analytics/<analysis_type>')
def get_analytics(analysis_type):
    """Get analytics data from real dataset"""
    try:
        # Get query parameters
        outlet_id = request.args.get('outletId')
        season = request.args.get('season')
        festival = request.args.get('festival')
        
        print(f"Analytics request: {analysis_type}, outlet: {outlet_id}, season: {season}")
        
        # Route to appropriate analysis function
        if analysis_type == 'peak-dining':
            data = data_processor.get_peak_dining_analysis(outlet_id, season, festival)
        elif analysis_type == 'customer-demographics':
            data = data_processor.get_customer_demographics(outlet_id, season, festival)
        elif analysis_type == 'customer-seasonal' or analysis_type == 'seasonal-behavior':
            data = data_processor.get_seasonal_behavior(outlet_id, season, festival)
        elif analysis_type == 'menu-analysis':
            data = data_processor.get_menu_analysis(outlet_id, season, festival)
        elif analysis_type == 'revenue-analysis':
            data = data_processor.get_revenue_analysis(outlet_id, season, festival)
        elif analysis_type == 'anomaly-detection':
            data = data_processor.get_anomaly_detection(outlet_id, season, festival)
        elif analysis_type == 'branch-performance':
            data = data_processor.get_branch_performance(outlet_id, season, festival)
        elif analysis_type == 'outlets':
            data = data_processor.get_outlets()
        else:
            return jsonify({'error': 'Invalid analysis type'}), 400
        
        print(f"Analytics response keys: {list(data.keys()) if isinstance(data, dict) else 'not dict'}")
        return jsonify(data)
            
    except Exception as e:
        print(f"Analytics error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/health')
def health_check():
    """Health check endpoint to verify all analytics functions are working"""
    try:
        health_status = {
            'status': 'healthy',
            'dataset_loaded': len(data_processor.df) > 0,
            'record_count': len(data_processor.df),
            'csv_path': data_processor.csv_path,
            'csv_exists': os.path.exists(data_processor.csv_path) if data_processor.csv_path else False,
            'endpoints': {}
        }
        
        # Test each analytics endpoint
        test_endpoints = [
            'peak-dining',
            'customer-demographics', 
            'revenue-analysis',
            'menu-analysis',
            'branch-performance',
            'anomaly-detection'
        ]
        
        for endpoint in test_endpoints:
            try:
                if endpoint == 'peak-dining':
                    result = data_processor.get_peak_dining_analysis()
                elif endpoint == 'customer-demographics':
                    result = data_processor.get_customer_demographics()
                elif endpoint == 'revenue-analysis':
                    result = data_processor.get_revenue_analysis()
                elif endpoint == 'menu-analysis':
                    result = data_processor.get_menu_analysis()
                elif endpoint == 'branch-performance':
                    result = data_processor.get_branch_performance()
                elif endpoint == 'anomaly-detection':
                    result = data_processor.get_anomaly_detection()
                
                health_status['endpoints'][endpoint] = {
                    'status': 'error' if 'error' in result else 'ok',
                    'error': result.get('error', None),
                    'data_keys': list(result.keys()) if isinstance(result, dict) else 'not_dict'
                }
            except Exception as e:
                health_status['endpoints'][endpoint] = {
                    'status': 'error',
                    'error': str(e)
                }
        
        return jsonify(health_status)
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'error': str(e)
        }), 500

@app.route('/debug/data-status')
def debug_data_status():
    """Debug endpoint to check data loading status"""
    try:
        status = {
            'csv_path': data_processor.csv_path,
            'csv_exists': os.path.exists(data_processor.csv_path) if data_processor.csv_path else False,
            'dataframe_loaded': data_processor.df is not None,
            'dataframe_empty': data_processor.df.empty if data_processor.df is not None else True,
            'record_count': len(data_processor.df) if data_processor.df is not None else 0,
            'columns': list(data_processor.df.columns) if data_processor.df is not None and not data_processor.df.empty else [],
            'working_directory': os.getcwd(),
            'sample_data': data_processor.df.head(2).to_dict('records') if data_processor.df is not None and not data_processor.df.empty else []
        }
        
        return jsonify(status)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/forecast')
def get_forecast():
    """Get 6-month forecast"""
    try:
        outlet_id = request.args.get('outletId')
        forecast = data_processor.get_6_month_forecast(outlet_id)
        return jsonify(forecast)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Test endpoint to verify everything is working
@app.route('/test')
def test_page():
    """Simple test page"""
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>RestaurantIQ Analytics - System Test</title>
        <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
    </head>
    <body class="p-4">
        <h1>🎉 RestaurantIQ Analytics System is Working!</h1>
        <div class="alert alert-success">
            <h4>✅ System Status: OPERATIONAL</h4>
            <p><strong>Data Records:</strong> {len(data_processor.df):,}</p>
            <p><strong>CSV Path:</strong> {data_processor.csv_path}</p>
        </div>
        
        <div class="row">
            <div class="col-md-6">
                <h3>🔗 Test Links</h3>
                <ul class="list-group">
                    <li class="list-group-item"><a href="/api/health">Health Check</a></li>
                    <li class="list-group-item"><a href="/api/analytics/peak-dining">Peak Dining Data</a></li>
                    <li class="list-group-item"><a href="/charts/peak-dining">Peak Dining Charts</a></li>
                    <li class="list-group-item"><a href="/analysis/peak-dining">Peak Dining Page</a></li>
                </ul>
            </div>
            <div class="col-md-6">
                <h3>📊 Analytics Modules</h3>
                <ul class="list-group">
                    <li class="list-group-item"><a href="/analysis/peak-dining">Peak Dining Analysis</a></li>
                    <li class="list-group-item"><a href="/analysis/customer-demographics">Customer Demographics</a></li>
                    <li class="list-group-item"><a href="/analysis/menu-analysis">Menu Analysis</a></li>
                    <li class="list-group-item"><a href="/analysis/revenue-analysis">Revenue Analysis</a></li>
                </ul>
            </div>
        </div>
    </body>
    </html>
    """

if __name__ == '__main__':
    print(f"🚀 Starting RestaurantIQ Analytics System...")
    print(f"📊 Data loaded: {len(data_processor.df):,} records")
    print(f"🌐 Server will be available at: http://localhost:5002")
    print(f"🧪 Test page: http://localhost:5002/test")
    
    app.run(debug=True, host='0.0.0.0', port=5002)