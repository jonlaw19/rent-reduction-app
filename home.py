import streamlit as st
import streamlit.components.v1 as components

# Must be the first Streamlit command
st.set_page_config(
    page_title="RentNinja",
    page_icon=None,
    layout="wide"
)

def logout():
    if 'user' in st.session_state:
        del st.session_state['user']
        st.switch_page("home.py")

def show_home_page():
    # Custom CSS for the title
    st.markdown("""
        <style>
        .title-container {
            display: flex;
            align-items: center;
            gap: 4px;
            padding: 0.5rem 0;
        }
        .title-text {
            font-size: 20px;
            font-weight: bold;
            margin: 0;
            padding: 0;
            display: inline-flex;
            align-items: center;
        }
        </style>
    """, unsafe_allow_html=True)

    # Top Navigation Bar with fixed title
    with st.container():
        cols = st.columns([3, 6, 3])
        with cols[0]:
            st.markdown(
                '<div class="title-container"><span class="title-text">RentNinja</span></div>',
                unsafe_allow_html=True
            )
        with cols[2]:
            if 'user' in st.session_state:
                if st.button("Logout"):
                    del st.session_state['user']
                    st.switch_page("home.py")
            else:
                if st.button("Login/Sign Up"):
                    st.switch_page("pages/login.py")

    # Hero Section
    st.markdown("""
        <div style="text-align: center; padding: 20px 0;">
            <h1 style="font-size: 3.5rem; font-weight: 800; margin-bottom: 1rem;">
                Stop Overpaying for Rent
            </h1>
            <p style="font-size: 1.5rem; color: #666; margin-bottom: 2rem;">
                Join our community of smart renters and start saving today, 100% free.
            </p>
        </div>
    """, unsafe_allow_html=True)

    # Savings Counter
    counter_html = """
    <div style="text-align: center; padding: 40px 0;">
        <div style="font-family: monospace; font-size: 4.5rem; font-weight: 600; color: #FF4B4B;" id="savings-counter">$342,191</div>
        <div style="font-family: system-ui; font-size: 1.5rem; color: #666; margin-top: 10px;">Saved for Customers</div>
    </div>
    """

    counter_js = """
    <script>
        let lastUpdate = Date.now();
        let currentAmount = 342191;
        const updateRate = 35;

        function formatNumber(num) {
            return '$' + num.toLocaleString('en-US');
        }

        function updateCounter() {
            const counter = document.getElementById('savings-counter');
            if (counter) {
                const now = Date.now();
                const deltaTime = (now - lastUpdate) / 1000;
                currentAmount += updateRate * deltaTime;
                counter.textContent = formatNumber(Math.floor(currentAmount));
                lastUpdate = now;
            }
            requestAnimationFrame(updateCounter);
        }

        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', updateCounter);
        } else {
            updateCounter();
        }
    </script>
    """

    # Use Streamlit components to inject the HTML and JavaScript
    components.html(counter_html + counter_js, height=200)

    # Features Section
    st.markdown("<h2 style='text-align: center; margin: 40px 0;'>How RentNinja Works</h2>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        ### Market Analysis
        - Enter your address to see how your rent compares to local averages
        - View historical pricing trends
        - Browse similar properties nearby
        """)

    with col2:
        st.markdown("""
        ### Professional Letters
        - Get a custom, data-backed negotiation letter if you're overpaying
        - Leverage market data and local insights
        - Send directly via email to your landlord
        """)

    with col3:
        st.markdown("""
        ### Know Your Rights
        - Access tenant rights information
        - Check building violations
        - Get negotiation leverage
        """)

    # Primary CTA Button
    st.markdown("""
        <style>
        div[data-testid="stButton"] button {
            font-size: 1.5rem !important;
            padding: 1rem 2rem !important;
            height: auto !important;
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
    show_home_page()