# Carbon-footprint-monitor

A versatile Python application designed to help both organizations and individuals track, analyze, and reduce their carbon footprint. This user-friendly tool enables the collection of environmental impact data, generates insightful reports with personalized reduction strategies, and identifies emission patterns over time.

## Project Overview

The carbon footprint monitor helps users calculate their carbon emissions across multiple categories: transportation, food, waste, energy, and products. Also, provides personalized recommendations based on their emissions which helps them reduce accordingly. The application features real-time global benchmarking via "Our World in Data API", and comprehensive PDF reporting.

## Features

- **Trend Analysis**: Track progress across multiple assessments
- **Multi-Category Analysis**: Transportation, energy, waste, food, and product emissions
- **Dynamic Currency Support**: Automatic currency selection based on user's country
- **Responsive Design**: Professional UI with glassmorphism effects
- **Error Handling**: Robust input validation and error management
- **Visual Reports**: Interactive charts and downloadable PDF reports
- **Global Benchmarking**: Real-time comparisons with country and global averages

## Architecture
```
Carbon Footprint Monitor/
├── app/
│   ├── init.py              # Flask application initialization
│   ├── routes.py                # URL routing and view functions
│   ├── models/
│   │   ├── carbon_calculator.py # Carbon footprint calculations
│   │   └── emission_factors.py  # Emission factors and constants
│   ├── services/
│   │   ├── benchmark_service.py # Our World in Data API integration
│   │   ├── currency_service.py  # Currency management
│   │   ├── data_service.py      # Data storage and retrieval
│   │   ├── pdf_service.py       # PDF report generation
│   │   └── report_service.py    # Chart and visualization generation
│   ├── static/
│   │   ├── css/style.css        # Application styling
│   │   └── assets/              # Images and visual assets
│   └── templates/               # Jinja2 HTML templates
├── reports/                     # Generated carbon footprint reports
├── cache/                       # API data caching
├── tests/                       # Unit tests
├── requirements.txt             # Project dependencies
└── run.py                       # Application entry point
````

## Installation

### Prerequisites
- Python 3.13+
- pip package manager

### Setup Instructions

1. **Clone the repository:**
   ```bash
   git clone https://github.com/aromal-baby/Carbon-footprint-monitor.git
   cd "Carbon Footprint Monitor"

   pip install -r requirements.txt

   python run.py

### To access

Open your browser and navigate to http://127.0.0.1:5000


## Usage 

### For Individual Users

1. Select "Individual" in the data entry form
2. Choose your country for accurate benchmarking
3. Complete the assessment across all categories
4. Review your results with global comparisons
5. Download your personalized PDF report


### For Organizations

1. Select "Organization" in the data entry form
2. Provide company details and employee count
3. Input organizational data across categories
4. Analyze per-capita emissions and trends
5. Generate comprehensive organizational reports


## Technical Impolementation

### Carbon Footprint Calculation

The application uses scientifically-backed emission factors:
- **Transportation**: Based on fuel type and distance by air/land, also based on personilized
mode of transports.
- **Energy**: Considers renewable energy percentage.
- **Waste**: Accounts for recycling znd composting.
- **Food**: Diet-specific calculations with local food benefits.
- **Products**: Spendings with secondhand benefits (currency-adjusted)

### API Integration

- **Our World in Data API**: Real-time carbon emissions benchmarking.
- **Fallback System**: Ensures reliability when API is not available.
- **Caching**: 30-day caching for improved performance.

### Key Technologies

- **Backend**: Python Flask.
- **Data Processing**: NumPy for calculations
- **Visualization**: Matplotlib for charts
- **PDF Generation**: ReportLab for professional reports
- **Frontend**: HTML5, CSS3, JavaScript (ES6)
- **Styling**: Custom CSS with glassmorphism effects


## Example Usage

```python

   # Example: Calculate carbon footprint
   from app.models.carbon_calculator import CarbonCalculator
   
   calculator = CarbonCalculator()
   user_data = {
       'transportation': {'car': {'weekly_km': 100, 'fuel_type': 'petrol'}},
       'energy': {'electricity': {'monthly_kwh': 300, 'renewable_percentage': 20}}
   }
   
   results = calculator.calculate_footprint(user_data)
   print(f"Total footprint: {results['total']:.2f} kg CO2e")

```
## Testing

```bash
   python -m pytest tests/
```

## Generated Reports

The application generates:

- **PDF Reports**: Comprehensive analysis with charts and recommendations
- **JSON Data**: Structured data for trend analysis
- **Visual Charts**: Category breakdowns and benchmark comparisons


## Global Benchmarking

EcoTrack provides real-time comparisons with:

- Country-specific averages
- Global emission averages
- Paris Agreement sustainability targets (2.0 tonnes CO2 per person)


## Future Enhancements

- Real-time carbon tracking integration
- Mobile application development
- Enhanced recommendation algorithms
- Corporate sustainability dashboard
- Carbon offset marketplace integration

## Academic Context

This project was developed as part of the M602 Computer Programming course at Gisma University of Applied Sciences, demonstrating:

- Object-oriented programming principles
- API integration and data processing
- Web application development
- Professional software documentation
- Error handling and user experience design


## Acknowledgments

- **Our World in Data** for providing reliable carbon emissions data
- **Gisma University** for project guidance and support
- **Flask Community** for excellent documentation and resources
- **Environmental Organizations** for emission factor research

## Contact

Aromal Baby

- GitHub: @aromal-baby
- Project Link: https://github.com/aromal-baby/Carbon-footprint-monitor

Built with 💚 for a sustainable future

### 1.2 Create Supporting Documentation Files

#### Create `INSTALL.md`:
```markdown
   # Installation Guide
   
   ## System Requirements
   - Python 3.13 or higher
   - 4GB RAM minimum
   - 500MB free disk space
   - Internet connection for API access
   
   ## Detailed Setup
   
   ### Windows
   1. Download Python from python.org
   2. Open Command Prompt as Administrator
   3. Navigate to project directory
   4. Run installation commands
   
   ### macOS
   1. Install Python via Homebrew: `brew install python`
   2. Follow standard installation steps
   
   ### Linux
   1. Install Python: `sudo apt-get install python3`
   2. Install pip: `sudo apt-get install python3-pip`
   3. Follow standard installation steps
   
   ## Troubleshooting
   - **Port 5000 in use**: Change port in run.py
   - **Permission errors**: Run as administrator
   - **API errors**: Check internet connection### 1.2 Create Supporting Documentation Files
   
   #### Create `INSTALL.md`:
   ```markdown
   # Installation Guide
   
   ## System Requirements
   - Python 3.13 or higher
   - 4GB RAM minimum
   - 500MB free disk space
   - Internet connection for API access
   
   ## Detailed Setup
   
   ### Windows
   1. Download Python from python.org
   2. Open Command Prompt as Administrator
   3. Navigate to project directory
   4. Run installation commands
   
   ### macOS
   1. Install Python via Homebrew: `brew install python`
   2. Follow standard installation steps
   
   ### Linux
   1. Install Python: `sudo apt-get install python3`
   2. Install pip: `sudo apt-get install python3-pip`
   3. Follow standard installation steps
   
   ## Troubleshooting
   - **Port 5000 in use**: Change port in run.py
   - **Permission errors**: Run as administrator
   - **API errors**: Check internet connection
```

## Create ARCHITECTURE.md

```markdown
   # System Architecture
   
   ## Overview
   EcoTrack follows a modular MVC architecture pattern optimized for scalability and maintainability.
   
   ## Component Breakdown
   
   ### Models Layer
   - `carbon_calculator.py`: Core calculation engine
   - `emission_factors.py`: Scientific constants and factors
   
   ### Services Layer
   - `benchmark_service.py`: External API integration
   - `currency_service.py`: Multi-currency support
   - `data_service.py`: Data persistence
   - `pdf_service.py`: Report generation
   - `report_service.py`: Visualization creation
   
   ### View Layer
   - `routes.py`: Request handling and business logic
   - `templates/`: HTML templates with Jinja2
   - `static/`: CSS, JavaScript, and assets
   
   ## Data Flow
   1. User input → Routes → Services → Models
   2. Calculations → Services → Templates → User display
   3. Reports → PDF Service → File download
