"""
Carbon Footprint Monitor - Carbon Calculator
Calculates carbon footprint based on user input data
"""
from unittest import result

from app.models.emission_factors import (
    TRANSPORTATION_FACTORS,
    ENERGY_FACTORS,
    WASTE_FACTORS,
    FOOD_FACTORS,
    PRODUCT_FACTORS
)
from contourpy.util import data


class CarbonCalculator:
    """Calculates carbon footprint based on user data"""

    def calculate_footprint(self, data):
        """Calculate total carbon footprint from all categories"""
        results = {
            'total': 0,
            'categories': {}
        }

        # Calculate footprint for each category
        for category in ['transportation', 'energy', 'waste', 'food', 'products']:
            if category in data:
                category_footprint = self.calculate_category_footprint(category, data[category])
                results['categories'][category] = category_footprint
                result['total'] += category_footprint['total']

            # Adding capita results if it's an organization
            if 'user_type' in data and data['user_type'] == 'Organization' in data and data['employees'] > 0:
                results['per_capita'] = results['total'] / data['employees']
            elif 'user_type' in data and data['user_type'] == 'Individual' in data and data['household_size'] > 0:
                results['per_capita'] = results['total'] / data['household_size']

            return results


        def calculate_category_footprint(self, category, data):
            """Calculate footprint for a specific category"""
            if category == 'transportation':
                return self.calculate_transport_footprint(data)
            elif category == 'energy':
                return self.calculate_energy_footprint(data)
            elif category == 'waste':
                return self.calculate_waste_footprint(data)
            elif category == 'food':
                return self.calculate_food_footprint(data)
            elif category == 'products':
                return self.calculate_product_footprint(data)
            return {'total': 0, 'categories': {}}


        def calculate_transport_footprint(data):
            """Calculate transportation carbon footprint"""
            result = {'total': 0, 'breakdown': {}}


            # Car emissions
            if 'car' in data:
                car_data = data['car']
                weekly_km = car_data.get('weekly_km', 0)
                fuel_type = car_data.get('fuel_type', 'petrol')

                # Calculate annual car emissions
                annual_km = weekly_km * 52
                emission_factor = TRANSPORTATION_FACTORS['car'].get(fuel_type, TRANSPORTATION_FACTORS['car']['petrol'])
                car_emissions = annual_km * emission_factor

                result['breakdown']['car'] = car_emissions
                result['total'] += car_emissions


            # Public transport emissions
            if 'public_transport' in data:
                weekly_km = data['public_transport'].get('weekly_km', 0)
                annual_km = weekly_km * 52
                emission_factor = TRANSPORTATION_FACTORS['public_transport']['average']
                public_transport_emissions = annual_km * emission_factor

                result['breakdown']['public_transport'] = public_transport_emissions
                result['total'] += public_transport_emissions


            # Air travel emissions
            if 'air_travel' in data:
                short_flights = data['air_travel'].get('short_flights', 0)
                long_flights = data['air_travel'].get('long_flights', 0)

                short_flight_emission = short_flights * TRANSPORTATION_FACTORS['air_travel']['average_short']
                long_flight_emission = long_flights * TRANSPORTATION_FACTORS['air_travel']['average_long']
                flight_emissions = short_flight_emission + long_flight_emission

                result['breakdown']['air_travel'] = flight_emissions
                result['total'] += flight_emissions

            return result


        def calculate_energy_footprint(data):
            """Calculate energy carbon footprint"""
            result = {'total': 0, 'breakdown': {}}

            # Electricity emissions
            if 'electricity' in data:
                monthly_kwh = data['electricity'].get('monthly_kwh', 0)
                renewable_percentage = data['electricity'].get('renewable_percentage', 0) / 100

                annual_kwh = monthly_kwh * 12
                grid_kwh = annual_kwh * (1 - renewable_percentage)
                renewable_kwh = annual_kwh * renewable_percentage

                grid_emissions = grid_kwh * ENERGY_FACTORS['electricity']['grid']
                renewable_emissions = renewable_kwh * ENERGY_FACTORS['electricity']['renewable']
                electricity_emissions = grid_emissions + renewable_emissions

                result['breakdown']['electricity'] = electricity_emissions
                result['total'] += electricity_emissions


            # Natural gas emissions
            if 'gas' in data:
                monthly_usage = data['gas'].get('monthly_usage', 0)
                annual_usage = monthly_usage * 12
                gas_emissions = annual_usage * ENERGY_FACTORS['natural_gas']

                result['breakdown']['gas'] = gas_emissions
                result['total'] += gas_emissions

            return result


        def calculate_waste_footprint(data):
            """Calculate waste carbon footprint"""
            result = {'total': 0, 'breakdown': {}}

            # General waste emissions
            if 'general_waste' in data:
                weekly_kg = data['general_waste'].get('weekly_kg', 0)
                annual_kg = weekly_kg * 52
                waste_emissions = annual_kg * ENERGY_FACTORS['general_waste']

                result['breakdown']['general_waste'] = waste_emissions
                result['total'] += waste_emissions

            # Recycling (emission saved)
            if 'recycling' in data:
                recycling_data = data['recycling']
                recycling_emissions = 0

                for material, weekly_kg in recycling_data.items():
                    if material in WASTE_FACTORS['recycling']:
                        annual_kg = weekly_kg * 52
                        material_emissions = annual_kg * WASTE_FACTORS['recycling'][material]
                        recycling_emissions += material_emissions

                    result['breakdown']['recycling'][material] = recycling_emissions
                    result['total'] += recycling_emissions

            # Composting (emission saved)
            if 'composting' in data and data['composting'] and 'general_waste' in data:
                # Assume 30% of waste could be composted if not already
                potential_compost_kg = data['general_waste'].get('weekly_kg', 0) * 0.3 * 52
                composting_savings = potential_compost_kg * WASTE_FACTORS['composting_reduction']

                # If composting, subtract the savings from total
                result['breakdown']['composting_benefits'] = -composting_savings
                result['total'] += composting_savings

            return result


        def calculate_food_footprint(data):
            """Calculate food carbon footprint"""
            result = {'total': 0, 'breakdown': {}}

            # Base diet emissions
            diet_type = data.get('diet_type', 'omnivore')
            daily_emissions = FOOD_FACTORS[diet_type].get(diet_type, FOOD_FACTORS['diet_type']['omnivore'])
            annual_diet_emissions = daily_emissions * 365

            result['breakdown']['base_diet'] = annual_diet_emissions
            result['total'] += annual_diet_emissions

            # Specific meat consumption (for accurate calc)
            if 'meat_consumption' in data:
                meat_data = data['meat_consumption']
                meat_emissions = 0

                # Calculate specific meat emissions and subtract from base diet
                # (since base diet already includes average meat consumption)
                for meat_type, weekly_kg in meat_data.items():
                    if meat_type in FOOD_FACTORS['meat_and_fish']:
                        annual_kg = weekly_kg * 52
                        type_emissions = annual_kg * FOOD_FACTORS['meat_and_fish'][meat_type]
                        meat_emissions += type_emissions

                # Adjust if specific meat consumption is tracked
                if meat_emissions > 0:
                    # Subtract a portion of base diet (estimated meat portion)
                    meat_portion = 0.5 if diet_type == 'omnivore' else 0.3
                    result['breakdown']['base_diet'] = annual_diet_emissions * (1 - meat_portion)
                    result['breakdown']['specific_meat'] = meat_emissions

                    # Adjust total
                    result['total'] = result['total'] - (annual_diet_emissions * meat_portion) + meat_emissions


            # Local food benefit
            local_percentage = data.get('local_food_percentage', 0) / 100
            if local_percentage > 0:
                local_food_benefit = result['total'] * local_percentage * FOOD_FACTORS['local_food_reduction']
                result['breakdown']['local_food_benefit'] = -local_food_benefit
                result['total'] -= local_food_benefit

            return result


        def calculate_products_footprint(self, data):
            """Calculate products footprint"""
            result = {'total': 0, 'breakdown': {}}

            if 'monthly_spending' in data:
                spending_data = data['monthly_spending']
                product_emissions = 0


                # Calculate emissions for each product factory
                for category, monthly_amount in spending_data.items():
                    annual_amount = monthly_amount * 12
                    if category in PRODUCT_FACTORS:
                        category_emissions = annual_amount * PRODUCT_FACTORS[category]
                    else:
                        # Use an average factor if specific category not found
                        category_emissions = annual_amount * 0.5


                    result['breakdown'][category] = category_emissions
                    product_emissions += category_emissions

                # Secondhand benefit
                secondhand_percentage = data.get('secondhand_percentage', 0) / 100
                if secondhand_percentage > 0:
                    secondhand_benefit = product_emissions * secondhand_percentage * PRODUCT_FACTORS['secondhand_reduction']
                    result['breakdown']['secondhand_benefit'] = -secondhand_benefit
                    product_emissions -= secondhand_benefit

                result['total'] += product_emissions


            return result





