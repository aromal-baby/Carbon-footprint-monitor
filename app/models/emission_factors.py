"""
Carbon Footprint Monitor - Emission Factors
Contains emission factors used for carbon footprint calculations
"""

# Transportation emission factors (kg CO2e)
TRANSPORTATION_FACTORS = {
    'car': {
        'petrol': 0.192,      # kg CO2e per km
        'diesel': 0.171,
        'hybrid': 0.106,
        'electric': 0.053,    # kg CO2e per km (depends on electricity source)
    },
    'public_transport': {
        'bus': 0.105,         # kg CO2e per km
        'train': 0.041,
        'subway': 0.027,
        'average': 0.058,     # kg CO2e per km (average)
    },
    'air_travel': {
        'short_haul': 0.255,  # kg CO2e per km
        'long_haul': 0.150,   # kg CO2e per km
        'average_short': 500, # kg CO2e per short flight (<1500 km)
        'average_long': 1800, # kg CO2e per long flight (>1500 km)
    },
}

# Energy emission factors
ENERGY_FACTORS = {
    'electricity': {
        'grid': 0.350,       # kg CO2e per kWh (varies by country)
        'renewable': 0.025,
    },
    'natural_gas': 2.03,     # kg CO2e per m3
    'heating_oil': 2.68,     # kg CO2e per liter
}

# Waste emission factors
WASTE_FACTORS = {
    'general_waste': 0.58,   # kg CO2e per kg waste
    'recycling': {
        'paper': 0.04,       # kg CO2e per kg recycled
        'plastic': 0.035,
        'glass': 0.03,
        'metal': 0.02,
    },
    'composting_reduction': 0.55,   # kg CO2e saved per kg waste composted vs Landfill
}

# Food emission factors
FOOD_FACTORS = {
    'diet_type': {
        'omnivore': 2.5,      # kg CO2e per day
        'pescatarian': 1.9,
        'vegetarian': 1.7,
        'vegan': 1.5,
    },
    'meat_and_flesh': {
        'red_meat': 27.0,     # kg CO2e per kg
        'poultry': 6.9,
        'fish': 6.1,
    },
    'local_food_reduction': 0.15,   # Percentage reduction for local food
}

# Product emission factors
PRODUCT_FACTORS = {
    'clothing': 0.5,          # kg CO2e per EUR
    'electronics': 0.7,
    'household_items': 0.4,
    'secondhand_reduction': 0.8,    # Percentage reduction for secondhand items
}


# Reduction potentials
REDUCTION_POTENTIAL = {
    'transportation': {
        'car_to_public': 0.6,       # 60% reduction by switching from car to public transport
        'car_to_bike': 0.95,        # 95% reduction by switching from car to biking
        'petrol_to_electric': 0.7,  # 70% reduction by switching from petrol to electric car
        'reduce_flights': 1800,     # kg CO2e saved per long flight avoided
    },
    'energy': {
        'renewable_electricity': 0.33,      # 33% reduction by switching to 100% renewable electricity
        'energy_efficient_appliances': 0.3, # 30% reduction in electricity usage
        'improved_insulation': 0.25,        # 25% reduction in heating needs
        'smart_thermostat': 0.15,           # 15% reduction in heating needs
    },
    'waste': {
        'zero_waste': 0.58,        # kg CO2e saved per kg waste reduced
        'start_composting': 0.55,  # kg CO2e saved per kg waste composted
    },
    'food': {
        'reduce_red_meat': 0.3,     # 30% reduction by cutting red meat consumption in half
        'vegetarian_diet': 0.35,    # 35% reduction by switching to vegetarian diet
        'vegan_diet': 0.47,         # 47% reduction by switching to vegan diet
        'local_food': 0.15,         # 15% reduction by eating local food
    },
    'products': {
        'reduce_consumption': 0.35,  # 35% reduction by reducing overall consumption
        'buy_secondhand': 0.8,       # 80% reduction by buying secondhand
        'extend_product_life': 0.3,  # 30% reduction by extending product lifespan
    }
}