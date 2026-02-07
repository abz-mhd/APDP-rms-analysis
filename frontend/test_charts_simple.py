#!/usr/bin/env python3
"""Simple test script to verify charts generation"""

import sys
import os
sys.path.append(os.path.dirname(__file__))

from routes.charts import generate_peak_dining_charts
from data_processor import data_processor

def test_charts():
    print("Testing chart generation...")
    
    # Test data loading
    print(f"Data loaded: {len(data_processor.df)} records")
    
    if data_processor.df.empty:
        print("ERROR: No data loaded!")
        return False
    
    # Test peak dining charts
    try:
        charts = generate_peak_dining_charts()
        print(f"Generated {len(charts)} peak dining charts")
        
        for chart_name in charts.keys():
            print(f"  - {chart_name}")
        
        return len(charts) > 0
        
    except Exception as e:
        print(f"ERROR generating charts: {e}")
        return False

if __name__ == "__main__":
    success = test_charts()
    print(f"\nTest {'PASSED' if success else 'FAILED'}")
    sys.exit(0 if success else 1)