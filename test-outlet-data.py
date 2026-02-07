#!/usr/bin/env python3
"""
Test script to verify outlet data with real metrics
"""

import requests
import json

def test_outlet_data():
    """Test if outlet data is loading with real metrics"""
    try:
        # Test the reports page
        response = requests.get('http://localhost:5002/reports')
        print(f"Reports page status: {response.status_code}")
        
        if response.status_code == 200:
            # Check if outlet data is in the response
            content = response.text
            
            # Look for outlet names
            outlets = ['Ocean View', 'City Square', 'Hillside', 'Seaside']
            found_outlets = []
            
            for outlet in outlets:
                if outlet in content:
                    found_outlets.append(outlet)
                    print(f"✅ Found outlet: {outlet}")
                else:
                    print(f"❌ Missing outlet: {outlet}")
            
            print(f"\nTotal outlets found: {len(found_outlets)}/4")
            
            # Check for metric values (should not be 0 or empty)
            if 'LKR 0' in content or 'Orders</div>' in content:
                print("⚠️  Warning: Some outlets may have zero values")
            else:
                print("✅ Outlets appear to have real data values")
                
        else:
            print(f"❌ Failed to load reports page: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error testing outlet data: {e}")

def test_api_data():
    """Test the API endpoints for outlet data"""
    try:
        # Test revenue analysis API
        response = requests.get('http://localhost:5002/reports/api/generate?type=summary')
        print(f"\nAPI status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            if 'revenueSummary' in data:
                summary = data['revenueSummary']
                print(f"✅ Total Revenue: LKR {summary.get('totalRevenue', 0):,.0f}")
                print(f"✅ Total Orders: {summary.get('totalOrders', 0):,}")
                print(f"✅ Avg Order Value: LKR {summary.get('averageOrderValue', 0):.2f}")
            else:
                print("❌ No revenue summary in API response")
        else:
            print(f"❌ API request failed: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error testing API: {e}")

if __name__ == "__main__":
    print("🧪 Testing Outlet Data with Real Metrics")
    print("=" * 50)
    
    test_outlet_data()
    test_api_data()
    
    print("\n" + "=" * 50)
    print("✅ Test completed!")