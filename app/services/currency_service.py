"""
    EcoTrack: Carbon Footprint Monitor - Currency Service
    Handles currency selection based on country
"""

class CurrencyService:
    """Service handling currency based on the country selected in the data entry form"""

    def __init__(self):
        """Initializing the service"""
        self.country_currency_map = {

            # Asia Pacific
            'Japan': {'symbol': '¥', 'code': 'JPY', 'name': 'Japanese Yen'},
            'China': {'symbol': '¥', 'code': 'CNY', 'name': 'Chinese Yuan'},
            'South Korea': {'symbol': '₩', 'code': 'KRW', 'name': 'Korean Won'},
            'India': {'symbol': '₹', 'code': 'INR', 'name': 'Indian Rupee'},
            'Singapore': {'symbol': 'S$', 'code': 'SGD', 'name': 'Singapore Dollar'},
            'Australia': {'symbol': 'A$', 'code': 'AUD', 'name': 'Australian Dollar'},
            'New Zealand': {'symbol': 'NZ$', 'code': 'NZD', 'name': 'New Zealand Dollar'},

            # North America
            'United States': {'symbol': '$', 'code': 'USD', 'name': 'US Dollar'},
            'Canada': {'symbol': 'C$', 'code': 'CAD', 'name': 'Canadian Dollar'},
            'Mexico': {'symbol': '$', 'code': 'MXN', 'name': 'Mexican Peso'},

            # South America
            'Brazil': {'symbol': 'R$', 'code': 'BRL', 'name': 'Brazilian Real'},

            # Africa
            'South Africa': {'symbol': 'R', 'code': 'ZAR', 'name': 'South African Rand'},

            # European Union (Euro)
            'Germany': {'symbol': '€', 'code': 'EUR', 'name': 'Euro'},
            'France': {'symbol': '€', 'code': 'EUR', 'name': 'Euro'},
            'Netherlands': {'symbol': '€', 'code': 'EUR', 'name': 'Euro'},
            'Austria': {'symbol': '€', 'code': 'EUR', 'name': 'Euro'},
            'Belgium': {'symbol': '€', 'code': 'EUR', 'name': 'Euro'},
            'Finland': {'symbol': '€', 'code': 'EUR', 'name': 'Euro'},
            'Italy': {'symbol': '€', 'code': 'EUR', 'name': 'Euro'},
            'Spain': {'symbol': '€', 'code': 'EUR', 'name': 'Euro'},
            'Portugal': {'symbol': '€', 'code': 'EUR', 'name': 'Euro'},

            # Other European Countries
            'United Kingdom': {'symbol': '£', 'code': 'GBP', 'name': 'British Pound'},
            'Switzerland': {'symbol': 'CHF', 'code': 'CHF', 'name': 'Swiss Franc'},
            'Denmark': {'symbol': 'kr', 'code': 'DKK', 'name': 'Danish Krone'},
            'Sweden': {'symbol': 'kr', 'code': 'SEK', 'name': 'Swedish Krona'},
            'Norway': {'symbol': 'kr', 'code': 'NOK', 'name': 'Norwegian Krone'},
        }

        # Default currency (fallback)
        self.default_currency = {'symbol': '€', 'code': 'EUR', 'name': 'Euro'}


    def get_currency_for_country(self, country):
        """To get the information of currency on a specific country"""
        return self.country_currency_map.get(country, self.default_currency)

    def get_currency_symbol(self, country):
        """To get the currency symbol on a specific country"""
        currency_info = self.get_currency_for_country(country)
        return currency_info['symbol']

    def get_currency_code(self, country):
        """To get the currency code on a specific country"""
        currency_info = self.get_currency_for_country(country)
        return currency_info['code']

    def get_all_currencies(self):
        """To get all currencies"""
        currencies = {}
        for country, currency in self.country_currency_map.items():
            code = currency['code']
            if code not in currencies:
                currencies[code] = currency

        return currencies