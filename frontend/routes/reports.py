from flask import Blueprint, render_template, jsonify, request
from data_processor import data_processor

reports_bp = Blueprint('reports', __name__)

@reports_bp.route('/')
def reports():
    """Reports page with real outlet data"""
    try:
        print("🔍 DEBUG: Starting reports route")
        outlets = data_processor.get_outlets()
        print(f"🔍 DEBUG: Found {len(outlets)} outlets")
        
        # Get real data for each outlet
        outlets_with_data = []
        for outlet in outlets:
            print(f"🔍 DEBUG: Processing outlet {outlet['name']}")
            outlet_id = outlet['id']
            
            # Get revenue analysis for this outlet
            revenue_data = data_processor.get_revenue_analysis(outlet_id)
            print(f"🔍 DEBUG: Revenue data keys: {list(revenue_data.keys())}")
            
            # Get branch performance data
            branch_data = data_processor.get_branch_performance(outlet_id)
            print(f"🔍 DEBUG: Branch data keys: {list(branch_data.keys())}")
            
            # Calculate outlet metrics from real data
            outlet_metrics = {
                'id': outlet_id,
                'name': outlet['name'],
                'borough': outlet['borough'],
                'capacity': outlet['capacity'],
                'status': 'Active',  # All outlets are active
                'orders': 0,
                'revenue': 0,
                'customers': 0
            }
            
            # Extract real metrics from revenue data
            if 'revenueSummary' in revenue_data:
                outlet_metrics['orders'] = revenue_data['revenueSummary'].get('totalOrders', 0)
                outlet_metrics['revenue'] = revenue_data['revenueSummary'].get('totalRevenue', 0)
                print(f"🔍 DEBUG: {outlet['name']} - Orders: {outlet_metrics['orders']}, Revenue: {outlet_metrics['revenue']}")
            
            # Extract customer count from branch data
            if 'branchRankings' in branch_data:
                for branch in branch_data['branchRankings']:
                    if branch['branchName'] == outlet['name']:
                        outlet_metrics['customers'] = branch.get('customerCount', 0)
                        print(f"🔍 DEBUG: {outlet['name']} - Customers: {outlet_metrics['customers']}")
                        break
            
            outlets_with_data.append(outlet_metrics)
        
        print(f"🔍 DEBUG: Final outlets_with_data: {len(outlets_with_data)} outlets")
        print(f"🔍 DEBUG: Rendering reports_ultra.html template")
        return render_template('reports_ultra.html', outlets=outlets_with_data)
    except Exception as e:
        print(f"❌ ERROR in reports route: {e}")
        import traceback
        traceback.print_exc()
        return render_template('reports_ultra.html', outlets=[], error=str(e))

@reports_bp.route('/api/generate')
def generate_report():
    """Generate report data"""
    try:
        report_type = request.args.get('type', 'summary')
        outlet_id = request.args.get('outletId')
        
        if report_type == 'summary':
            data = data_processor.get_revenue_analysis(outlet_id)
        elif report_type == 'performance':
            data = data_processor.get_branch_performance(outlet_id)
        else:
            data = {'error': 'Invalid report type'}
        
        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500