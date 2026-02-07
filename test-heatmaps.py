#!/usr/bin/env python3
"""
Test script to verify heatmaps are working
"""

import requests
import json

def test_heatmaps():
    """Test if heatmaps are generated correctly"""
    print("🔥 Testing Heatmap Generation")
    print("=" * 50)
    
    # Test different analysis types for heatmaps
    analysis_types = [
        'peak-dining',
        'branch-performance', 
        'customer-demographics',
        'menu-analysis',
        'seasonal-behavior'
    ]
    
    for analysis_type in analysis_types:
        try:
            print(f"\n📊 Testing {analysis_type} heatmaps...")
            
            # Get charts for this analysis type
            response = requests.get(f'http://localhost:5002/charts/{analysis_type}')
            
            if response.status_code == 200:
                charts = response.json()
                
                # Look for heatmap charts
                heatmap_charts = [key for key in charts.keys() if 'heatmap' in key.lower()]
                
                if heatmap_charts:
                    print(f"  ✅ Found {len(heatmap_charts)} heatmap(s):")
                    for heatmap in heatmap_charts:
                        print(f"    🔥 {heatmap}")
                        
                        # Verify it's valid JSON
                        try:
                            chart_data = json.loads(charts[heatmap])
                            if 'data' in chart_data and len(chart_data['data']) > 0:
                                chart_type = chart_data['data'][0].get('type', 'unknown')
                                print(f"      Type: {chart_type}")
                            else:
                                print(f"      ⚠️  No data in chart")
                        except json.JSONDecodeError:
                            print(f"      ❌ Invalid JSON in chart")
                else:
                    print(f"  ❌ No heatmaps found")
                    print(f"  Available charts: {list(charts.keys())}")
            else:
                print(f"  ❌ Failed to get charts: {response.status_code}")
                
        except Exception as e:
            print(f"  ❌ Error testing {analysis_type}: {e}")
    
    print("\n" + "=" * 50)
    print("✅ Heatmap test completed!")

def test_specific_heatmap():
    """Test a specific heatmap in detail"""
    print("\n🔍 Testing Peak Dining Heatmap in Detail")
    print("=" * 40)
    
    try:
        response = requests.get('http://localhost:5002/charts/peak-dining')
        
        if response.status_code == 200:
            charts = response.json()
            
            if 'peak_dining_heatmap' in charts:
                print("✅ Peak dining heatmap found!")
                
                # Parse the chart data
                chart_data = json.loads(charts['peak_dining_heatmap'])
                
                if 'data' in chart_data and len(chart_data['data']) > 0:
                    heatmap_data = chart_data['data'][0]
                    
                    print(f"Chart type: {heatmap_data.get('type', 'unknown')}")
                    print(f"Colorscale: {heatmap_data.get('colorscale', 'unknown')}")
                    
                    if 'z' in heatmap_data:
                        z_data = heatmap_data['z']
                        print(f"Heatmap dimensions: {len(z_data)} x {len(z_data[0]) if z_data else 0}")
                        print(f"Sample data: {z_data[0][:5] if z_data and z_data[0] else 'No data'}")
                    
                    if 'x' in heatmap_data:
                        x_labels = heatmap_data['x']
                        print(f"X-axis labels: {x_labels[:5]}... ({len(x_labels)} total)")
                    
                    if 'y' in heatmap_data:
                        y_labels = heatmap_data['y']
                        print(f"Y-axis labels: {y_labels}")
                        
                else:
                    print("❌ No data in heatmap")
            else:
                print("❌ Peak dining heatmap not found")
                print(f"Available charts: {list(charts.keys())}")
        else:
            print(f"❌ Failed to get charts: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error testing specific heatmap: {e}")

if __name__ == "__main__":
    test_heatmaps()
    test_specific_heatmap()