#!/usr/bin/env python3
"""
Direct test of reports route
"""

import requests

def test_reports_page():
    """Test reports page directly"""
    try:
        response = requests.get('http://localhost:5002/reports')
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            content = response.text
            
            # Check for specific outlet data patterns
            patterns = [
                'Ocean View',
                'City Square', 
                'Hillside',
                'Seaside',
                'Negombo',
                'Galle',
                'Colombo',
                'Kandy',
                'LKR',
                'orders',
                'revenue',
                'customers'
            ]
            
            found_patterns = []
            for pattern in patterns:
                if pattern in content:
                    found_patterns.append(pattern)
                    
            print(f"Found patterns: {found_patterns}")
            
            # Look for specific outlet card structure
            if 'outlet-card' in content:
                print("✅ Found outlet-card class")
            else:
                print("❌ No outlet-card class found")
                
            if 'outlets-section' in content:
                print("✅ Found outlets-section")
            else:
                print("❌ No outlets-section found")
                
            # Check for template variables
            if '{{' in content or '{%' in content:
                print("⚠️  Found unrendered template variables")
                # Find and show them
                import re
                variables = re.findall(r'\{\{.*?\}\}|\{%.*?%\}', content)
                for var in variables[:5]:  # Show first 5
                    print(f"   {var}")
            else:
                print("✅ No unrendered template variables")
                
        else:
            print(f"❌ Failed to load page: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_reports_page()