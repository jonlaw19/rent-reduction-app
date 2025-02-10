"""Gamification system for rental negotiations"""
from typing import Dict, Any, List, Optional
import math

def calculate_negotiation_power(market_data: Dict[str, Any], violations: List[Dict[str, Any]]) -> float:
    """Calculate negotiation power score (0-100) based on market conditions and violations"""
    base_score = 50
    
    # Market conditions impact (up to 30 points)
    if market_data:
        # Higher vacancy rate increases negotiation power
        vacancy_impact = market_data.get('vacancy_rate', 0) * 100 * 0.3
        # Negative yearly change increases negotiation power
        yearly_change = market_data.get('yearly_change', 0)
        trend_impact = -yearly_change * 100 * 0.2 if yearly_change < 0 else 0
        base_score += vacancy_impact + trend_impact
    
    # Building violations impact (up to 20 points)
    if violations:
        violation_score = min(20, len(violations) * 5)
        base_score += violation_score
    
    return min(100, max(0, base_score))

def calculate_negotiation_score(
    current_rent: float,
    market_rate: float,
    negotiation_power: float,
    violations: List[Dict[str, Any]],
    comps: List[Dict[str, Any]]
) -> Dict[str, Any]:
    """Calculate overall negotiation score and provide feedback"""
    
    # Base score starts at 60
    score = 60
    achievements = []
    tips = []
    
    # Market rate alignment (up to 20 points)
    rent_diff_percent = (market_rate - current_rent) / market_rate
    market_points = 20 * (1 - min(1, abs(rent_diff_percent)))
    score += market_points
    
    if rent_diff_percent > 0.1:
        achievements.append("🎯 Market Researcher")
        tips.append("Your rent is below market rate - great position!")
    elif rent_diff_percent < -0.1:
        tips.append("Consider using market rate data in your negotiation")
    
    # Supporting evidence (up to 10 points)
    evidence_points = 0
    if violations:
        evidence_points += min(5, len(violations))
        achievements.append("🔍 Evidence Collector")
    
    if len(comps) >= 3:
        evidence_points += 5
        achievements.append("📊 Data Analyst")
    
    score += evidence_points
    
    # Negotiation power bonus (up to 10 points)
    power_bonus = negotiation_power * 0.1
    score += power_bonus
    
    if negotiation_power >= 75:
        achievements.append("💪 Power Negotiator")
    elif negotiation_power <= 25:
        tips.append("Try finding more leverage points to strengthen your position")
    
    # Calculate level
    level = math.floor(score / 10)
    next_level_progress = (score % 10) * 10  # Progress to next level (0-100)
    
    return {
        "score": round(score, 1),
        "level": level,
        "next_level_progress": next_level_progress,
        "achievements": achievements,
        "tips": tips,
        "components": {
            "market_alignment": round(market_points, 1),
            "evidence_strength": round(evidence_points, 1),
            "negotiation_power": round(power_bonus, 1)
        }
    }

def get_level_title(level: int) -> str:
    """Get the title for the current negotiation level"""
    titles = {
        0: "Novice Negotiator",
        1: "Rent Rookie",
        2: "Market Apprentice",
        3: "Deal Detective",
        4: "Savings Seeker",
        5: "Bargain Baron",
        6: "Negotiation Ninja",
        7: "Rental Rockstar",
        8: "Property Pro",
        9: "Master Mediator",
        10: "Legendary Landlord Liaison"
    }
    return titles.get(level, "Supreme Negotiator")
