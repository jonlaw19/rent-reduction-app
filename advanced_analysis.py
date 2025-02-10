import json
import os
from typing import Dict, Any, List, Optional
from openai import OpenAI

# the newest OpenAI model is "gpt-4o" which was released May 13, 2024.
# do not change this unless explicitly requested by the user
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def analyze_market_trends(market_data: Dict[str, Any], current_rent: float) -> Dict[str, Any]:
    """Analyze market trends and generate insights using OpenAI"""
    try:
        prompt = f"""
        Analyze the following rental market data and provide insights in JSON format:
        - Current Rent: ${current_rent}
        - Market Average: ${market_data.get('avg_rent', 0)}
        - Vacancy Rate: {market_data.get('vacancy_rate', 0)*100}%
        - Yearly Change: {market_data.get('yearly_change', 0)*100}%
        - Seasonal Patterns: {market_data.get('seasonal_patterns', {})}

        Provide analysis in this JSON format:
        {{
            "market_position": string (whether the rent is above/below market),
            "price_trend": string (increasing/decreasing/stable),
            "negotiation_leverage": string (strong/moderate/weak),
            "best_time_to_negotiate": string (recommended season),
            "key_insights": list of strings (3-4 key observations),
            "confidence_score": float (0-1)
        }}
        """

        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{
                "role": "user",
                "content": prompt
            }],
            response_format={"type": "json_object"}
        )
        
        return json.loads(response.choices[0].message.content)
    except Exception as e:
        print(f"Error in market trend analysis: {str(e)}")
        return {
            "market_position": "unknown",
            "price_trend": "stable",
            "negotiation_leverage": "moderate",
            "best_time_to_negotiate": "current",
            "key_insights": ["Unable to generate detailed insights"],
            "confidence_score": 0.5
        }

def calculate_price_metrics(current_rent: float, market_data: Dict[str, Any], comps: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Calculate advanced price metrics"""
    try:
        # Calculate price per bedroom
        comp_prices_per_bedroom = [comp['rent'] / comp['bedrooms'] for comp in comps if comp.get('bedrooms', 0) > 0]
        avg_price_per_bedroom = sum(comp_prices_per_bedroom) / len(comp_prices_per_bedroom) if comp_prices_per_bedroom else 0
        
        # Calculate market position percentile
        all_rents = [comp['rent'] for comp in comps] + [current_rent]
        all_rents.sort()
        percentile = (all_rents.index(current_rent) / len(all_rents)) * 100

        # Calculate price volatility
        seasonal_patterns = market_data.get('seasonal_patterns', {})
        price_volatility = max(seasonal_patterns.values()) - min(seasonal_patterns.values()) if seasonal_patterns else 0

        return {
            "price_per_bedroom": avg_price_per_bedroom,
            "market_percentile": percentile,
            "price_volatility": price_volatility,
            "value_score": calculate_value_score(current_rent, market_data, comps)
        }
    except Exception as e:
        print(f"Error calculating price metrics: {str(e)}")
        return {
            "price_per_bedroom": 0,
            "market_percentile": 50,
            "price_volatility": 0,
            "value_score": 50
        }

def calculate_value_score(current_rent: float, market_data: Dict[str, Any], comps: List[Dict[str, Any]]) -> float:
    """Calculate a value score (0-100) based on multiple factors"""
    try:
        # Base score starts at 50
        score = 50
        
        # Adjust based on market rate difference
        market_rate = market_data.get('avg_rent', current_rent)
        if market_rate > 0:
            rate_diff_percent = (market_rate - current_rent) / market_rate
            score += rate_diff_percent * 30  # Adjust up to 30 points based on market rate
        
        # Adjust based on comparable properties
        if comps:
            comp_avg = sum(comp['rent'] for comp in comps) / len(comps)
            if comp_avg > 0:
                comp_diff_percent = (comp_avg - current_rent) / comp_avg
                score += comp_diff_percent * 20  # Adjust up to 20 points based on comps
        
        return max(0, min(100, score))  # Ensure score is between 0 and 100
    except Exception as e:
        print(f"Error calculating value score: {str(e)}")
        return 50
