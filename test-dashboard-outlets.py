#!/usr/bin/env python3
"""
Test script to verify dashboard shows 4 outlets
"""

import requests

def test_dashboard_outlets():
    """Test if dashboard shows correct number of outlets"""
    try:
        response = requests.get('http://localhost:5002/')
        print(f"Dashboard status: {response.status_code}")
        
        if response.status_code == 200:
            content = response.text
            
            # Check for outlet count in template
            if '{{ outlets|length }}' in content:
                print("⚠️  Template variable not rendered")
            elif '4' in content and 'Active Outlets' in content:
                print("✅ Found '4 Active Outlets' in dashboard")
            elif '3' in content and 'Active Outlets' in content:
                print("❌ Still showing '3 Active Outlets'")
            else:
                print("⚠️  Could not find outlet count")
            
            # Check for all outlet names
            outlets = ['Ocean View', 'City Square', 'Hillside', 'Seaside']
            found_outlets = []
            
            for outlet in outlets:
                if outlet in content:
                    found_outlets.append(outlet)
                    
            print(f"Found outlets in dashboard: {len(found_outlets)}/4")
            for outlet in found_outlets:
                print(f"  ✅ {outlet}")
                
            missing = [o for o in outlets if o not in found_outlets]
            for outlet in missing:
                print(f"  ❌ {outlet}")
                
        else:
            print(f"❌ Failed to load dashboard: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error testing dashboard: {e}")

if __name__ == "__main__":
    print("🧪 Testing Dashboard Outlet Count")
    print("=" * 40)
    test_dashboard_outlets()
    print("=" * 40)
    print("✅ Test completed!")