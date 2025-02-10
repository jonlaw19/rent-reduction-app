"""Real estate API integrations for HUD data"""
import os
import requests
from typing import Dict, Any, Optional

class HUDAPI:
    def __init__(self):
        self.api_key = os.getenv('HUD_API_KEY')
        # Updated base URL for HUD API
        self.base_url = "https://www.huduser.gov/hudapi/public/fmr/data"

    def get_fair_market_rent(self, zip_code: str) -> Optional[Dict[str, Any]]:
        """
        Fetch Fair Market Rent data from HUD API
        Returns None if data not found or error occurs
        """
        if not self.api_key:
            raise ValueError("HUD API key not configured")

        headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }

        params = {
            'zip': zip_code,
            # Use current year for FMR data
            'year': '2024'
        }

        try:
            response = requests.get(
                self.base_url, 
                headers=headers, 
                params=params,
                timeout=10
            )

            # Log the response for debugging
            print(f"HUD API Response Status: {response.status_code}")
            if response.status_code != 200:
                print(f"HUD API Error Response: {response.text}")
                return None

            return response.json()
        except requests.RequestException as e:
            print(f"Error fetching HUD data: {str(e)}")
            return None

# Initialize API client
hud_client = HUDAPI()