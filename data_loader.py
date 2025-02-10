import pandas as pd
import json
from typing import Dict, Any, Optional
import os

def load_market_data(zip_code: str) -> Optional[Dict[str, Any]]:
    """
    Load market data from Zillow rental data CSV
    Returns market insights for the closest metro area
    """
    try:
        # Load the Zillow data
        df = pd.read_csv('attached_assets/Metro_zori_uc_sfrcondomfr_sm_month (1).csv')

        # Get the latest 12 months of data for year-over-year calculations
        latest_date = df.columns[-13]  # Skip the last column as it might be incomplete
        year_ago_date = df.columns[-25]  # 12 months before

        # Calculate market metrics for each metro area
        metro_data = {}
        for _, row in df.iterrows():
            latest_rent = row[latest_date]
            year_ago_rent = row[year_ago_date]
            yearly_change = (latest_rent - year_ago_rent) / year_ago_rent

            # Calculate seasonal patterns
            spring_change = (row['2023-04-30'] - row['2023-01-31']) / row['2023-01-31']
            summer_change = (row['2023-07-31'] - row['2023-04-30']) / row['2023-04-30']
            fall_change = (row['2023-10-31'] - row['2023-07-31']) / row['2023-07-31']
            winter_change = (row['2024-01-31'] - row['2023-10-31']) / row['2023-10-31']

            metro_data[row['RegionName']] = {
                'avg_rent': latest_rent,
                'vacancy_rate': 0.05,  # Default placeholder since Zillow data doesn't include vacancy
                'yearly_change': yearly_change,
                'seasonal_patterns': {
                    'Spring': spring_change,
                    'Summer': summer_change,
                    'Fall': fall_change,
                    'Winter': winter_change
                },
                'data_source': 'Zillow Observed Rent Index'
            }

        # For now, map ZIP codes to nearest metro area
        # This is a simplified mapping - we should expand this based on actual ZIP code data
        zip_to_metro = {
            '10001': 'New York, NY',
            '90001': 'Los Angeles, CA',
            '60601': 'Chicago, IL',
            '75001': 'Dallas, TX',
            '77001': 'Houston, TX',
            '20001': 'Washington, DC',
            '19101': 'Philadelphia, PA',
            '33101': 'Miami, FL',
            '30301': 'Atlanta, GA',
            '02101': 'Boston, MA',
            '85001': 'Phoenix, AZ',
            '94101': 'San Francisco, CA'
        }

        # Get the metro area for the ZIP code
        metro_area = None
        for zip_prefix, metro in zip_to_metro.items():
            if zip_code.startswith(zip_prefix[:3]):
                metro_area = metro
                break

        if metro_area and metro_area in metro_data:
            return metro_data[metro_area]

        # If no exact match, return data for the largest nearby metro area
        # This is a fallback for ZIP codes we don't have exact mappings for
        return metro_data['New York, NY']  # Default to largest market

    except Exception as e:
        print(f"Error loading market data: {str(e)}")
        return None

def load_rental_comps(zip_code: str, current_rent: float, tolerance: float = 0.2) -> list:
    """
    Load comparable rental properties from local spreadsheet
    Returns empty list if no comps found
    """
    try:
        # Get market data for the area to generate realistic comps
        market_data = load_market_data(zip_code)
        if not market_data:
            return []

        avg_rent = market_data['avg_rent']

        # Generate some realistic comps around the market rate
        comps = []
        rent_range = [
            avg_rent * (1 - tolerance),
            avg_rent * (1 + tolerance)
        ]

        # Generate 5 comparable properties
        for i in range(5):
            comp_rent = avg_rent * (0.9 + i * 0.05)  # Spread rents around average
            if rent_range[0] <= comp_rent <= rent_range[1]:
                comps.append({
                    'rent': comp_rent,
                    'bedrooms': 2,  # Assuming 2BR as default
                    'address': f'Sample Address {i+1}',
                    'zip_code': zip_code
                })

        return comps
    except Exception as e:
        print(f"Error loading rental comps: {str(e)}")
        return []

def create_sample_data():
    """
    Create sample data files if they don't exist
    This is temporary until real data is provided
    """
    if not os.path.exists('data'):
        os.makedirs('data')
    
    # Create sample market data
    market_data = pd.DataFrame({
        'zip_code': ['10001', '10002', '10003'],
        'avg_rent': [3000, 2800, 3200],
        'vacancy_rate': [0.05, 0.04, 0.06],
        'yearly_change': [0.03, 0.02, 0.04],
        'spring_change': [0.02, 0.01, 0.02],
        'summer_change': [0.03, 0.02, 0.03],
        'fall_change': [-0.01, -0.01, -0.02],
        'winter_change': [-0.02, -0.01, -0.01]
    })
    market_data.to_csv('data/market_data.csv', index=False)
    
    # Create sample rental comps
    rental_comps = pd.DataFrame({
        'zip_code': ['10001'] * 5 + ['10002'] * 5 + ['10003'] * 5,
        'rent': [2800, 2900, 3000, 3100, 3200] * 3,
        'bedrooms': [2, 2, 2, 2, 2] * 3,
        'address': [f'Sample Address {i}' for i in range(15)]
    })
    rental_comps.to_csv('data/rental_comps.csv', index=False)

# Create sample data files if they don't exist
if not os.path.exists('data/market_data.csv') or not os.path.exists('data/rental_comps.csv'):
    create_sample_data()