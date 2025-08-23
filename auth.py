import streamlit as st
import hashlib
import json
import os

# Simple file-based user storage (in production, use a proper database)
USERS_FILE = "users.json"

def load_users():
    """Load users from JSON file"""
    if os.path.exists(USERS_FILE):
        try:
            with open(USERS_FILE, 'r') as f:
                return json.load(f)
        except:
            return {}
    return {}

def save_users(users):
    """Save users to JSON file"""
    with open(USERS_FILE, 'w') as f:
        json.dump(users, f)

def hash_password(password):
    """Hash password using SHA256"""
    return hashlib.sha256(password.encode()).hexdigest()

def create_user(name, email, password):
    """Create a new user"""
    users = load_users()
    if email in users:
        return False, "User already exists"
    
    users[email] = {
        'name': name,
        'password': hash_password(password)
    }
    save_users(users)
    return True, "Account created successfully"

def authenticate_user(email, password):
    """Authenticate user credentials"""
    users = load_users()
    if email in users and users[email]['password'] == hash_password(password):
        return True, users[email]['name']
    return False, "Invalid credentials"

def show_login_page():
    """Display the login/registration page"""
    
    # Title with custom styling
    st.markdown("""
        <div class="main-title">
            <h1>ProFileMatch</h1>
            <h2>AI Resume & Job Matcher</h2>
        </div>
    """, unsafe_allow_html=True)
    
    # Create container for the login/registration section
    st.markdown("""
        <div class="login-container">
        </div>
    """, unsafe_allow_html=True)
    
    # Create tabs for login and registration
    login_tab, register_tab = st.tabs(["🔐 Login", "📝 Create Account"])
    
    with login_tab:
        st.markdown("""
            <div style="text-align: center; margin: 2rem 0;">
                <h3 style="color: #ffffff; font-size: 1.8rem; margin-bottom: 2rem;">Welcome Back</h3>
            </div>
        """, unsafe_allow_html=True)
        
        # Create columns for centering
        col1, col2, col3 = st.columns([1, 3, 1])
        
        with col2:
            with st.form("login_form"):
                st.markdown("<div style='margin-bottom: 1.5rem;'></div>", unsafe_allow_html=True)
                email = st.text_input("📧 Email", placeholder="Enter your email", label_visibility="collapsed")
                st.markdown("<div style='margin-bottom: 1rem;'></div>", unsafe_allow_html=True)
                password = st.text_input("🔒 Password", type="password", placeholder="Enter your password", label_visibility="collapsed")
                
                # Add spacing before button
                st.markdown("<div style='margin: 2rem 0;'></div>", unsafe_allow_html=True)
                
                # Centered login button at bottom
                login_button = st.form_submit_button("🚀 Login", use_container_width=True, type="primary")
                
                if login_button:
                    if email and password:
                        success, result = authenticate_user(email, password)
                        if success:
                            st.session_state.authenticated = True
                            st.session_state.user_data = {'name': result, 'email': email}
                            st.session_state.current_page = 'upload'
                            st.success(f"Welcome back, {result}!")
                            st.rerun()
                        else:
                            st.error(result)
                    else:
                        st.error("Please fill in all fields")
    
    with register_tab:
        st.markdown("""
            <div style="text-align: center; margin: 2rem 0;">
                <h3 style="color: #ffffff; font-size: 1.8rem; margin-bottom: 2rem;">Create New Account</h3>
            </div>
        """, unsafe_allow_html=True)
        
        # Create columns for centering
        col1, col2, col3 = st.columns([1, 3, 1])
        
        with col2:
            with st.form("register_form"):
                st.markdown("<div style='margin-bottom: 1.5rem;'></div>", unsafe_allow_html=True)
                name = st.text_input("👤 Full Name", placeholder="Enter your full name", label_visibility="collapsed")
                st.markdown("<div style='margin-bottom: 1rem;'></div>", unsafe_allow_html=True)
                email = st.text_input("📧 Email", placeholder="Enter your email", label_visibility="collapsed")
                st.markdown("<div style='margin-bottom: 1rem;'></div>", unsafe_allow_html=True)
                password = st.text_input("🔒 Password", type="password", placeholder="Create a password", label_visibility="collapsed")
                st.markdown("<div style='margin-bottom: 1rem;'></div>", unsafe_allow_html=True)
                confirm_password = st.text_input("🔒 Confirm Password", type="password", placeholder="Confirm your password", label_visibility="collapsed")
                
                # Add spacing before button
                st.markdown("<div style='margin: 2rem 0;'></div>", unsafe_allow_html=True)
                
                # Centered register button at bottom
                register_button = st.form_submit_button("✨ Create Account", use_container_width=True, type="primary")
                
                if register_button:
                    if name and email and password and confirm_password:
                        if password != confirm_password:
                            st.error("Passwords don't match")
                        elif len(password) < 6:
                            st.error("Password must be at least 6 characters long")
                        else:
                            success, result = create_user(name, email, password)
                            if success:
                                st.success("Account created successfully! Please login.")
                            else:
                                st.error(result)
                    else:
                        st.error("Please fill in all fields")

def check_authentication():
    """Check if user is authenticated"""
    return st.session_state.authenticated

def logout():
    """Logout user"""
    st.session_state.authenticated = False
    st.session_state.user_data = {}
    st.session_state.current_page = 'login'
    st.session_state.analysis_results = {}
    st.rerun()
