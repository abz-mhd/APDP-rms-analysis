from flask import Flask, render_template, request, jsonify, send_file
import requests
import json
import os
import requests
import json
from routes.dashboard import dashboard_bp
from routes.reports import reports_bp
from routes.charts import charts_bp
from data_processor import data_processor

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
        return render_template('dashboard_overview.html', outlets=outlets)
    except Exception as e:
        return render_template('dashboard_overview.html', outlets=[], error=str(e))

@app.route('/dashboard-overview')
def dashboard_overview():
    """Dashboard overview page"""
    try:
        outlets = data_processor.get_outlets()
        return render_template('dashboard_overview.html', outlets=outlets)
    except Exception as e:
        return render_template('dashboard_overview.html', outlets=[], error=str(e))

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
            return render_template('analysis_fixed.html', outlets=outlets, analysis_type='general', error=f'Invalid analysis type: {analysis_type}')
        
        return render_template('analysis_fixed.html', outlets=outlets, analysis_type=analysis_type)
        
    except Exception as e:
        return render_template('analysis_fixed.html', outlets=[], analysis_type='general', error=str(e))

@app.route('/reports')
def reports():
    """Reports page"""
    try:
        outlets = data_processor.get_outlets()
        return render_template('reports.html', outlets=outlets)
    except Exception as e:
        return render_template('reports.html', outlets=[], error=str(e))

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
        
        return jsonify(data)
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/test-analysis/<analysis_type>')
def test_analysis(analysis_type):
    """Test analysis page with direct data loading"""
    try:
        # Get analytics data
        if analysis_type == 'peak-dining':
            analytics_data = data_processor.get_peak_dining_analysis()
        elif analysis_type == 'customer-demographics':
            analytics_data = data_processor.get_customer_demographics()
        elif analysis_type == 'menu-analysis':
            analytics_data = data_processor.get_menu_analysis()
        elif analysis_type == 'revenue-analysis':
            analytics_data = data_processor.get_revenue_analysis()
        elif analysis_type == 'branch-performance':
            analytics_data = data_processor.get_branch_performance()
        elif analysis_type == 'seasonal-behavior' or analysis_type == 'customer-seasonal':
            analytics_data = data_processor.get_seasonal_behavior()
        elif analysis_type == 'anomaly-detection':
            analytics_data = data_processor.get_anomaly_detection()
        else:
            return jsonify({'error': 'Invalid analysis type'}), 400
        
        # Get charts data
        charts_response = requests.get(f'http://localhost:5000/charts/{analysis_type}')
        charts_data = charts_response.json() if charts_response.status_code == 200 else {}
        
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Test {analysis_type}</title>
            <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
            <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
        </head>
        <body class="p-4">
            <h1>Test {analysis_type}</h1>
            <div class="row" id="charts"></div>
            <script>
                const charts = {json.dumps(charts_data)};
                console.log('Charts:', charts);
                
                let html = '';
                Object.keys(charts).forEach(chartId => {{
                    html += `<div class="col-md-6 mb-4">
                        <div class="card">
                            <div class="card-header"><h5>${{chartId}}</h5></div>
                            <div class="card-body">
                                <div id="${{chartId}}" style="height: 400px;"></div>
                            </div>
                        </div>
                    </div>`;
                }});
                
                document.getElementById('charts').innerHTML = html;
                
                setTimeout(() => {{
                    Object.keys(charts).forEach(chartId => {{
                        try {{
                            const chartData = JSON.parse(charts[chartId]);
                            Plotly.newPlot(chartId, chartData.data, chartData.layout, {{
                                responsive: true,
                                displayModeBar: false
                            }});
                            console.log('Rendered:', chartId);
                        }} catch (e) {{
                            console.error('Error rendering', chartId, e);
                            document.getElementById(chartId).innerHTML = '<div class="alert alert-danger">Error: ' + e.message + '</div>';
                        }}
                    }});
                }}, 500);
            </script>
        </body>
        </html>
        """
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/simple_test.html')
def simple_test():
    """Simple test page for charts"""
    return send_file('simple_test.html')

@app.route('/debug/<analysis_type>')
def debug_analysis(analysis_type):
    """Debug endpoint to check analysis data and charts"""
    try:
        # Test analytics data
        if analysis_type == 'peak-dining':
            analytics_data = data_processor.get_peak_dining_analysis()
        elif analysis_type == 'customer-demographics':
            analytics_data = data_processor.get_customer_demographics()
        elif analysis_type == 'menu-analysis':
            analytics_data = data_processor.get_menu_analysis()
        elif analysis_type == 'revenue-analysis':
            analytics_data = data_processor.get_revenue_analysis()
        elif analysis_type == 'branch-performance':
            analytics_data = data_processor.get_branch_performance()
        elif analysis_type == 'seasonal-behavior' or analysis_type == 'customer-seasonal':
            analytics_data = data_processor.get_seasonal_behavior()
        elif analysis_type == 'anomaly-detection':
            analytics_data = data_processor.get_anomaly_detection()
        else:
            return jsonify({'error': 'Invalid analysis type'}), 400
        
        # Test charts data
        charts_response = requests.get(f'http://localhost:5000/charts/{analysis_type}')
        charts_data = charts_response.json() if charts_response.status_code == 200 else {'error': f'Charts failed: {charts_response.status_code}'}
        
        return jsonify({
            'analysis_type': analysis_type,
            'analytics_data_keys': list(analytics_data.keys()) if isinstance(analytics_data, dict) else 'Not a dict',
            'analytics_has_error': 'error' in analytics_data if isinstance(analytics_data, dict) else False,
            'charts_data_keys': list(charts_data.keys()) if isinstance(charts_data, dict) else 'Not a dict',
            'charts_status': 'success' if charts_response.status_code == 200 else f'failed: {charts_response.status_code}',
            'charts_count': len(charts_data) if isinstance(charts_data, dict) and 'error' not in charts_data else 0
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/test_charts.html')
def test_charts():
    """Test page for charts"""
    return send_file('test_charts.html')

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

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)