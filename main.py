import streamlit as st
import pandas as pd
from utils.analysis import (
    calculate_rent_score, get_comparable_units, get_market_insights,
    get_building_violations, get_tenant_rights
)
from utils.letter_generator import generate_negotiation_letter
from utils.visualization import create_rent_comparison_chart, create_trend_chart
from database.models import User, RentSearch, init_db
from database.session import get_session
import urllib.parse

def save_search_data(name, email, address, zip_code, current_rent, market_rate, rent_score):
    try:
        session = get_session()
        user = session.query(User).filter(User.email == email).first()
        if not user:
            user = User(name=name, email=email)
            session.add(user)
            session.flush()

        rent_search = RentSearch(
            user_id=user.id,
            address=address,
            zip_code=zip_code,
            current_rent=current_rent,
            market_rate=market_rate,
            rent_score=rent_score
        )
        session.add(rent_search)
        session.commit()
    except Exception as e:
        st.error(f"Error saving data: {str(e)}")
    finally:
        if 'session' in locals():
            session.close()

def analyze_rent():
    """Main rent analysis function"""
    # Initialize database tables
    try:
        init_db()
    except Exception as e:
        st.error(f"Database initialization error: {str(e)}")

    st.title("🏠 RentLeverage")
    st.subheader("Instant Rent Negotiation Power")

    # User Input Section
    col1, col2 = st.columns(2)

    with col1:
        address = st.text_input(
            "Enter your address",
            help="Start typing your address...",
            key="address_input",
            autocomplete="street-address"
        )
        zip_code = st.text_input(
            "Enter your ZIP code",
            max_chars=5,
            help="5-digit ZIP code",
            key="zip_code_input"
        )

    with col2:
        current_rent = st.number_input(
            "Enter your current monthly rent ($)",
            min_value=0,
            help="Your current monthly rent amount"
        )
        name = st.text_input(
            "Enter your name",
            help="Your full name for the negotiation letter",
            key="name_input"
        )
        email = st.text_input(
            "Enter your email",
            help="Your email address for saving your analysis",
            key="email_input"
        )

    if st.button("Analyze My Rent"):
        if address and zip_code and current_rent and name and email:
            with st.spinner("Analyzing your rent..."):
                # Calculate rent score
                rent_score = calculate_rent_score(current_rent, zip_code)

                # Get market insights
                market_data = get_market_insights(zip_code)
                market_rate = market_data.get('avg_rent', current_rent)

                # Save search data
                try:
                    save_search_data(name, email, address, zip_code, current_rent, market_rate, rent_score)
                except Exception as e:
                    st.warning(f"Unable to save search data: {str(e)}")

                # Get comparable units and violations
                comps = get_comparable_units(zip_code, current_rent)
                violations = get_building_violations(address)

                # Display Results
                st.header("📊 Rent Analysis Results")

                # Metrics
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Rent Score", f"{rent_score:.0f}/100")
                with col2:
                    difference = market_rate - current_rent
                    st.metric(
                        "Market Rate",
                        f"${market_rate:,.0f}",
                        delta=f"${abs(difference):,.0f} {'below' if difference < 0 else 'above'} your rent"
                    )
                with col3:
                    st.metric("Vacancy Rate", f"{market_data.get('vacancy_rate', 0)*100:.1f}%")

                # Charts
                st.subheader("Rent Comparison")
                fig = create_rent_comparison_chart(current_rent, market_rate, comps)
                st.plotly_chart(fig, use_container_width=True)

                if market_data and market_data.get('seasonal_patterns'):
                    st.subheader("Market Trends")
                    trend_fig = create_trend_chart(market_data)
                    st.plotly_chart(trend_fig, use_container_width=True)

                # Comparable Units
                st.subheader("📍 Nearby Comparable Units")
                for comp in comps[:3]:
                    st.write(f"- {comp['address']}: ${comp['rent']:,.0f}/month")

                # Building Issues
                if violations:
                    st.subheader("🏗️ Building Issues")
                    for violation in violations:
                        st.write(f"- {violation['type']}: {violation['description']}")

                # Negotiation Letter
                st.header("📝 Negotiation Letter")
                letter = generate_negotiation_letter(
                    name, address, current_rent, market_rate, violations, comps
                )
                st.text_area("Your customized negotiation letter:", letter, height=400)

                # Email Button
                email_subject = urllib.parse.quote("Rent Negotiation Request")
                email_body = urllib.parse.quote(letter)
                email_link = f"mailto:?subject={email_subject}&body={email_body}"

                st.markdown(
                    f'<a href="{email_link}" target="_blank">'
                    '<button style="background-color: #FF4B4B; color: white; '
                    'padding: 10px 24px; border: none; border-radius: 4px; '
                    'cursor: pointer;">✉️ Send via Email</button></a>',
                    unsafe_allow_html=True
                )

                # Tenant Rights
                st.header("⚖️ Know Your Rights")
                for right in get_tenant_rights():
                    st.write(f"- {right}")
        else:
            st.error("Please fill in all required fields")

if __name__ == "__main__":
    analyze_rent()