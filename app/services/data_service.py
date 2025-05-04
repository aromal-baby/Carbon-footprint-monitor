"""
Data Service:
    Handles storage and retrieval of user data and reports
"""


import os
import json
import datetime

class DataService:
    """Service for storing and retrieving carbon footprint data"""

    def __init__(self):
        """Initializing data service"""
        self.reports_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'reports')

        # Creating the report directory if it doesn't already exist
        if not os.path.exists(self.reports_dir):
            os.makedirs(self.reports_dir)


    def save_report(self, user_data, footprint_data):
        """Save report data to the file"""
        # Creating a unique file for it
        timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')

        if 'user_type' in user_data and user_data['user_type'] == 'Organization':
            name = user_data.get('org_name', 'Unknown organization')
        else:
            name = user_data.get('name', 'Unknown Individual')

        # Clean the name for the file name
        safe_name = ''.join(c if c.isalnum() else '_' for c in name)

        filename = f"{timestamp}_{safe_name}.json"
        filepath = os.path.join(self.reports_dir, filename)

        # Combine data for storage
        report_data = {
            'user_data': user_data,
            'footprint_data': footprint_data,
            'timestamp': timestamp,
            'date': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        }

        # Save to file
        with open(filepath, 'w') as f:
            json.dump(report_data, f, indent=4)

        return filepath


    def get_all_reports(self):
        """Get a list of all saved reports"""
        reports = []

        if not os.path.exists(self.reports_dir):
            return reports

        for filename in os.listdir(self.reports_dir):
            if filename.endswith('.json'):
                filepath = os.path.join(self.reports_dir, filename)
                try:
                    with open(filepath, 'r') as f:
                        report_data = json.load(f)

                    # Extracting key information for listing
                    report_info = {
                        'filename': filename,
                        'date': report_data.get('date', 'Unknown'),
                        'name': self.get_report_name(report_data.get('user_data', {})),
                        'total_footprint': report_data.get('footprint_data', {}).get('total', 0),
                        'filepath': filepath
                    }

                    reports.append(report_info)
                except:
                    # Skip files that can't be parsed
                    continue

        # Sort by date (newest first)
        reports.sort(key=lambda x: x['date'], reverse=True)

        return reports

def get_report(self, filename):
    """Get a specific report by filename"""
    filepath = os.path.join(self.reports_dir, filename)

    if not os.path.exists(filepath):
        return None

    try:
        with open(filepath, 'r') as f:
            report_data = json.load(f)
        return report_data
    except:
        return None


def _get_report_name(self, user_data):
    """Get the name to display for a report"""
    if user_data.get('user_type') == 'Organization':
        return user_data.get('org_name', 'Unknown Organization')
    else:
        return user_data.get('name', 'Unknown Individual')