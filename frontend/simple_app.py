#!/usr/bin/env python3
"""Simple test Flask app to verify everything works"""

from flask import Flask, jsonify, render_template_string
import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(__file__))

from data_processor import data_processor
from routes.charts import generate_peak_dining_charts

app = Flask(__name__)

@app.route('/')
def index():
    return render_template_string('''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Analytics Test</title>
        <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
    </head>
    <body class="p-4">
        <h1>Analytics System Test</h1>
        <div class="row">
            <div class="col-md-6">
                <div class="card">
                    <div class="card-header">System Status</div>
                    <div class="card-body">
                        <p><strong>Data Records:</strong> {{ record_count }}</p>
                        <p><strong>Status:</strong> <span class="badge bg-success">Working</span></p>
                        <button class="btn btn-primary" onclick="loadCharts()">Load Peak Dining Charts</button>
                    </div>
                </div>
            </div>
            <div class="col-md-6">
                <div class="card">
                    <div class="card-header">Quick Links</div>
                    <div class="card-body">
                        <a href="/api/test" class="btn btn-outline-primary btn-sm">Test API</a>
                        <a href="/api/peak-dining" class="btn btn-outline-primary btn-sm">Peak Dining Data</a>
                        <a href="/charts/peak-dining" class="btn btn-outline-primary btn-sm">Peak Dining Charts</a>
                    </div>
                </div>
            </div>
        </div>
        
        <div id="charts" class="row mt-4" style="display: none;">
            <!-- Charts will load here -->
        </div>
        
        <script>
        function loadCharts() {
            fetch('/charts/peak-dining')
                .then(response => response.json())
                .then(charts => {
                    console.log('Charts received:', charts);
                    displayCharts(charts);
                })
                .catch(error => {
                    console.error('Error:', error);
                    alert('Error loading charts: ' + error.message);
                });
        }
        
        function displayCharts(charts) {
            const container = document.getElementById('charts');
            let html = '';
            
            Object.keys(charts).forEach(chartId => {
                html += `
                    <div class="col-md-6 mb-4">
                        <div class="card">
                            <div class="card-header">${chartId.replace(/_/g, ' ')}</div>
                            <div class="card-body">
                                <div id="${chartId}" style="height: 400px;"></div>
                            </div>
                        </div>
                    </div>
                `;
            });
            
            container.innerHTML = html;
            container.style.display = 'block';
            
            // Render charts
            setTimeout(() => {
                Object.keys(charts).forEach(chartId => {
                    try {
                        const chartData = JSON.parse(charts[chartId]);
                        Plotly.newPlot(chartId, chartData.data, chartData.layout, {
                            responsive: true,
                            displayModeBar: false
                        });
                    } catch (e) {
                        console.error('Chart error:', chartId, e);
                        document.getElementById(chartId).innerHTML = '<div class="alert alert-danger">Error: ' + e.message + '</div>';
                    }
                });
            }, 500);
        }
        </script>
    </body>
    </html>
    ''', record_count=len(data_processor.df))

@app.route('/api/test')
def api_test():
    return jsonify({
        'status': 'success',
        'message': 'API is working!',
        'data_records': len(data_processor.df),
        'sample_data': data_processor.df.head(2).to_dict('records') if not data_processor.df.empty else []
    })

@app.route('/api/peak-dining')
def api_peak_dining():
    try:
        result = data_processor.get_peak_dining_analysis()
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/charts/peak-dining')
def charts_peak_dining():
    try:
        charts = generate_peak_dining_charts()
        return jsonify(charts)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    print(f"Starting simple test app with {len(data_processor.df)} records...")
    app.run(debug=True, host='0.0.0.0', port=5001)  # Use port 5001 to avoid conflicts