from flask import render_template, request, redirect, url_for, session, flash, jsonify, send_file
from pkg_resources import safe_name

from app import app
from app.models.carbon_calculator import CarbonCalculator
from app.services import pdf_service
from app.services.data_service import DataService
from app.services.report_service import ReportService
from app.services.pdf_service import PDFService
import json
import os
import io
import datetime


calculator = CarbonCalculator()     # Calculator instance
data_service = DataService()        # Data service instance
report_service = ReportService()    # Report service instance
pdf_service =PDFService()           # PDF service instance


@app.route('/')
def index():
    """Home page route"""
    return render_template('home.html', title='Carbon Footprint Monitor')

@app.route('/about')
def about():
    """About page route"""
    return render_template('about.html', title='About')

@app.route('/data-entry', methods=['GET', 'POST'])
def data_entry():
    """Data entry form route"""
    if request.method == 'POST':
        # Process form data
        user_data = {
            'user_type': request.form.get('user_type'),
            'date': datetime.datetime.now().strftime('%Y-%m-%d')
        }


        # To handle organization or individual specific fields
        if user_data['user_type'] == 'Organization':
            user_data['org_name'] = request.form.get('org_name')
            user_data['contact_person'] = request.form.get('contact_person')
            user_data['industry'] = request.form.get('industry')
            user_data['employees'] = int(request.form.get('employees', 1))

        else:
            user_data['name'] = request.form.get('name')
            user_data['household_size'] = int(request.form.get('household_size'))


        # To store basic info in session
        session['user_data'] = user_data

        # Redirect to transportation data entry
        return redirect(url_for('transportation_entry'))

    return render_template('data_entry.html', title='Enter Your Data')


@app.route('/transportation', methods=['GET', 'POST'])
def transportation_entry():
    """Transportation data entry form"""
    if 'user_data' not in session:
        # Redirect to initial data entry section if no data is entered
        redirect(url_for('data_entry'))

    if request.method == 'POST':
        transportation_data = {}

        # Car data
        if request.form.get('has_car') == 'yes':
            transportation_data['car'] = {
                'weekly_km': float(request.form.get('car_weekly_km', 0)),
                'fuel_type': request.form.get('car_fuel_type', 'petrol')
            }

        # Public transportation data
        if request.form.get('has_public_transport') == 'yes':
            transportation_data['public_transport'] = {
                'weekly_km': float(request.form.get('public_transport_weekly_km', 0)),
            }

        # Air travel data
        if request.form.get('has_air_travel') == 'yes':
            transportation_data['air_travel'] = {
                'short_flight': int(request.form.get('short_flights', 0)),
                'long_flight': int(request.form.get('long_flights', 0)),
            }


        # Adding transportation data to session
        user_data = session.get('user_data', {})
        user_data['transportation'] = transportation_data
        session['user_data'] = user_data

        # To energy data entry
        return redirect(url_for('energy_entry'))

    # Redirect to energy data form
    return render_template('transportation.html', title='Transportation Data')


@app.route('/energy', methods=['GET', 'POST'])
def energy_entry ():
    """Energy data entry form"""
    if 'user_data' not in session:
        # Redirect to initial data entry if there is nothing
        return redirect(url_for('data_entry'))

    if request.method == 'POST':
        energy_data = {}

        # Electricity data
        energy_data['electricity'] = {
            'monthly_kwh': float(request.form.get('electricity_monthly_kwh', 0)),
            'renewables_percentage': float(request.form.get('renewables_percentage', 0)),
        }

        # Natural gas data
        if request.form.get('has_gas') == 'yes':
            energy_data['gas'] = {
                'monthly_usage': float(request.form.get('gas_monthly_usage', 0))
            }

        # Adding energy to the session
        user_data = session.get('user_data', {})
        user_data['energy'] = energy_data
        session['user_data'] = user_data

        # For simplicity, we're skipping waste, food, and products forms
        # In a complete implementation, you would continue with those forms

        # Calculate footprint and show results
        return redirect(url_for('waste_entry'))

    return render_template('energy.html', title='Energy Data')


@app.route('/waste', methods=['GET', 'POST'])
def waste_entry():
    """Waste data entry form"""
    if 'user_data' not in session:
        # Redirect to initial data entry if there is nothing
        return redirect(url_for('data_entry'))

    if request.method == 'POST':
        waste_data = {}

        # General waste
        waste_data['general_waste'] = {
            'weekly_kg': float(request.form.get('weekly_kg', 0))
        }

        # Recycling
        waste_data['recycling'] = {
            'paper': float(request.form.get('paper', 0)),
            'plastic': float(request.form.get('plastic', 0)),
            'glass': float(request.form.get('glass', 0)),
            'metal': float(request.form.get('metal', 0))
        }

        # Composting
        waste_data['composting'] = True if request.form.get('composting') == 'yes' else False

        # Add waste data to session
        user_data = session.get('user_data', {})
        user_data['waste'] = waste_data
        session['user_data'] = user_data

        # Redirect to food data entry
        return redirect(url_for('food_entry'))

    return render_template('waste.html', title='Waste Data')


@app.route('/food', methods=['GET', 'POST'])
def food_entry():
    """Food data entry form"""
    if 'user_data' not in session:
        # Redirect to initial data entry if no user data exists
        return redirect(url_for('data_entry'))

    if request.method == 'POST':
        food_data = {}

        # Diet type
        food_data['diet_type'] = request.form.get('diet_type', 'omnivore')

        # Meat consumption
        if food_data['diet_type'] in ['omnivore', 'pescatarian']:
            food_data['meat_consumption'] = {}

            if food_data['diet_type'] == 'omnivore':
                food_data['meat_consumption']['red_meat'] = float(request.form.get('red_meat', 0))
                food_data['meat_consumption']['poultry'] = float(request.form.get('poultry', 0))

            food_data['meat_consumption']['fish'] = float(request.form.get('fish', 0))

        # Local food
        food_data['local_food_percentage'] = float(request.form.get('local_food_percentage', 0))

        # Add food data to session
        user_data = session.get('user_data', {})
        user_data['food'] = food_data
        session['user_data'] = user_data

        # Redirect to products data entry
        return redirect(url_for('products_entry'))

    return render_template('food.html', title='Food Data')


@app.route('/products', methods=['GET', 'POST'])
def products_entry():
    """Products data entry form"""
    if 'user_data' not in session:
        # Redirect to initial data entry if no user data exists
        return redirect(url_for('data_entry'))

    if request.method == 'POST':
        products_data = {}

        # Monthly spending
        products_data['monthly_spending'] = {
            'clothing': float(request.form.get('clothing', 0)),
            'electronics': float(request.form.get('electronics', 0)),
            'household_items': float(request.form.get('household_items', 0))
        }

        # Secondhand percentage
        products_data['secondhand_percentage'] = float(request.form.get('secondhand_percentage', 0))

        # Add products data to session
        user_data = session.get('user_data', {})
        user_data['products'] = products_data
        session['user_data'] = user_data

        # Calculate footprint and show results
        return redirect(url_for('results'))

    return render_template('products.html', title='Products Data')


@app.route('/results')
def results():
    """Display carbon footprint results"""
    if 'user_data' not in session:
        # Redirect to initial data entry if no user data exists
        return redirect(url_for('data_entry'))

    user_data = session.get('user_data', {})

    # Calculate carbon footprint
    footprint_data = calculator.calculate_footprint(user_data)

    # Generate charts
    charts = report_service.generate_charts(footprint_data)

    # Save data and results
    data_service.save_report(user_data, footprint_data)

    return render_template('results.html',
                           title='Your Carbon Footprint',
                           user_data=user_data,
                           footprint_data=footprint_data,
                           charts=charts)



@app.route('/reports')
def reports_list():
    """List all saved reports"""
    reports = data_service.get_all_reports()
    return render_template('reports.html', title='Saved Reports', reports=reports)


@app.route('/reports/<filename>')
def view_report(filename):
    """View a specific report"""
    report_data = data_service.get_report(filename)

    charts = report_service.generate_charts(report_data)

    if not report_data:
        flash('Report not found.', 'error')
        return redirect(url_for('reports_list'))

    return render_template('view_report.html',
                           title='View Report',
                           report_data=report_data,
                           charts=charts)



@app.route('/download-report')
def download_report():
    """Generate and download the PDF report"""
    if 'user_data' not in session:
        # Redirecting to initial data entry if nothing is entered
        return redirect(url_for('data_entry'))

    user_data = session.get('user_data', {})

    # Calc footprint
    footprint_data = calculator.calculate_footprint(user_data)

    # Generating charts
    charts = report_service.generate_charts(footprint_data)

    # Generating PDF report
    pdf = pdf_service.generate_report_pdf(user_data, footprint_data, charts)

    # Create a file-like object from the PDF data
    pdf_buffer = io.BytesIO(pdf)
    pdf_buffer.seek(0)

    # Determining the file name
    if user_data.get('user_type') == 'Organization':
        name = user_data.get('org_name', 'Unknown')
    else:
        name = user_data.get('name', 'Unknown')

    # Cleaning the name for the filename
    safe_name = ''.join(c if c.isalnum() else '_' for c in name)
    filename = f"carbon_footprint_report_{safe_name}.pdf"

    # Sending the PDF as a downloadable file
    return send_file(
        pdf_buffer,
        as_attachment=True,
        download_name=filename,
        mimetype='application/pdf',
    )
