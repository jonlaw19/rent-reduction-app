import json
import pandas as pd
import numpy as np
from utils.data_loader import load_market_data, load_rental_comps

def load_violations_data():
    """Load mock violations data from JSON file"""
    try:
        with open('data/mock_violations.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        # Create mock violations data if file doesn't exist
        mock_data = {
            "building_violations": [],
            "tenant_rights": [
                "Right to a habitable dwelling",
                "Right to repairs and maintenance",
                "Right to privacy",
                "Protection against retaliation",
                "Security deposit protection"
            ]
        }
        with open('data/mock_violations.json', 'w') as f:
            json.dump(mock_data, f)
        return mock_data

def calculate_rent_score(current_rent, zip_code):
    """Calculate a rent score based on market data"""
    market_data = load_market_data(zip_code)

    if not market_data:
        return 50, 'No Market Data Available'

    avg_rent = market_data['avg_rent']

    if current_rent > avg_rent:
        score = 100 - min(100, ((current_rent - avg_rent) / avg_rent * 100))
    else:
        score = 100

    return max(0, score), 'Local Market Data'

def get_comparable_units(zip_code, current_rent, tolerance=0.2):
    """Find comparable units within the same zip code"""
    comps = load_rental_comps(zip_code, current_rent, tolerance)
    return comps, 'Local Market Data'

def get_market_insights(zip_code):
    """Get market insights for the given zip code"""
    market_data = load_market_data(zip_code)
    if not market_data:
        return {
            'avg_rent': 0,
            'vacancy_rate': 0,
            'yearly_change': 0,
            'seasonal_patterns': {},
            'data_source': 'No Data Available'
        }
    return market_data

def get_building_violations(address):
    """Get building violations for the given address"""
    data = load_violations_data()
    violations = [
        building['violations'] for building in data['building_violations']
        if building['address'].lower() == address.lower()
    ]
    return violations[0] if violations else []

def get_tenant_rights():
    """Get list of tenant rights"""
    data = load_violations_data()
    return data['tenant_rights']

def load_rental_data():
    """Load mock rental data from JSON file"""
    with open('data/mock_rental_data.json', 'r') as f:
        return json.load(f)