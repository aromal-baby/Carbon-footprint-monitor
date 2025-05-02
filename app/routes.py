from flask import render_template, request, redirect, url_for, session, flash, jsonify
from matplotlib.pyplot import title

from app import app
from app.models.carbon_calculator import CarbonCalculator
import json
import os
import datetime

# Create calculator instance
calculator = CarbonCalculator()

@app.route('/')
def index():
    """Home page route"""
    return render_template('index.html', title='Carbon Footprint Monitor')

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

        # Redirect to energy data form
        return render_template('transportation.html', title='Transportation Data')


@app.route('/energy', methods=['GET', 'POST'])
def energy():
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
        return redirect(url_for('results'))

    return render_template('energy.html', title='Energy Data')

@app.route('/results')
def results():
    """Display carbon footprint results"""
    if 'user_data' not in session:
        # Redirect to initial data entry if no user data exists
        return redirect(url_for('data_entry'))

    user_data = session.get('user_data', {})

    # Calculate carbon footprint
    footprint_data = calculator.calculate_footprint(user_data)


    # Save data and results (for a real application)
    # save_report(user_data, footprint_data)

    return render_template('results.html',
                           title='Your Carbon Footprint',
                           user_data=user_data,
                           footprint_data=footprint_data)
