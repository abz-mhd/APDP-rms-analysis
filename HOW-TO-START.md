# 🚀 How to Start RestaurantIQ Analytics System

## 📋 Quick Start Guide

### Method 1: Double-Click Batch File (Easiest)
1. Navigate to the `RMS-analytics-system-main` folder
2. **Double-click** `START-SYSTEM.bat`
3. Wait for the server to start
4. Open browser to http://localhost:5002

### Method 2: Command Prompt / Terminal
1. Open **Command Prompt** or **PowerShell**
2. Navigate to the project folder:
   ```cmd
   cd C:\Users\Mohammed Abzin\Desktop\RMS\RMS-analytics-system-main
   ```
3. Run the startup script:
   ```cmd
   START-SYSTEM.bat
   ```
   OR
   ```cmd
   START.bat
   ```

### Method 3: Direct Python Command
1. Open **Command Prompt** or **PowerShell**
2. Navigate to the project folder:
   ```cmd
   cd C:\Users\Mohammed Abzin\Desktop\RMS\RMS-analytics-system-main
   ```
3. Run Python directly:
   ```cmd
   python frontend/app_fixed.py
   ```

### Method 4: PowerShell
1. Open **PowerShell**
2. Navigate to the project folder:
   ```powershell
   cd "C:\Users\Mohammed Abzin\Desktop\RMS\RMS-analytics-system-main"
   ```
3. Run the server:
   ```powershell
   python frontend/app_fixed.py
   ```

---

## 🌐 Access URLs

Once the server starts, you can access:

### Main Pages:
- **Dashboard:** http://localhost:5002/
- **Reports:** http://localhost:5002/reports
- **Test Page:** http://localhost:5002/test

### Analytics Modules:
- **Peak Dining:** http://localhost:5002/analysis/peak-dining
- **Customer Demographics:** http://localhost:5002/analysis/customer-demographics
- **Seasonal Behavior:** http://localhost:5002/analysis/seasonal-behavior
- **Menu Analysis:** http://localhost:5002/analysis/menu-analysis
- **Revenue Analysis:** http://localhost:5002/analysis/revenue-analysis
- **Branch Performance:** http://localhost:5002/analysis/branch-performance
- **Anomaly Detection:** http://localhost:5002/analysis/anomaly-detection

### API Endpoints:
- **Health Check:** http://localhost:5002/api/health
- **Outlets:** http://localhost:5002/api/outlets
- **Analytics:** http://localhost:5002/api/analytics/peak-dining

---

## 🛑 How to Stop the Server

### In Command Prompt/PowerShell:
- Press **CTRL + C**
- Type `Y` if prompted
- Press **Enter**

### If Server Won't Stop:
1. Open **Task Manager** (Ctrl + Shift + Esc)
2. Find **Python** process
3. Right-click → **End Task**

---

## ⚠️ Troubleshooting

### Problem: "Port 5002 is already in use"
**Solution:**
```cmd
# Find process using port 5002
netstat -ano | findstr :5002

# Kill the process (replace PID with actual process ID)
taskkill /PID <PID> /F
```

### Problem: "Python is not recognized"
**Solution:**
- Make sure Python is installed
- Add Python to PATH environment variable
- Or use full path: `C:\Python\python.exe frontend/app_fixed.py`

### Problem: "Module not found"
**Solution:**
```cmd
# Install required packages
pip install flask pandas plotly numpy
```

### Problem: "CSV file not found"
**Solution:**
- Make sure `restaurant_dataset_with_4th_outlet.csv` exists in the main folder
- Check the file path in `frontend/data_processor.py`

---

## 📊 System Information

### Data:
- **Records:** 8,458 orders
- **Outlets:** 4 restaurants
- **Date Range:** Full year data
- **Customers:** 100 unique customers

### Outlets:
1. **Ocean View - Galle** (80 seats)
2. **City Square - Colombo** (120 seats)
3. **Hillside - Kandy** (60 seats)
4. **Seaside - Negombo** (100 seats)

### Features:
- ✅ 7 Analytics Modules
- ✅ 5 Interactive Heatmaps
- ✅ 8 Filter Options
- ✅ Real-time Data Processing
- ✅ Modern Gradient UI
- ✅ SOLID Principles Architecture
- ✅ Design Patterns Implementation

---

## 🎯 First Time Setup

### 1. Install Python (if not installed)
- Download from: https://www.python.org/downloads/
- Make sure to check "Add Python to PATH"

### 2. Install Required Packages
```cmd
pip install flask pandas plotly numpy
```

### 3. Verify Installation
```cmd
python --version
pip list
```

### 4. Start the System
```cmd
START-SYSTEM.bat
```

---

## 📝 Available Batch Files

| File | Description |
|------|-------------|
| `START.bat` | Simple startup script |
| `START-SYSTEM.bat` | Detailed startup with info |
| `START-COMPLETE-SYSTEM.bat` | Legacy startup script |
| `START-ULTRA-BEAUTIFUL-SYSTEM.bat` | Alternative startup |
| `START-BEAUTIFUL-DASHBOARD.bat` | Dashboard-focused startup |

**Recommended:** Use `START-SYSTEM.bat` for best experience

---

## 💡 Tips

1. **Keep terminal open** while using the system
2. **Don't close the browser** - just minimize it
3. **Use Chrome or Firefox** for best experience
4. **Clear browser cache** if you see old data
5. **Check terminal** for error messages

---

## 🆘 Need Help?

### Check Logs:
- Terminal output shows all server activity
- Look for error messages in red
- Check `frontend/app_fixed.py` for configuration

### Common Issues:
- **Slow loading?** → Wait for data to load (8,458 records)
- **Charts not showing?** → Check browser console (F12)
- **Filters not working?** → Refresh the page
- **Data looks wrong?** → Verify CSV file is correct

---

## ✅ Success Indicators

You'll know the system is running when you see:
```
🚀 Starting RestaurantIQ Analytics System...
📊 Data loaded: 8,458 records
🌐 Server will be available at: http://localhost:5002
 * Running on http://127.0.0.1:5002
 * Debugger is active!
```

---

**Created for RestaurantIQ Analytics System**
*Professional Restaurant Analytics Platform*
