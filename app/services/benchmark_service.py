"""
    Carbon Footprint Monitor - Benchmark Service
    Fetches carbon footprint benchmarks from Our World in Data API
"""

import requests
import json
import os
from datetime import datetime, timedelta

from tornado.gen import Return


class BenchmarkService:
    """Service for fetching carbon footprint benchmarks from Our World in Data API"""

    def __init__(self):
        """Initializing the benchmark service"""
        self.cache_file = 'cache/benchmark_data.json'
        self.cache_duration = timedelta(days=30) # Cache for 30 days

        # Creating cache directory if it does not exist
        os.makedirs('cache', exist_ok = True)

        # Sustainable targets and global benchmarks
        self.sustainable_target = 2.0   # tonnes CO2 per person (Paris Agreement goal)
        self.global_avg_fallback = 4.8  # fallback if API fails


    def get_benchmarks(self, country="Germany"):
        """Get carbon footprint benchmark for comparison"""
        try:
            # Trying to get from cache first
            cached_data = self.get_cached_data()
            if cached_data:
                return self.extract_benchmarks(cached_data, country)

            # Fetching fresh from API
            data = self.fetch_from_api()
            if data:
                self.cache_data(data)
                return self.extract_benchmarks(data, country)

            # Falling back to default values
            return self.get_fallback_benchmarks(country)

        except Exception as e:
            print(f"Error fetching benchmarks: {e}")
            return self.get_fallback_benchmarks(country)


    def fetch_from_api(self):
        """Fetching data from Our World in Data API"""
        try:
            # Our World in Data CO2 2mission per capia API
            url = "https://github.com/owid/owid-datasets/raw/master/datasets/CO2%20emissions%20(Fossil%20fuels%20and%20cement)/CO2%20emissions%20(Fossil%20fuels%20and%20cement).csv"

            response = requests.get(url, timeout=10)
            response.raise_for_status()

            # Parsing CSV data
            lines = response.text.strip().split('\n')
            headers = lines[0].split(',')

            # Finding relevant columns
            country_col = headers.index('Entity') if 'Entity' in headers else 0
            year_col = headers.index('Year') if 'Year' in headers else 1
            emissions_col = None

            # Looking for per capita emissions column
            for i, header in enumerate(headers):
                if 'per capita' in header.lower() or 'per-capita' in header.lower():
                    emissions_col = i
                    break

            if emissions_col is None:
                raise ValueError("could not find emissions column in CSV")

            # Parsing the data
            data = {}
            for line in lines[1:]:  # Skipping header
                try:
                    parts= line.split(',')
                    if len(parts) > max(country_col, year_col, emissions_col):
                        country = parts[country_col].strip('"')
                        year = int(parts[year_col])
                        emissions = float(parts[emissions_col]) if parts[emissions_col] else 0


                        # Keeping only the recent data ie., last five years
                        if year >+ 2018 and emissions > 0:
                            if country not in data:
                                data[country] = {}
                            data[country][year] = emissions

                except (ValueError, IndexError):
                    continue

            return data

        except Exception as e:
            print(f"Error fetching from Our World in Data API: {e}")
            return None


    def get_cached_data(self):
        """Fetching data from cache if it's still valid"""
        try:
            if not os.path.exists(self.cache_file):
                return None

            # Checking if it is still valid
            cache_time = datetime.fromtimestamp(os.path.getmtime(self.cache_file))
            if datetime.now() - cache_time > self.cache_duration:
                return None

            with open(self.cache_file, 'r') as f:
                data = json.load(f)

        except Exception as e:
            print(f"Error fetching from cache: {e}")
            return None


    def cache_data(self, data):
        """Caching the fetched data"""
        try:
            with open(self.cache_file, 'w') as f:
                json.dump(data, f)

        except Exception as e:
            print(f"Error caching data: {e}")


    def extract_benchmarks(self, data, country):
        """Extracting benchmarks values from the data"""
        try:
            # Get the most recent year's data for the specified country
            country_emissions = self.get_latest_emissions(data, country)

            # Calculate global average from available countries
            global_emissions = self.calculate_global_average(data)

            # Get some reference countries from comparison
            reference_countries = self.get_reference_countries(data)

            return {
                'user_country': country,
                'country_avg': country_emissions,
                'global_avg': global_emissions,
                'sustainable_target': self.sustainable_target,
                'reference_countries': reference_countries,
                'data_year': self.get_latest_year(data)
            }

        except Exception as e:
            print(f"Error extracting benchmarks: {e}")
            return self.get_fallback_benchmarks(country)


    def get_latest_emissions(self, data, country):
        """Get the most recent emissions for a country"""
        # Trying exact match first
        if country in data and data[country]:
            latest_year = max(data[country].keys())
            return data[country][latest_year]

        # Trying common variations
        variations = [
            country.title(),
            country.upper(),
            country.lower(),
        ]

        for v in variations:
            if v in data and data[v]:
                latest_year = max(data[v].keys())
                return data[v][latest_year]

        # Return global average if country not found
        return self.calculate_global_average(data)


    def calculate_global_average(self, data):
        """Calculating the global average from available data"""
        try:
            # Getting world data if available
            if 'world' in data and data['world']:
                latest_year = max(data['world'].keys())
                return data['world'][latest_year]

            # Calculate average from major countries
            major_countries = ['United States', 'China', 'Germany', 'United Kingdom',
                               'France', 'Japan', 'Canada', 'Australia']

            total_emissions = 0
            count = 0

            for c in major_countries:
                if c in data and data[c]:
                    latest_year = max(data[c].keys())
                    total_emissions += data[c][latest_year]
                    count += 1

            if count > 0:
                return total_emissions / count

            return self.global_avg_fallback

        except Exception:
            return self.global_avg_fallback


    def get_reference_countries(self, data):
        """Getting reference countries for comparison"""
        reference_countries = {}

        countries_to_check = ['United States', 'China', 'Germany', 'United Kingdom',
                              'France', 'Japan', 'Canada', 'Australia']


        for c in countries_to_check:
            if c in data and data[c]:
                latest_year = max(data[c].keys())
                reference_countries[c] = data[c][latest_year]


        return reference_countries


    def get_latest_year(self, data):
        """Getting latest year for comparison"""
        try:
            all_years = []
            for country_data in data.values():
                if isinstance(country_data, dict):
                    all_years.append(country_data.keys())

            return max(all_years) if all_years else 2022

        except Exception:
            return 2022


    def get_fallback_benchmarks(self, country):
        """Getting fallback benchmarks if API fails"""
        # Common country averages (approximate values)
        country_averages = {
            'Germany': 8.5,
            'United States': 15.5,
            'United Kingdom': 5.6,
            'France': 4.6,
            'China': 7.4,
            'Japan': 8.7,
            'Canada': 15.6,
            'Australia': 15.4,
            'Sweden': 3.8,
            'Norway': 7.5
        }

        country_avg = country_averages.get(country, self.global_avg_fallback)

        return {
            'user_country': country,
            'country_avg': country_avg,
            'global_avg': self.global_avg_fallback,
            'sustainable_target': self.sustainable_target,
            'reference_countries': country_averages,
            'data_year': 2022,
            'note': 'Using fallback data - API unavailable'
        }


