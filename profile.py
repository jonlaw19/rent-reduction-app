import streamlit as st
from database.session import get_session
from database.models import User, RentSearch # Added RentSearch import
from datetime import datetime

def update_user_profile(user_id, name=None, email=None, password=None):
    """Update user profile information"""
    session = get_session()
    try:
        user = session.query(User).filter(User.id == user_id).first()
        if user:
            if name:
                user.name = name
            if email:
                user.email = email
            if password:
                user.password_hash = hashlib.sha256(password.encode()).hexdigest()
            session.commit()
            return True
    except Exception as e:
        st.error(f"Error updating profile: {str(e)}")
        return False
    finally:
        session.close()

def show_profile():
    st.title("👤 My Profile")

    if 'user' not in st.session_state:
        st.warning("Please login to view your profile")
        st.button("Go to Login", on_click=lambda: st.switch_page("pages/login.py"))
        return

    user_id = st.session_state['user']['id']
    session = get_session()

    try:
        user = session.query(User).filter(User.id == user_id).first()
        if not user:
            st.error("User not found")
            return

        st.subheader("Account Information")

        # User Stats - only keep essential information
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Member Since", user.created_at.strftime("%B %d, %Y"))
        with col2:
            # Get fresh count of searches from database
            search_count = session.query(RentSearch).filter(RentSearch.user_id == user_id).count()
            st.metric("Total Searches", search_count)

        # Profile Form
        with st.form("profile_form"):
            name = st.text_input("Name", value=user.name)
            email = st.text_input("Email", value=user.email)
            new_password = st.text_input("New Password (leave blank to keep current)", type="password")
            confirm_password = st.text_input("Confirm New Password", type="password")

            if st.form_submit_button("Update Profile"):
                if new_password:
                    if new_password != confirm_password:
                        st.error("Passwords do not match")
                        return
                    if len(new_password) < 6:
                        st.error("Password must be at least 6 characters")
                        return

                if update_user_profile(user_id, name, email, new_password):
                    st.session_state['user']['name'] = name
                    st.session_state['user']['email'] = email
                    st.success("Profile updated successfully!")

    finally:
        session.close()

if __name__ == "__main__":
    show_profile()