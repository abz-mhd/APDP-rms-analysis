#!/usr/bin/env python3
"""Test script to diagnose import issues"""

import sys
import os

print("Current working directory:", os.getcwd())
print("Python path:", sys.path)
print()

# Test basic imports
try:
    import pandas as pd
    print("✓ pandas imported successfully")
except ImportError as e:
    print("✗ pandas import failed:", e)

try:
    import plotly.graph_objs as go
    print("✓ plotly imported successfully")
except ImportError as e:
    print("✗ plotly import failed:", e)

try:
    from flask import Flask
    print("✓ Flask imported successfully")
except ImportError as e:
    print("✗ Flask import failed:", e)

# Test data processor
try:
    from data_processor import data_processor
    print(f"✓ data_processor imported successfully - {len(data_processor.df)} records")
except ImportError as e:
    print("✗ data_processor import failed:", e)
except Exception as e:
    print("✗ data_processor error:", e)

# Test routes
print("\nTesting route imports:")
try:
    from routes.charts import charts_bp
    print("✓ charts blueprint imported successfully")
except ImportError as e:
    print("✗ charts blueprint import failed:", e)
except Exception as e:
    print("✗ charts blueprint error:", e)

try:
    from routes.dashboard import dashboard_bp
    print("✓ dashboard blueprint imported successfully")
except ImportError as e:
    print("✗ dashboard blueprint import failed:", e)

try:
    from routes.reports import reports_bp
    print("✓ reports blueprint imported successfully")
except ImportError as e:
    print("✗ reports blueprint import failed:", e)

# Test app creation
print("\nTesting app creation:")
try:
    from app import app
    print("✓ Flask app created successfully")
    print("Routes available:")
    for rule in app.url_map.iter_rules():
        print(f"  {rule.rule} -> {rule.endpoint}")
except ImportError as e:
    print("✗ Flask app import failed:", e)
except Exception as e:
    print("✗ Flask app error:", e)