import streamlit as st

def apply_custom_styles():
    """Apply custom CSS styles for the ProFileMatch application"""
    
    st.markdown("""
    <style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Global Styles */
    .main {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
        color: white;
        font-family: 'Inter', sans-serif;
        min-height: 100vh;
    }
    
    /* Rich dark backgrounds */
    .stApp {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
    }
    
    /* Hide Streamlit branding and elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stDeployButton {visibility: hidden;}
    .stDecoration {visibility: hidden;}
    div[data-testid="stToolbar"] {visibility: hidden;}
    div[data-testid="stDecoration"] {visibility: hidden;}
    div[data-testid="stStatusWidget"] {visibility: hidden;}
    .stActionButton {visibility: hidden;}
    
    /* Main title styling */
    .main-title {
        text-align: center;
        padding: 3rem 0;
        margin-bottom: 3rem;
        background: rgba(26, 26, 46, 0.8);
        backdrop-filter: blur(15px);
        border-radius: 20px;
        margin: 2rem 0;
        box-shadow: 0 8px 32px rgba(15, 52, 96, 0.6);
        border: 1px solid #3498db;
    }
    
    .main-title h1 {
        font-size: 4rem;
        font-weight: 700;
        background: linear-gradient(135deg, #3498db 0%, #2ecc71 50%, #f39c12 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 0.5rem;
        text-shadow: 0 4px 8px rgba(15, 52, 96, 0.8);
        animation: glow 3s ease-in-out infinite alternate;
    }
    
    .main-title h2 {
        font-size: 1.8rem;
        color: #ecf0f1;
        font-weight: 400;
        margin: 0;
        text-shadow: 0 2px 4px rgba(15, 52, 96, 0.6);
    }
    
    @keyframes glow {
        from { text-shadow: 0 0 20px rgba(52, 152, 219, 0.4); }
        to { text-shadow: 0 0 30px rgba(46, 204, 113, 0.6); }
    }
    
    /* Page title styling */
    .page-title {
        font-size: 2.5rem;
        font-weight: 600;
        color: #ffffff;
        text-align: center;
        margin-bottom: 1rem;
    }
    
    /* Custom button styling */
    .stButton > button {
        background: linear-gradient(135deg, #2c3e50 0%, #34495e 100%);
        color: #ecf0f1;
        border: 2px solid #3498db;
        border-radius: 12px;
        padding: 0.9rem 2.5rem;
        font-weight: 600;
        font-family: 'Inter', sans-serif;
        font-size: 1.1rem;
        transition: all 0.3s ease;
        box-shadow: 0 8px 25px rgba(52, 152, 219, 0.3);
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, #34495e 0%, #2c3e50 100%);
        border-color: #5dade2;
        transform: translateY(-3px);
        box-shadow: 0 12px 35px rgba(52, 152, 219, 0.5);
        color: #ffffff;
    }
    
    .stButton > button:active {
        transform: translateY(-1px);
    }
    
    /* Primary button styling */
    .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #e74c3c 0%, #c0392b 100%);
        border: 2px solid #e74c3c;
        box-shadow: 0 8px 25px rgba(231, 76, 60, 0.4);
        color: white;
    }
    
    .stButton > button[kind="primary"]:hover {
        background: linear-gradient(135deg, #c0392b 0%, #a93226 100%);
        border-color: #ec7063;
        box-shadow: 0 12px 35px rgba(231, 76, 60, 0.6);
    }
    
    /* Form styling */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea,
    .stSelectbox > div > div > select {
        background: rgba(44, 62, 80, 0.9);
        backdrop-filter: blur(10px);
        border: 2px solid #3498db;
        border-radius: 12px;
        color: #ffffff;
        font-family: 'Inter', sans-serif;
        padding: 0.8rem 1rem;
        font-size: 1rem;
        font-weight: 500;
    }
    
    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus,
    .stSelectbox > div > div > select:focus {
        border-color: #3498db;
        box-shadow: 0 0 0 3px rgba(52, 152, 219, 0.3);
        background: rgba(52, 73, 94, 0.9);
    }
    
    /* Login form container */
    .login-container {
        background: rgba(22, 33, 62, 0.9);
        backdrop-filter: blur(15px);
        border-radius: 20px;
        padding: 2rem;
        margin: 1rem 0;
        box-shadow: 0 8px 32px rgba(15, 52, 96, 0.6);
        border: 1px solid #2c3e50;
    }
    
    /* File uploader styling */
    .stFileUploader > div {
        background: linear-gradient(135deg, #2c3e50, #34495e);
        border: 2px dashed #3498db;
        border-radius: 15px;
        padding: 2rem;
        text-align: center;
        transition: all 0.3s ease;
    }
    
    .stFileUploader > div:hover {
        border-color: #5dade2;
        background: linear-gradient(135deg, #34495e, #2c3e50);
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(52, 152, 219, 0.3);
    }
    
    /* File uploader text */
    .stFileUploader label {
        color: #ffffff !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
    }
    
    .stFileUploader small {
        color: #e8e8e8 !important;
        font-weight: 500 !important;
    }
    
    /* Tab styling */
    .stTabs > div > div > div > div {
        background: rgba(44, 62, 80, 0.8);
        backdrop-filter: blur(10px);
        border-radius: 15px 15px 0 0;
        border: 1px solid #2c3e50;
    }
    
    .stTabs > div > div > div > div > div {
        color: #ffffff;
        font-weight: 600;
        font-size: 1.1rem;
    }
    
    /* Active tab styling */
    .stTabs > div > div > div > div[data-baseweb="tab"][aria-selected="true"] {
        background: linear-gradient(135deg, #34495e 0%, #2c3e50 100%);
        border: 2px solid #3498db;
        color: white;
    }
    
    /* Enhanced File Upload Styling */
    .uploadedFile {
        background: linear-gradient(135deg, #2c3e50, #34495e);
        border: 2px dashed #3498db;
        border-radius: 15px;
        padding: 2rem;
        text-align: center;
        transition: all 0.3s ease;
        margin: 1rem 0;
    }
    
    .uploadedFile:hover {
        border-color: #5dade2;
        background: linear-gradient(135deg, #34495e, #2c3e50);
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(52, 152, 219, 0.3);
    }
    
    
    /* Progress Bar Styling */
    .progress-container {
        background: rgba(44, 62, 80, 0.8);
        border-radius: 10px;
        padding: 1rem;
        margin: 1rem 0;
        border: 1px solid #3498db;
    }
    
    .progress-bar {
        width: 100%;
        height: 20px;
        background: #2c3e50;
        border-radius: 10px;
        overflow: hidden;
        margin: 0.5rem 0;
    }
    
    .progress-fill {
        height: 100%;
        background: linear-gradient(135deg, #3498db, #2ecc71);
        border-radius: 10px;
        transition: width 0.5s ease;
        animation: shimmer 2s infinite;
    }
    
    @keyframes shimmer {
        0% { background-position: -200px 0; }
        100% { background-position: calc(200px + 100%) 0; }
    }
    
    /* Upload Zone Animation */
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.02); }
        100% { transform: scale(1); }
    }
    
    .upload-zone {
        animation: pulse 3s ease-in-out infinite;
    }
    
    /* Success Animation */
    @keyframes checkmark {
        0% { transform: scale(0); }
        50% { transform: scale(1.2); }
        100% { transform: scale(1); }
    }
    
    .success-check {
        animation: checkmark 0.6s ease-in-out;
    }
    
    /* Metric styling */
    .stMetric {
        background-color: #2D2D2D;
        padding: 1rem;
        border-radius: 8px;
        border: 1px solid #404040;
    }
    
    /* Success/Error message styling */
    .stSuccess {
        background-color: rgba(76, 175, 80, 0.1);
        border: 1px solid #4CAF50;
        color: #4CAF50;
    }
    
    .stError {
        background-color: rgba(255, 87, 34, 0.1);
        border: 1px solid #FF5722;
        color: #FF5722;
    }
    
    .stWarning {
        background-color: rgba(255, 193, 7, 0.1);
        border: 1px solid #FFC107;
        color: #FFC107;
    }
    
    /* Card styling for results */
    .result-card {
        background: linear-gradient(135deg, #2D2D2D, #1E1E1E);
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
        border: 1px solid #404040;
        box-shadow: 0 4px 12px rgba(0,0,0,0.3);
    }
    
    /* Progress bar styling */
    .stProgress > div > div > div > div {
        background: linear-gradient(135deg, #C0C0C0, #A0A0A0);
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background-color: #1E1E1E;
    }
    
    /* Custom scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: #1E1E1E;
    }
    
    ::-webkit-scrollbar-thumb {
        background: #C0C0C0;
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: #D0D0D0;
    }
    
    /* Loading spinner styling */
    .stSpinner > div {
        border-color: #C0C0C0;
    }
    
    /* Plotly chart styling */
    .js-plotly-plot {
        background-color: transparent !important;
    }
    
    /* Skills list styling */
    .skill-item {
        background: #2D2D2D;
        padding: 0.5rem 1rem;
        border-radius: 6px;
        margin: 0.25rem 0;
        border-left: 3px solid #C0C0C0;
    }
    
    /* YouTube recommendation card */
    .youtube-card {
        background: linear-gradient(135deg, #2D2D2D, #1E1E1E);
        border-radius: 10px;
        padding: 1rem;
        margin: 0.5rem;
        border: 1px solid #404040;
        transition: all 0.3s ease;
    }
    
    .youtube-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 16px rgba(0,0,0,0.4);
    }
    
    /* Responsive design */
    @media (max-width: 768px) {
        .main-title h1 {
            font-size: 2.5rem;
        }
        
        .main-title h2 {
            font-size: 1.2rem;
        }
        
        .page-title {
            font-size: 2rem;
        }
        
        .stButton > button {
            padding: 0.5rem 1rem;
        }
    }
    </style>
    """, unsafe_allow_html=True)
