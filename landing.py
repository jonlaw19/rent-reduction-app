import streamlit as st
import streamlit.components.v1 as components

# Must be the first Streamlit command
st.set_page_config(
    page_title="RentNinja",
    page_icon=None,
    layout="wide"
)

def show_landing_page():
    # Custom CSS for styling
    st.markdown("""
        <style>
        .section {
            padding: 4rem 0;
            margin: 2rem 0;
        }
        .section-alt {
            background-color: #f8f9fa;
            padding: 4rem 0;
            margin: 2rem 0;
            border-radius: 12px;
        }
        .feature-card {
            background: white;
            padding: 2rem;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            height: 100%;
            margin: 1rem 0;
            transition: transform 0.2s;
        }
        .feature-card:hover {
            transform: translateY(-5px);
        }
        .testimonial-card {
            background: white;
            padding: 2rem;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            margin: 1.5rem 0;
        }
        .testimonial-text {
            font-style: italic;
            font-size: 1.1rem;
            line-height: 1.6;
            margin-bottom: 1.5rem;
            color: #333;
        }
        .testimonial-author {
            font-weight: 600;
            margin-bottom: 0.3rem;
        }
        .testimonial-location {
            color: #666;
            font-size: 0.9rem;
        }
        .hero-title {
            font-size: 4rem;
            font-weight: 800;
            margin-bottom: 1.5rem;
            line-height: 1.2;
        }
        .hero-subtitle {
            font-size: 1.5rem;
            color: #666;
            margin-bottom: 3rem;
            line-height: 1.4;
        }
        .nav-container {
            padding: 1rem 0;
            margin-bottom: 2rem;
            border-bottom: 1px solid #eee;
        }
        .counter-section {
            background: linear-gradient(45deg, #FF4B4B, #FF6B6B);
            color: white;
            padding: 3rem 0;
            margin: 3rem 0;
            border-radius: 12px;
        }
        .counter-value {
            font-size: 3.5rem;
            font-weight: 700;
            margin-bottom: 0.5rem;
        }
        .counter-label {
            font-size: 1.2rem;
            opacity: 0.9;
        }
        .cta-section {
            text-align: center;
            padding: 5rem 0;
            background: #f8f9fa;
            border-radius: 12px;
            margin: 4rem 0;
        }
        .cta-title {
            font-size: 2.5rem;
            font-weight: 700;
            margin-bottom: 1.5rem;
        }
        .cta-subtitle {
            font-size: 1.3rem;
            color: #666;
            margin-bottom: 2.5rem;
        }
        </style>
    """, unsafe_allow_html=True)

    # Navigation
    with st.container():
        st.markdown('<div class="nav-container">', unsafe_allow_html=True)
        cols = st.columns([3, 6, 3])
        with cols[0]:
            st.markdown('<h1 style="margin: 0; font-size: 1.5rem;">RentNinja</h1>', unsafe_allow_html=True)
        with cols[2]:
            if 'user' in st.session_state:
                if st.button("Logout"):
                    del st.session_state['user']
                    st.switch_page("home.py")
            else:
                if st.button("Login/Sign Up"):
                    st.switch_page("pages/login.py")
        st.markdown('</div>', unsafe_allow_html=True)

    # Hero Section
    st.markdown("""
        <div style="text-align: center; padding: 4rem 0;">
            <h1 class="hero-title">Stop Overpaying for Rent</h1>
            <p class="hero-subtitle">
                Join our community of smart renters and start saving today.<br>
                Data-driven insights to help you negotiate better rates.
            </p>
        </div>
    """, unsafe_allow_html=True)

    # Counter Section
    st.markdown("""
        <div class="counter-section">
            <div style="text-align: center;">
                <div class="counter-value" id="savings-counter">$342,191</div>
                <div class="counter-label">Total Savings Generated</div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # Features Section
    st.markdown('<div class="section-alt">', unsafe_allow_html=True)
    st.markdown('<h2 style="text-align: center; margin-bottom: 3rem;">How RentNinja Works</h2>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
            <div class="feature-card">
                <h3 style="margin-bottom: 1.5rem;">Market Analysis</h3>
                <ul style="padding-left: 1.2rem;">
                    <li style="margin-bottom: 0.8rem;">Compare your rent to local averages</li>
                    <li style="margin-bottom: 0.8rem;">View historical pricing trends</li>
                    <li style="margin-bottom: 0.8rem;">Find similar properties nearby</li>
                </ul>
            </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
            <div class="feature-card">
                <h3 style="margin-bottom: 1.5rem;">Professional Letters</h3>
                <ul style="padding-left: 1.2rem;">
                    <li style="margin-bottom: 0.8rem;">Get custom negotiation letters</li>
                    <li style="margin-bottom: 0.8rem;">Leverage data-backed arguments</li>
                    <li style="margin-bottom: 0.8rem;">Send directly to your landlord</li>
                </ul>
            </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
            <div class="feature-card">
                <h3 style="margin-bottom: 1.5rem;">Know Your Rights</h3>
                <ul style="padding-left: 1.2rem;">
                    <li style="margin-bottom: 0.8rem;">Access tenant rights info</li>
                    <li style="margin-bottom: 0.8rem;">Check building violations</li>
                    <li style="margin-bottom: 0.8rem;">Get negotiation leverage</li>
                </ul>
            </div>
        """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Testimonials Section
    st.markdown('<div class="section">', unsafe_allow_html=True)
    st.markdown('<h2 style="text-align: center; margin-bottom: 3rem;">What Our Users Say</h2>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
            <div class="testimonial-card">
                <p class="testimonial-text">
                    "RentNinja helped me negotiate a $200 monthly reduction in my rent. 
                    The market data and professional letter made all the difference in my negotiation."
                </p>
                <div class="testimonial-author">Sarah M.</div>
                <div class="testimonial-location">New York, NY</div>
            </div>
        """, unsafe_allow_html=True)

        st.markdown("""
            <div class="testimonial-card">
                <p class="testimonial-text">
                    "The building violation checker revealed issues I wasn't aware of. 
                    Used this information to negotiate necessary repairs along with a rent freeze."
                </p>
                <div class="testimonial-author">David L.</div>
                <div class="testimonial-location">Chicago, IL</div>
            </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
            <div class="testimonial-card">
                <p class="testimonial-text">
                    "I was amazed by how easy it was to use. The market insights gave me 
                    the confidence to negotiate, and I ended up saving over $3,000 annually!"
                </p>
                <div class="testimonial-author">Michael R.</div>
                <div class="testimonial-location">San Francisco, CA</div>
            </div>
        """, unsafe_allow_html=True)

        st.markdown("""
            <div class="testimonial-card">
                <p class="testimonial-text">
                    "The seasonal trends data helped me time my lease renewal perfectly. 
                    Saved $150 per month just by negotiating at the right time!"
                </p>
                <div class="testimonial-author">Jessica W.</div>
                <div class="testimonial-location">Austin, TX</div>
            </div>
        """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Call to Action Section
    st.markdown("""
        <div class="cta-section">
            <h2 class="cta-title">Ready to Start Saving?</h2>
            <p class="cta-subtitle">
                Join thousands of smart renters already saving money with RentNinja.<br>
                Get your personalized rent analysis in minutes.
            </p>
        </div>
    """, unsafe_allow_html=True)

    # Custom button styling
    st.markdown("""
        <style>
        div[data-testid="stButton"] button {
            font-size: 1.3rem !important;
            padding: 1rem 2rem !important;
            height: auto !important;
            background-color: #FF4B4B !important;
            border: none !important;
            transition: all 0.3s ease !important;
        }
        div[data-testid="stButton"] button:hover {
            transform: translateY(-2px) !important;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1) !important;
        }
        </style>
    """, unsafe_allow_html=True)

    if st.button("Start Your Rent Analysis", type="primary", use_container_width=True):
        if 'user' in st.session_state:
            st.switch_page("pages/analysis.py")
        else:
            st.warning("Please login or sign up to use this feature")
            st.switch_page("pages/login.py")

if __name__ == "__main__":
    show_landing_page()