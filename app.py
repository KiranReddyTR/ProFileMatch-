import streamlit as st
import requests
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Optional imports (safe)
try:
    import pdfplumber
except ImportError:
    pdfplumber = None

try:
    import docx2txt
except ImportError:
    docx2txt = None

try:
    from sentence_transformers import SentenceTransformer, util
except ImportError:
    st.error("sentence-transformers not installed.")

try:
    import googleapiclient.discovery
except ImportError:
    st.warning("google-api-python-client not installed.")

try:
    import spacy
    from spacy.cli import download
except ImportError:
    spacy = None

from streamlit_lottie import st_lottie
import streamlit.components.v1 as components

# -----------------------------
# Page config & dark theme
# -----------------------------
st.set_page_config(page_title="AI Resume Analyzer — Pro Edition", layout="wide")
st.markdown(
    """
    <style>
    .stApp { background: linear-gradient(180deg, #0a1121 0%, #0e1b35 100%); color: #e8ecf2; }
    .stButton>button { background: linear-gradient(90deg,#0ea5e9,#6366f1); color: white; border:none; border-radius:8px; }
    .metric-box { padding:1.5rem; border-radius:16px; background:linear-gradient(180deg, rgba(37,99,235,0.15), rgba(14,165,233,0.08)); text-align:center; }
    .skill-section { background: rgba(255,255,255,0.05); padding:1rem; border-radius:12px; }
    .pill { display:inline-block; padding:8px 12px; border-radius:999px; background:rgba(255,255,255,0.08); margin:5px; font-size:14px; }
    .card { padding: 1rem; border-radius: 12px; background: rgba(255,255,255,0.03); box-shadow: 0 6px 18px rgba(0,0,0,0.3); }
    </style>
    """, unsafe_allow_html=True
)

# -----------------------------
# NLP Model
# -----------------------------
if spacy:
    model_name = "en_core_web_md"
    try:
        nlp = spacy.load(model_name)
    except OSError:
        download(model_name)
        nlp = spacy.load(model_name)

st_model = SentenceTransformer('all-MiniLM-L6-v2')

# -----------------------------
# YouTube API
# -----------------------------
YOUTUBE_API_KEY = "YOUR_YOUTUBE_API_KEY"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

# -----------------------------
# Session state
# -----------------------------
if "skills_analyzed" not in st.session_state:
    st.session_state.update({
        "skills_analyzed": False,
        "show_courses": False,
        "missing_skills": [],
        "matching_score": 0.0,
        "resume_skills": [],
        "job_skills": [],
        "resume_text": "",
        "job_text": "",
    })

# -----------------------------
# Helper functions
# -----------------------------
def fetch_youtube_courses(skill):
    try:
        youtube = googleapiclient.discovery.build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=YOUTUBE_API_KEY)
        request = youtube.search().list(q=f"{skill} course", part="snippet", maxResults=6, type="video")
        response = request.execute()
        return [
            {
                "Title": item["snippet"]["title"],
                "Channel": item["snippet"]["channelTitle"],
                "Video Link": f'https://www.youtube.com/watch?v={item["id"]["videoId"]}',
                "Thumbnail": item["snippet"]["thumbnails"].get("medium", {}).get("url", "")
            }
            for item in response.get("items", [])
        ]
    except:
        return []

def extract_text(uploaded_file):
    if uploaded_file:
        ext = uploaded_file.name.split(".")[-1].lower()
        if ext == "pdf":
            if pdfplumber:
                with pdfplumber.open(uploaded_file) as pdf:
                    return "\n".join([page.extract_text() for page in pdf.pages if page.extract_text()]) or "No text extracted."
            else:
                return "PDF extraction requires pdfplumber, not installed."
        elif ext in ["docx", "doc"]:
            if docx2txt:
                return docx2txt.process(uploaded_file) or "No text extracted."
            else:
                return "DOCX extraction requires docx2txt, not installed."
        elif ext == "txt":
            return uploaded_file.read().decode("utf-8") or "No text extracted."
    return "No text extracted."

def generate_summary(text):
    sentences = text.split(". ")[:3]
    return "... ".join(sentences) + "..." if sentences else "No content extracted."

def extract_skills(text):
    if spacy:
        doc = nlp(text)
        skills = set()
        for ent in doc.ents:
            if ent.label_ == "ORG":
                skills.add(ent.text)
        return list(skills)
    return []

def calculate_matching_score(resume_text, job_text):
    embeddings = st_model.encode([resume_text, job_text], convert_to_tensor=True)
    return round(float(util.pytorch_cos_sim(embeddings[0], embeddings[1])[0]), 2) * 100

def plot_skill_distribution_pie(resume_skills, job_skills):
    resume_labels = list(resume_skills) if resume_skills else ["No Skills Found"]
    resume_sizes = [1] * len(resume_skills) if resume_skills else [1]
    job_labels = list(job_skills) if job_skills else ["No Skills Found"]
    job_sizes = [1] * len(job_skills) if job_skills else [1]
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    axes[0].pie(resume_sizes, labels=resume_labels, autopct='%1.1f%%', startangle=90)
    axes[0].set_title("Resume Skills")
    axes[1].pie(job_sizes, labels=job_labels, autopct='%1.1f%%', startangle=90)
    axes[1].set_title("Job Skills")
    st.pyplot(fig)

def load_lottie_url(url: str):
    try:
        r = requests.get(url)
        if r.status_code == 200:
            return r.json()
    except:
        return None
    return None

LOTTIE_UPLOAD = load_lottie_url("https://assets2.lottiefiles.com/packages/lf20_w51pcehl.json")
LOTTIE_SCORE = load_lottie_url("https://assets6.lottiefiles.com/packages/lf20_g8n0xqbm.json")

# -----------------------------
# Navigation
# -----------------------------
page = st.sidebar.radio("📂 Navigate", ["📄 Upload Documents", "📝 Summaries", "🧠 Analysis", "📊 Insights & Courses"])

if st.sidebar.button("Reset All"):
    for k in list(st.session_state.keys()):
        del st.session_state[k]
    st.experimental_rerun()

# --- Pages implementation (same as before) ---
# Upload, Summaries, Analysis, Insights & Courses
# [Use the same code logic from your last working version]

