"""
Carbon Footprint Monitor - Report Service
Generates reports and visualizations
"""

import os
import matplotlib
matplotlib.use('Agg')   # USe non-interactive backend
import matplotlib.pyplot as plt
import numpy as np
import datetime
import base64
from io import BytesIO

class ReportService:
    """Service for generating reports and visualizations"""

    def __init__(self):
        """Initialize the report service"""
        self.static_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'static')
        self.chart_dir = os.path.join(self.static_dir, 'charts')

        # Create charts directory if it doesn't exist
        if not os.path.exists(self.chart_dir):
            os.makedirs(self.chart_dir)

    def generate_charts(self, footprint_data):
        """Generates charts for the carbon footprint report"""
        charts = {}

        # Generate category breakdown chart
        charts['category_breakdown'] = self.generate_category_breakdown_chart(footprint_data)

        # Generate comparison chart if per capita data available
        if 'per_capita' in footprint_data:
            charts['comparison'] = self.generate_comparison_chart(footprint_data)

        return charts

    def generate_category_breakdown_chart(self, footprint_data):
        """Generates pie chart category breakdown"""
        categories = footprint_data.get('categories', {})
        if not categories:
            return None

        # Preparing data
        labels = []
        sizes = []

        for category, data in categories.items():
            if data.get('total', 0) > 0:  # Including only categories with emissions
                labels.append(category.capitalize())
                sizes.append(data.get('total', 0))


        if not sizes:   # No data to display
            return None

        # Create pie chart
        plt.figure(figsize = (8, 6))
        plt.pie(sizes, labels = labels, autopct='%1.1f%%', startangle=90)
        plt.axis('equal')   # Equal aspect ratio ensures that pie is drawn as a circle
        plt.title('Carbon Footprint by Category')

        # Saving to BytesIO
        img = BytesIO()
        plt.savefig(img, format='png', bbox_inches='tight')
        plt.close()
        img.seek(0)

        # Converting to base64 for embedding in HTML
        img_base64 = base64.b64encode(img.getvalue()).decode('utf-8')
        return f"data:image/png;base64,{img_base64}"

    def generate_comparison_chart(self, footprint_data):
        """Generates chart comparing user's footprint to benchmarks"""
        per_capita = footprint_data.get('per_capita', 0)

        # Benchmark data (example values)
        benchmarks = {
            'Your Footprint': per_capita,
            'Global Average': 5000,
            'EU Average': 8500,
            'US Average': 16000,
            'Sustainable Level': 2000
        }

        # Create bar chart
        plt.figure(figsize = (8, 5))
        bars = plt.bar(benchmarks.keys(), benchmarks.values())

        # Color code the bars
        colors = ['green', 'blue', 'blue', 'blue', 'green']
        for i, bar in enumerate(bars):
            bar.set_color(colors[i])

        plt.title('Carbon Footprint Comparison')
        plt.ylabel('kg CO2e per person per year')
        plt.axhline(y=benchmarks['Sustainable Level'], color='r', linestyle='-', alpha=0.3)

        # Rotate x-axis labels for better readability
        plt.xticks(rotation=45, ha='right')

        # Add value labels
        for bar in bars:
            height = bar.get_height()
            plt.text(bar.get_x() + bar.get_width() / 2., height + 100,
                     f'{height:.0f}',
                     ha='center', va='bottom')

            plt.tight_layout()

            # Save to BytesIO
            img = BytesIO()
            plt.savefig(img, format='png', bbox_inches='tight')
            plt.close()
            img.seek(0)

            # Convert to base64 for embedding in HTML
            img_base64 = base64.b64encode(img.getvalue()).decode('utf-8')
            return f"data:image/png;base64,{img_base64}"