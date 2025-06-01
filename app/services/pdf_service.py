"""
EcoTrack: Carbon Footprint Monitor - PDF Service
Generates downloadable PDF reports
"""

import os
import datetime
from io import BytesIO
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch

class PDFService:
    """Service for generating PDF reports"""

    def __init__(self):
        """Initialize PDF service"""
        self.static_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'static')

    def generate_report_pdf(self, user_data, footprint_data, charts=None):
        """Generate PDF report for the footprint data"""
        # To create a file-like buffer to receive PDF data
        buffer = BytesIO()

        # Creating the PDF object using the buffer as its "file"
        doc = SimpleDocTemplate(buffer, pagesize=A4)

        # Getting styles
        styles = getSampleStyleSheet()
        title_style = styles['Title']
        heading_style = styles['Heading2']
        normal_style = styles['Normal']

        # Create custom styles
        section_style = ParagraphStyle(
            'SectionTitle',
            parent=styles['Heading2'],
            spaceAfter=12,
            spaceBefore=6,
            textColor=colors.darkblue
        )

        # Container for the 'Flowable' objects (paragraphs, tables, etc.)
        elements = []

        # Title
        elements.append(Paragraph("Carbon Footprint Assessment Report", title_style))
        elements.append(Spacer(1, 0.25*inch))

        # Adding report date
        report_date = datetime.datetime.now().strftime("%Y-%m-%d")
        elements.append(Paragraph(f"Report Date: {report_date}", normal_style))
        elements.append(Spacer(1, 0.25*inch))

        # Adding client information
        elements.append(Paragraph("Client Information", section_style))

        client_info = []
        if user_data.get('user_type') == 'Organization':
            client_info.append(["Organization", user_data.get('org_name', 'N/A')])
            client_info.append(["Contact Person", user_data.get('contact_person', 'N/A')])
            client_info.append(["Industry", user_data.get('industry', 'N/A')])
            client_info.append(["Number of Employees", str(user_data.get('employees', 'N/A'))])
        else:
            client_info.append(["Individual", user_data.get('name', 'N/A')])
            client_info.append(["Household Size", str(user_data.get('household_size', 'N/A'))])


        # Creating client info table
        client_table = Table(client_info, colWidths=[2*inch, 3.5*inch])
        client_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('LEFTPADDING', (0, 0), (-1, -1), 6),
            ('RIGHTPADDING', (0, 0), (-1, -1), 6),
        ]))

        elements.append(client_table)
        elements.append(Spacer(1, 0.25*inch))

        # Summary section
        elements.append(Paragraph("Carbon Footprint Summary", section_style))

        # Total footprint
        elements.append(Paragraph(f"Total Annual Carbon Footprint: {footprint_data.get('total', 0):.2f} kg CO2e", normal_style))

        # Per capita footprint if available
        if 'per_capita' in footprint_data:
            elements.append(Paragraph(f"Per Capita Annual Carbon Footprint: {footprint_data.get('per_capita', 0):.2f} kg CO2e", normal_style))

        # Global context
        global_average = 5000       # Example value
        sustainable_level = 2000    # Example value

        elements.append(Paragraph(f"Global Average: {global_average} kg CO2e per person per year", normal_style))
        elements.append(Paragraph(f"Sustainable Level: {sustainable_level} kg CO2e per person per year", normal_style))

        # Adding sustainability message
        comparison_value = footprint_data.get('per_capita', footprint_data.get('total', 0))
        if comparison_value < sustainable_level:
            elements.append(Paragraph("Your carbon footprint is below the sustainable level. Great job!", normal_style))
        elif comparison_value < global_average:
            elements.append(Paragraph("Your carbon footprint is below the global average but above the sustainable level.", normal_style))
        else:
            elements.append(Paragraph("Your carbon footprint is above the global average.", normal_style))

        elements.append(Spacer(1, 0.25*inch))


        """# Adding charts if available
        if charts and 'category_breakdown' in charts:
            # Add charts if provided
            if isinstance(charts['category_breakdown'], str) and charts['category_breakdown'].startswith('data:image/png;base64,'):
                # Extract base64 image data
                import base64
                img_data = charts['category_breakdown'].split(',')[1]
                img_bytes = base64.b64decode(img_data)

                # Saving temp image
                temp_img_path = os.path.join(self.static_dir, 'temp_chart.png')
                with open(temp_img_path, 'wb') as f:
                    f.write(img_bytes)


                # Add image to PDF
                img = Image(temp_img_path, width=5*inch, height=3*inch)
                elements.append(img)
                elements.append(Spacer(1, 0.25*inch))

                # Clean up temp file
                try:
                    os.remove(temp_img_path)
                except:
                    pass """


        # Break down by category
        elements.append(Paragraph("Breakdown by Category", normal_style))

        categories = footprint_data.get('categories', {})
        if categories:
            # Prepare data for category
            category_data = [["Category", "Emissions (kg CO2e)", "Percentage"]]

            for category, data in categories.items():
                if isinstance(data, dict) and 'total' in data:
                    category_total = data.get('total', 0)
                    percentage = (category_total / footprint_data.get('total', 1)) * 100
                    category_data.append([
                        category.capitalize(),
                        f"{category_total:.2f}",
                        f"{percentage:.1f}"
                    ])

            # Creating category table
            category_table = Table(category_data, colWidths=[2*inch, 2*inch, 1.5*inch])
            category_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
                ('LEFTPADDING', (0, 0), (-1, -1), 6),
                ('RIGHTPADDING', (0, 0), (-1, -1), 6),
            ]))

            elements.append(category_table)
            elements.append(Spacer(1, 0.25*inch))

            # Detailed breakdown for each category
            elements.append(Paragraph("Detailed Breakdown", section_style))

            for category, data in categories.items():
                if isinstance(data, dict) and 'breakdown' in data:
                    elements.append(Paragraph(f"{category.capitalize()} Details:", heading_style))

                    # Prepare data for breakdown table
                    breakdown_data = [["Item", "Emissions (kg CO2e)"]]

                    for item, value in data.get('breakdown', {}).items():
                        # Handle nested dictionaries
                        if isinstance(value, dict):
                            for subitem, subValue in value.items():
                                breakdown_data.append([
                                    f"{item.replace('_', ' ').capitalize()} - {subitem.replace('_', ' ').capitalize()}",
                                    f"{subValue:.2f}"
                                ])
                        else:
                            breakdown_data.append([
                                f"{item.replace('_', ' ').capitalize()}",
                                f"{value:.2f}"
                            ])

                    # Creating breakdown table
                    breakdown_table = Table(breakdown_data, colWidths=[4*inch, 1.5*inch])
                    breakdown_table.setStyle(TableStyle([
                        ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
                        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
                        ('LEFTPADDING', (0, 0), (-1, -1), 6),
                        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
                    ]))

                    elements.append(breakdown_table)
                    elements.append(Spacer(1, 0.25*inch))

        # Recommendations section
        elements.append(Paragraph("Recommendations", section_style))

        # Add generic recommendations based on the footprint data
        recommendations = self.generate_recommendations(footprint_data)

        for i, recommendation in enumerate(recommendations, 1):
            elements.append(Paragraph(f"{i}. {recommendation}", normal_style))
            elements.append(Spacer(1, 0.1*inch))

        elements.append(Spacer(1, 0.25*inch))

        # Footer
        elements.append(Paragraph("This report was generated by EcoTrack Carbon Footprint Monitor.", normal_style))
        elements.append(Paragraph("For more information, visit eco-track.example.com", normal_style))

        # Building the PDF
        doc.build(elements)

        # Getting the value of the BytesIO buffer
        pdf = buffer.getvalue()
        buffer.close()

        return pdf

    # Method for generating recommendations
    def generate_recommendations(self, footprint_data):
        """Generate recommendations based on footprint data"""
        recommendations = []

        # Finding the category with the highest emissions
        categories = footprint_data.get('categories', {})
        if not categories:
            return ["Track your carbon footprint regularly to monitor your progress."]

        # Finding the highest category
        highest_category = max(categories.items(), key=lambda x: x[1].get('total', 0) if isinstance(x[1], dict) else 0)
        highest_category_name = highest_category[0]

        # General recommendations
        recommendations.append("Track your carbon footprint regularly to monitor your progress.")
        recommendations.append("Consider carbon offsetting for emissions you cannot eliminate.")

        # Category-specific recommendations
        if highest_category_name == 'transportation':
            recommendations.append("Consider using public transportation instead of a car for regular commutes.")
            recommendations.append("Reduce the number of flights and consider video conferencing for business meetings.")
            recommendations.append("If possible, switch to an electric or hybrid vehicle for your next car purchase.")

        elif highest_category_name == 'energy':
            recommendations.append("Switch to a renewable energy provider to reduce your electricity emissions.")
            recommendations.append("Invest in energy-efficient appliances and LED lighting.")
            recommendations.append("Improve home insulation to reduce heating needs.")

        elif highest_category_name == 'waste':
            recommendations.append("Adopt zero-waste principles to reduce your general waste.")
            recommendations.append("Start composting organic waste if you don't already.")
            recommendations.append("Increase recycling efforts for paper, plastic, glass, and metal.")

        elif highest_category_name == 'food':
            recommendations.append("Reduce red meat consumption to significantly lower your food emissions.")
            recommendations.append("Choose locally produced food to reduce transportation emissions.")
            recommendations.append("Consider adopting a more plant-based diet for substantial emission reductions.")

        elif highest_category_name == 'products':
            recommendations.append("Buy more secondhand items to reduce emissions from manufacturing.")
            recommendations.append("Reduce overall consumption by prioritizing essential purchases.")
            recommendations.append("Extend the life of your products through repair and maintenance.")

        return recommendations

