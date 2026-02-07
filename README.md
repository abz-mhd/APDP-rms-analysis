# Uber Eats Restaurant Analytics System

A comprehensive restaurant analytics platform built with Java Spring Boot backend and Python Flask frontend, featuring advanced data processing, interactive visualizations, and detailed reporting capabilities.

## 🚀 Quick Start Options

### Option 1: Immediate Demo (Python-only with Mock Data)
Perfect for quickly exploring the interface with sample data:
```bash
setup-python-only.bat
start-frontend-only.bat
```
Then open http://localhost:5000

### Option 2: Full System (Complete Analytics Platform)
For full functionality with real data processing:
```bash
setup.bat
run-system.bat
```
Then open http://localhost:5000

## 📋 Prerequisites & Installation

### System Requirements
- **Operating System**: Windows 10/11
- **RAM**: Minimum 4GB, Recommended 8GB+
- **Storage**: 2GB free space
- **Ports**: 8080 (backend), 5000 (frontend)

### Required Software

#### 1. Java 17 or Higher
- **Download**: https://adoptium.net/
- **Installation**: 
  - Download the Windows x64 MSI installer
  - Run installer and ensure "Add to PATH" is checked
- **Verify**: `java -version`

#### 2. Apache Maven 3.6+
- **Download**: https://maven.apache.org/download.cgi
- **Installation**:
  - Download Binary zip archive (apache-maven-3.x.x-bin.zip)
  - Extract to `C:\Program Files\Apache\maven`
  - Add `C:\Program Files\Apache\maven\bin` to system PATH
- **Verify**: `mvn -version`

#### 3. Python 3.8+
- **Download**: https://www.python.org/downloads/
- **Installation**:
  - Download Windows installer
  - **IMPORTANT**: Check "Add Python to PATH" during installation
- **Verify**: `python --version`

### Manual Setup (Alternative)
If automated scripts don't work:

1. **Install Python Dependencies**
   ```bash
   cd frontend
   pip install -r requirements.txt
   cd ..
   ```

2. **Compile Java Backend**
   ```bash
   cd backend
   mvn compile
   cd ..
   ```

3. **Start Backend** (in one terminal)
   ```bash
   cd backend
   mvn spring-boot:run
   ```

4. **Start Frontend** (in another terminal)
   ```bash
   cd frontend
   python app.py
   ```

## 🏗️ System Architecture

### Backend (Java Spring Boot)
- **Modular Pipeline**: Ingestion → Transformation → Analytics → API
- **Source-Agnostic Ingestion**: CSV, JSON, Database, APIs
- **Chunk-Based Processing**: Handles large files (5GB+)
- **Error Handling**: Dead-letter queue for failed operations
- **REST APIs**: JSON endpoints for analytics results

### Frontend (Python Flask)
- **Web GUI**: Interactive management dashboard
- **Visualizations**: Plotly/Seaborn/Matplotlib charts
- **Report Export**: CSV, PDF formats
- **Filtering**: Branch selector, time filters, seasonal analysis

## 📊 Analytics Modules

### 1. Peak Dining Analysis
- **Heatmaps**: Order volume by hour and outlet
- **Peak Hour Tables**: Top performing time slots
- **Branch Summaries**: Performance metrics per location
- **Daily/Weekly Patterns**: Temporal analysis

### 2. Customer Demographics & Segmentation
- **Age Distribution**: Customer age group analysis
- **Gender Analysis**: Gender-based patterns
- **Loyalty Groups**: Customer segmentation by loyalty
- **Spending Patterns**: Behavioral analysis
- **RFM Analysis**: Recency, Frequency, Monetary segmentation

### 3. Customer Seasonal Behavior
- **Seasonal Retention**: Customer retention across seasons
- **Loyalty Index**: Customer loyalty scoring
- **Seasonal Spending**: Spending patterns by season
- **Customer Lifecycle**: Lifespan analysis

### 4. Popular Menu & Order Flow Analysis
- **Top Items**: Most popular menu items
- **Category Analysis**: Performance by food category
- **Item Combos**: Frequently ordered combinations
- **Sankey Diagrams**: Order flow visualization
- **Spice Level Preferences**: Customer taste preferences
- **Vegetarian Analysis**: Dietary preference insights

### 5. Ticket Counting & Revenue Analysis
- **Revenue Summary**: Total revenue and growth metrics
- **Daily/Monthly Revenue**: Time-based revenue trends
- **Average Order Value**: AOV analysis by various dimensions
- **Payment Method Analysis**: Payment preference insights
- **Outlet Revenue Comparison**: Branch performance comparison

### 6. Service Anomaly Detection
- **Preparation Time Anomalies**: Unusual cooking times
- **Order Volume Anomalies**: Unexpected order patterns
- **Revenue Anomalies**: Unusual revenue patterns
- **Customer Behavior Anomalies**: Unusual spending patterns
- **Alert Logs**: Automated alert system

### 7. Branch Performance Analysis
- **Branch Dashboards**: Comprehensive branch metrics
- **Branch Rankings**: Performance-based rankings
- **Efficiency Analysis**: Operational efficiency metrics
- **Customer Satisfaction**: Satisfaction indicators

## 🎯 Key Features

### Interactive Dashboard
- **Real-time Analytics**: Live data analysis and visualization
- **Filtering System**: Multi-dimensional filtering (outlet, season, festival)
- **Responsive Design**: Works on desktop, tablet, and mobile
- **Interactive Charts**: Plotly-powered interactive visualizations

### Advanced Analytics
- **Statistical Analysis**: Z-score based anomaly detection
- **Time Series Analysis**: Temporal pattern recognition
- **Customer Segmentation**: RFM analysis and loyalty scoring
- **Performance Metrics**: KPI tracking and benchmarking

### Export Capabilities
- **CSV Export**: Raw data for further analysis
- **PDF Reports**: Formatted reports with charts and tables
- **Customizable Filters**: Export specific data subsets

### Seasonal & Festival Filtering
- **Seasons**: Spring, Summer, Autumn, Winter
- **Festivals**: Christmas, New Year, Valentine's Day, Easter, Diwali, Vesak
- **Custom Periods**: Flexible date range filtering

## 🔧 Installation & Setup

See [INSTALLATION_GUIDE.md](INSTALLATION_GUIDE.md) for detailed setup instructions.

## 📁 Project Structure
```
uber-eats-restaurant-analytics/
├── backend/                    # Java Spring Boot Backend
│   ├── src/main/java/com/restaurant/analytics/
│   │   ├── ingestion/         # Data ingestion module
│   │   ├── transform/         # Data transformation
│   │   ├── analytics/         # Analytics engines
│   │   ├── api/              # REST API controllers
│   │   └── model/            # Data models
│   ├── pom.xml               # Maven configuration
│   └── restaurant_dataset_combined.csv
├── frontend/                   # Python Flask Frontend
│   ├── app.py                 # Main Flask application
│   ├── app-mock.py           # Mock data version (for demo)
│   ├── routes/
│   │   ├── dashboard.py       # Dashboard routes
│   │   ├── reports.py         # Report generation
│   │   └── charts.py          # Chart endpoints
│   ├── templates/             # HTML templates (minimal design)
│   │   ├── base.html         # Base template with right sidebar
│   │   ├── index.html        # Dashboard with blue/gray theme
│   │   ├── analysis.html     # Analytics modules
│   │   ├── reports.html      # Report generation
│   │   └── dashboard_overview.html
│   └── requirements.txt       # Python dependencies
├── setup.bat                  # Full system setup script
├── setup-python-only.bat     # Python-only setup script
├── run-system.bat            # Start full system
├── start-backend.bat         # Start backend only
├── start-frontend.bat        # Start frontend (requires backend)
├── start-frontend-only.bat   # Start frontend with mock data
├── restaurant_dataset_combined.csv  # Sample dataset
└── README.md                 # This comprehensive guide
```

## 🎨 Design Features

### Modern Minimal Interface
- **Color Scheme**: Simple blue (#4a90e2), light gray (#6c757d), and white
- **Layout**: Clean design with right-positioned sidebar
- **Navigation**: Intuitive menu structure for easy access
- **Responsive**: Works on desktop, tablet, and mobile devices

### Interactive Dashboard
- **Real-time Analytics**: Live data analysis and visualization
- **Filtering System**: Multi-dimensional filtering (outlet, season, festival)
- **Interactive Charts**: Plotly-powered visualizations with minimal color palette
- **Export Options**: CSV and PDF report generation

## 🌐 API Endpoints

### Analytics Endpoints
- `GET /api/analytics/peak-dining` - Peak dining analysis
- `GET /api/analytics/customer-demographics` - Customer demographics
- `GET /api/analytics/customer-seasonal` - Seasonal behavior
- `GET /api/analytics/menu-analysis` - Menu analysis
- `GET /api/analytics/revenue-analysis` - Revenue analysis
- `GET /api/analytics/anomaly-detection` - Anomaly detection
- `GET /api/analytics/branch-performance` - Branch performance
- `GET /api/analytics/outlets` - List of outlets

### Query Parameters
- `outletId` - Filter by specific outlet
- `season` - Filter by season (spring, summer, autumn, winter)
- `festival` - Filter by festival period

### Export Endpoints
- `GET /reports/export/csv/{analysis_type}` - Export as CSV
- `GET /reports/export/pdf/{analysis_type}` - Export as PDF

## 🚨 Troubleshooting

### Common Issues

#### "Java is not recognized"
- **Problem**: Java not installed or not in PATH
- **Solution**: Install Java 17+ from https://adoptium.net/ and ensure PATH is set

#### "mvn is not recognized"
- **Problem**: Maven not installed or not in PATH
- **Solution**: Install Maven and add to PATH (see installation guide above)

#### "python is not recognized"
- **Problem**: Python not installed or not in PATH
- **Solution**: Install Python and check "Add to PATH", or use `py` command

#### Backend won't start
- Check Java version: `java -version` (should be 17+)
- Check Maven: `mvn -version`
- Ensure port 8080 is available
- Review console error messages

#### Frontend connection errors
- Ensure backend is running first at http://localhost:8080
- Verify Python dependencies are installed
- Check port 5000 is available

#### Data loading issues
- Ensure `restaurant_dataset_combined.csv` is in backend directory
- Check file permissions
- Review backend console for error messages

### Feature Comparison

#### Full Installation Features
- ✅ All 7 analytics modules
- ✅ Real-time data processing
- ✅ Interactive charts and visualizations
- ✅ CSV/PDF export functionality
- ✅ Advanced filtering (season, festival, outlet)
- ✅ Anomaly detection
- ✅ Large file processing (5GB+)

#### Python-only (Mock Data) Features
- ✅ User interface demonstration
- ✅ Basic chart examples
- ❌ Real data processing
- ❌ Export functionality
- ❌ Advanced analytics

## 🔮 Future Enhancements

- Real-time data streaming integration
- Machine learning prediction models
- Advanced forecasting capabilities
- Multi-tenant restaurant support
- Role-based access control system
- Mobile application development
- Advanced dashboard customization
- API rate limiting and security enhancements

## 📄 License & Usage

This Uber Eats Restaurant Analytics System is designed for educational and commercial use in restaurant analytics and business intelligence applications.

## 🏗️ System Architecture

```
CSV Data → Java Backend (Spring Boot) → REST APIs → Python Frontend (Flask) → Web Dashboard
```

The system follows a modular architecture with clear separation of concerns:
- **Data Layer**: CSV file processing and storage
- **Processing Layer**: Java Spring Boot for heavy analytics computations
- **API Layer**: RESTful services for data exchange
- **Presentation Layer**: Python Flask web application with minimal design
- **User Interface**: Clean, responsive web dashboard with blue/gray color scheme

---

**Note**: This system includes both a full-featured version (requires Java/Maven) and a demo version (Python-only with mock data) to accommodate different setup and demonstration requirements.