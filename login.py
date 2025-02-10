import streamlit as st
from database.models import User
from database.session import get_session
import hashlib

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def auth_user():
    st.title("👋 Welcome to RentNinja!")
    st.write("Join our community of smart renters and start saving today. Free forever.")

    # Clear any previous error messages when switching tabs
    if 'auth_error' in st.session_state:
        del st.session_state['auth_error']

    tab1, tab2 = st.tabs(["Sign In", "Create Account"])

    with tab1:
        st.subheader("Welcome Back!")

        # Login form with improved layout
        with st.form("login_form"):
            login_email = st.text_input(
                "Email",
                key="login_email",
                placeholder="your.email@example.com",
                help="Enter the email you used to register"
            )
            login_password = st.text_input(
                "Password",
                type="password",
                key="login_password",
                help="Enter your password"
            )

            submitted = st.form_submit_button("Sign In", use_container_width=True)
            if submitted and login_email and login_password:
                session = get_session()
                try:
                    user = session.query(User).filter(
                        User.email == login_email,
                        User.password_hash == hash_password(login_password)
                    ).first()

                    if user:
                        st.session_state['user'] = {
                            'id': user.id,
                            'name': user.name,
                            'email': user.email
                        }
                        st.success("Successfully signed in! Redirecting...")
                        st.switch_page("pages/analysis.py")
                    else:
                        st.error("We couldn't find an account with those credentials. Please try again.")
                except Exception as e:
                    st.error("Something went wrong. Please try again later.")
                finally:
                    session.close()
            elif submitted:
                st.error("Please fill in both email and password")

    with tab2:
        st.subheader("Create Your Account")
        st.write("Start your journey to smarter rent decisions!")

        # Registration form with improved layout
        with st.form("signup_form"):
            col1, col2 = st.columns(2)

            with col1:
                name = st.text_input(
                    "Full Name",
                    key="signup_name",
                    placeholder="John Smith",
                    help="How should we address you?"
                )

            with col2:
                email = st.text_input(
                    "Email",
                    key="signup_email",
                    placeholder="your.email@example.com",
                    help="We'll send important updates here"
                )

            password = st.text_input(
                "Password",
                type="password",
                key="signup_password",
                help="Use at least 8 characters with letters and numbers"
            )

            confirm_password = st.text_input(
                "Confirm Password",
                type="password",
                key="confirm_password",
                help="Re-enter your password"
            )

            # Password strength indicator
            if password:
                strength = 0
                checks = [
                    len(password) >= 8,
                    any(c.isupper() for c in password),
                    any(c.islower() for c in password),
                    any(c.isdigit() for c in password)
                ]
                strength = sum(checks)
                st.progress(strength/4, f"Password Strength: {['Weak', 'Fair', 'Good', 'Strong'][strength-1]}")

            submitted = st.form_submit_button("Create Account", use_container_width=True)
            if submitted:
                if all([name, email, password, confirm_password]):
                    if password != confirm_password:
                        st.error("Passwords don't match. Please try again.")
                        return

                    if len(password) < 8:
                        st.error("Password must be at least 8 characters long")
                        return

                    session = get_session()
                    try:
                        # Check if email exists
                        email_exists = session.query(User).filter(User.email == email).count() > 0
                        if email_exists:
                            st.error("This email is already registered. Try signing in instead.")
                            return

                        new_user = User(
                            name=name,
                            email=email,
                            password_hash=hash_password(password)
                        )
                        session.add(new_user)
                        session.commit()

                        st.success("🎉 Account created successfully! Please sign in to continue.")
                        # Switch to the login tab by refreshing the page
                        st.switch_page("pages/login.py")
                    except Exception as e:
                        st.error("Something went wrong. Please try again later.")
                        session.rollback()
                    finally:
                        session.close()
                else:
                    st.error("Please fill in all fields")

if __name__ == "__main__":
    auth_user()