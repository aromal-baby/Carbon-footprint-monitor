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

# Example: Calculate carbon footprint
from app.models.carbon_calculator import CarbonCalculator

calculator = CarbonCalculator()
user_data = {
    'transportation': {'car': {'weekly_km': 100, 'fuel_type': 'petrol'}},
    'energy': {'electricity': {'monthly_kwh': 300, 'renewable_percentage': 20}}
}

results = calculator.calculate_footprint(user_data)
print(f"Total footprint: {results['total']:.2f} kg CO2e")

## Testing

```bash
  python -m pytest tests/
