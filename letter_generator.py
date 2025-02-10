from datetime import datetime

def generate_negotiation_letter(name, address, current_rent, market_rate, violations, comps):
    """Generate a professionally formatted negotiation letter with data-driven arguments"""

    # Calculate rent difference percentage
    rent_difference = ((current_rent - market_rate) / market_rate) * 100
    rent_difference_str = f"{abs(rent_difference):.1f}%"

    letter_template = f"""
{datetime.now().strftime('%B %d, %Y')}

Dear Property Manager,

I hope this letter finds you well. My name is {name}, and I am currently renting the property. I am writing to discuss the current rental rate of ${current_rent:,.2f} per month and would like to present some market research to support a rate adjustment.

Market Analysis:
Based on extensive research of the local rental market, I have found that comparable properties in our area are renting for an average of ${market_rate:,.2f} per month. This indicates that the current rent is {rent_difference_str} {'above' if rent_difference > 0 else 'below'} the market rate.

"""
    if violations:
        letter_template += "\nBuilding Maintenance Considerations:\n"
        for violation in violations:
            letter_template += f"• {violation['type']}: {violation['description']}\n"
        letter_template += "\nThese maintenance issues affect the property's value and tenant quality of life, and should be considered in our rent discussion.\n"

    letter_template += """
Proposed Resolution:
1. A rent adjustment to better align with current market rates
2. A review of any outstanding maintenance issues
3. A meeting to discuss these points in detail

Benefits of Retention:
• Consistent, timely rent payments
• Proper maintenance and care of the property
• Stability and continuity, saving turnover costs

I value our landlord-tenant relationship and believe this adjustment would benefit both parties by ensuring a fair market rate while maintaining a reliable, long-term tenancy.

I would appreciate the opportunity to discuss this in person at your earliest convenience. Please contact me to schedule a meeting.

Thank you for your time and consideration.

Best regards,
"""
    letter_template += f"{name}\n"
    return letter_template