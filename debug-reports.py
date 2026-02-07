#!/usr/bin/env python3
"""
Debug script to check reports route data processing
"""

import sys
import os
sys.path.append('frontend')

from data_processor import data_processor

def debug_outlet_data():
    """Debug outlet data processing"""
    print("🔍 Debugging Outlet Data Processing")
    print("=" * 50)
    
    try:
        # Test get_outlets method
        outlets = data_processor.get_outlets()
        print(f"✅ Found {len(outlets)} outlets from get_outlets()")
        
        for i, outlet in enumerate(outlets, 1):
            print(f"\n{i}. Outlet ID: {outlet['id']}")
            print(f"   Name: {outlet['name']}")
            print(f"   Borough: {outlet['borough']}")
            print(f"   Capacity: {outlet['capacity']}")
            
            # Test revenue analysis for this outlet
            print(f"   Testing revenue analysis...")
            revenue_data = data_processor.get_revenue_analysis(outlet['id'])
            
            if 'revenueSummary' in revenue_data:
                summary = revenue_data['revenueSummary']
                orders = summary.get('totalOrders', 0)
                revenue = summary.get('totalRevenue', 0)
                print(f"   ✅ Orders: {orders:,}")
                print(f"   ✅ Revenue: LKR {revenue:,.0f}")
            else:
                print(f"   ❌ No revenue summary found")
                print(f"   Available keys: {list(revenue_data.keys())}")
            
            # Test branch performance
            print(f"   Testing branch performance...")
            branch_data = data_processor.get_branch_performance(outlet['id'])
            
            if 'branchRankings' in branch_data:
                for branch in branch_data['branchRankings']:
                    if branch['branchName'] == outlet['name']:
                        customers = branch.get('customerCount', 0)
                        print(f"   ✅ Customers: {customers:,}")
                        break
                else:
                    print(f"   ⚠️  Branch not found in rankings")
            else:
                print(f"   ❌ No branch rankings found")
                print(f"   Available keys: {list(branch_data.keys())}")
                
    except Exception as e:
        print(f"❌ Error debugging outlet data: {e}")
        import traceback
        traceback.print_exc()

def test_reports_route_logic():
    """Test the reports route logic"""
    print("\n🔍 Testing Reports Route Logic")
    print("=" * 50)
    
    try:
        outlets = data_processor.get_outlets()
        
        # Simulate the reports route logic
        outlets_with_data = []
        for outlet in outlets:
            outlet_id = outlet['id']
            
            # Get revenue analysis for this outlet
            revenue_data = data_processor.get_revenue_analysis(outlet_id)
            
            # Get branch performance data
            branch_data = data_processor.get_branch_performance(outlet_id)
            
            # Calculate outlet metrics from real data
            outlet_metrics = {
                'id': outlet_id,
                'name': outlet['name'],
                'borough': outlet['borough'],
                'capacity': outlet['capacity'],
                'status': 'Active',
                'orders': 0,
                'revenue': 0,
                'customers': 0
            }
            
            # Extract real metrics from revenue data
            if 'revenueSummary' in revenue_data:
                outlet_metrics['orders'] = revenue_data['revenueSummary'].get('totalOrders', 0)
                outlet_metrics['revenue'] = revenue_data['revenueSummary'].get('totalRevenue', 0)
            
            # Extract customer count from branch data
            if 'branchRankings' in branch_data:
                for branch in branch_data['branchRankings']:
                    if branch['branchName'] == outlet['name']:
                        outlet_metrics['customers'] = branch.get('customerCount', 0)
                        break
            
            outlets_with_data.append(outlet_metrics)
            
            print(f"\n✅ {outlet_metrics['name']} - {outlet_metrics['borough']}")
            print(f"   Orders: {outlet_metrics['orders']:,}")
            print(f"   Revenue: LKR {outlet_metrics['revenue']:,.0f}")
            print(f"   Customers: {outlet_metrics['customers']:,}")
        
        print(f"\n✅ Successfully processed {len(outlets_with_data)} outlets with data")
        
    except Exception as e:
        print(f"❌ Error testing reports route logic: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    debug_outlet_data()
    test_reports_route_logic()