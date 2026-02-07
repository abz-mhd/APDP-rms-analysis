#!/usr/bin/env python3
"""Test all pages to ensure they're working"""

import requests
import sys

def test_page(url, page_name):
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200 and len(response.text) > 1000:
            print(f"✅ {page_name}: Working (Status: {response.status_code}, Size: {len(response.text)} chars)")
            return True
        else:
            print(f"❌ {page_name}: Failed (Status: {response.status_code}, Size: {len(response.text)} chars)")
            return False
    except Exception as e:
        print(f"❌ {page_name}: Error - {e}")
        return False

def main():
    base_url = "http://127.0.0.1:5002"
    
    pages_to_test = [
        (f"{base_url}/", "Home Dashboard"),
        (f"{base_url}/reports", "Reports Page"),
        (f"{base_url}/analysis/peak-dining", "Peak Dining Analysis"),
        (f"{base_url}/analysis/customer-demographics", "Customer Demographics"),
        (f"{base_url}/analysis/seasonal-behavior", "Seasonal Behavior"),
        (f"{base_url}/analysis/menu-analysis", "Menu Analysis"),
        (f"{base_url}/analysis/revenue-analysis", "Revenue Analysis"),
        (f"{base_url}/analysis/branch-performance", "Branch Performance"),
        (f"{base_url}/analysis/anomaly-detection", "Anomaly Detection"),
        (f"{base_url}/api/health", "Health API"),
        (f"{base_url}/api/outlets", "Outlets API"),
    ]
    
    print("🧪 Testing All Pages...")
    print("=" * 50)
    
    passed = 0
    total = len(pages_to_test)
    
    for url, name in pages_to_test:
        if test_page(url, name):
            passed += 1
    
    print("=" * 50)
    print(f"📊 Results: {passed}/{total} pages working ({(passed/total)*100:.1f}%)")
    
    if passed == total:
        print("🎉 All pages are working perfectly!")
        return True
    else:
        print(f"⚠️  {total - passed} pages need attention")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)