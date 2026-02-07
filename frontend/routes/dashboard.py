from flask import Blueprint, render_template, jsonify
from data_processor import data_processor

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/overview')
def overview():
    """Dashboard overview"""
    try:
        outlets = data_processor.get_outlets()
        return render_template('dashboard_overview.html', outlets=outlets)
    except Exception as e:
        return render_template('dashboard_overview.html', outlets=[], error=str(e))

@dashboard_bp.route('/api/summary')
def get_summary():
    """Get dashboard summary data"""
    try:
        # Get basic metrics
        df = data_processor.df
        if df.empty:
            return jsonify({'error': 'No data available'})
        
        summary = {
            'totalOrders': len(df),
            'totalRevenue': float(df['total_price_lkr'].sum()),
            'totalCustomers': int(df['customer_id'].nunique()),
            'totalOutlets': int(df['outlet_id'].nunique()),
            'averageOrderValue': float(df['total_price_lkr'].mean())
        }
        
        return jsonify(summary)
    except Exception as e:
        return jsonify({'error': str(e)}), 500