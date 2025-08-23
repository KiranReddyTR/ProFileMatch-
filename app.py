import streamlit as st
import os
from auth import show_login_page, check_authentication
from file_processor import show_upload_page
from ai_analyzer import show_results_page
from database import show_saved_results_page
from styles import apply_custom_styles

# Page configuration
st.set_page_config(
    page_title="ProFileMatch - AI Resume & Job Matcher",
    page_icon="📄",
    layout="centered",
    initial_sidebar_state="collapsed",
    menu_items={
        'Get Help': None,
        'Report a bug': None,
        'About': None
    }
)

# Apply custom styles
apply_custom_styles()

# Initialize session state
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'current_page' not in st.session_state:
    st.session_state.current_page = 'login'
if 'user_data' not in st.session_state:
    st.session_state.user_data = {}
if 'analysis_results' not in st.session_state:
    st.session_state.analysis_results = {}
if 'saved_results' not in st.session_state:
    st.session_state.saved_results = []

def main():
    # Navigation logic
    if not st.session_state.authenticated:
        # Force user to login page if not authenticated
        st.session_state.current_page = 'login'
        show_login_page()
    else:
        # Show navigation based on current page
        if st.session_state.current_page == 'upload':
            show_upload_page()
        elif st.session_state.current_page == 'results':
            show_results_page()
        elif st.session_state.current_page == 'saved_results':
            show_saved_results_page()
        else:
            # Default to upload page after login
            st.session_state.current_page = 'upload'
            show_upload_page()

if __name__ == "__main__":
    main()
