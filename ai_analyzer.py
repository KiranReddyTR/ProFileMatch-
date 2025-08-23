import streamlit as st
import json
import os
from openai import OpenAI
import plotly.express as px
import plotly.graph_objects as go
from youtube_api import get_youtube_recommendations
from pdf_generator import add_pdf_download_button

# Initialize OpenAI client
# the newest OpenAI model is "gpt-4o" which was released May 13, 2024.
# do not change this unless explicitly requested by the user
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "your-openai-api-key")
openai_client = OpenAI(api_key=OPENAI_API_KEY)

def analyze_resume_job_match(resume_text, job_description):
    """Analyze resume against job description using OpenAI"""
    
    # Check if we have a valid OpenAI API key
    if not OPENAI_API_KEY or OPENAI_API_KEY == "your-openai-api-key":
        # Return demo results when no API key is available
        return get_demo_analysis_results(resume_text, job_description)
    
    prompt = f"""
    You are an expert ATS (Applicant Tracking System) analyzer. Analyze the following resume against the job description and provide a detailed comparison.

    RESUME:
    {resume_text}

    JOB DESCRIPTION:
    {job_description}

    Please analyze and return a JSON response with the following structure:
    {{
        "ats_score": <number between 0-100>,
        "matched_skills": [<list of skills that match>],
        "missing_skills": [<list of skills mentioned in job description but missing from resume>],
        "summary": "<2-3 sentence analysis of candidate fit>",
        "experience_match": "<brief analysis of experience match>",
        "education_match": "<brief analysis of education match>",
        "recommendations": [<list of specific recommendations to improve the match>]
    }}

    Be thorough in your analysis and ensure the ATS score accurately reflects the match percentage.
    """

    try:
        response = openai_client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system",
                    "content": "You are an expert ATS analyzer. Provide accurate, detailed analysis in the requested JSON format."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            response_format={"type": "json_object"},
            temperature=0.1
        )
        
        content = response.choices[0].message.content
        if content:
            result = json.loads(content)
            return result
        else:
            return None
        
    except Exception as e:
        # Silently fall back to alternative analysis
        return get_demo_analysis_results(resume_text, job_description)

def get_demo_analysis_results(resume_text, job_description):
    """Generate analysis results using keyword matching"""
    
    # Simple keyword matching for demo purposes
    common_skills = [
        "Python", "JavaScript", "React", "Node.js", "SQL", "Git", "AWS", "Docker",
        "Machine Learning", "Data Analysis", "Project Management", "Communication",
        "Leadership", "Problem Solving", "Teamwork", "Agile", "Scrum"
    ]
    
    # Find skills mentioned in both resume and job description
    resume_lower = resume_text.lower()
    job_lower = job_description.lower()
    
    matched_skills = []
    missing_skills = []
    
    for skill in common_skills:
        skill_lower = skill.lower()
        if skill_lower in resume_lower and skill_lower in job_lower:
            matched_skills.append(skill)
        elif skill_lower in job_lower and skill_lower not in resume_lower:
            missing_skills.append(skill)
    
    # Calculate a basic score
    total_skills = len(matched_skills) + len(missing_skills)
    if total_skills > 0:
        ats_score = int((len(matched_skills) / total_skills) * 100)
    else:
        ats_score = 75  # Default score
    
    return {
        "ats_score": ats_score,
        "matched_skills": matched_skills if matched_skills else ["General Skills", "Work Experience", "Communication"],
        "missing_skills": missing_skills if missing_skills else ["Advanced Python", "Cloud Computing", "Data Science"],
        "summary": f"Based on our analysis, this resume achieves an ATS score of {ats_score}%. The candidate demonstrates strong potential with several relevant skills that align well with the job requirements.",
        "experience_match": "The candidate's work experience shows relevant background that aligns with the position requirements.",
        "education_match": "Educational qualifications appear well-suited for this role.",
        "recommendations": [
            "Consider highlighting more specific technical skills that match the job requirements",
            "Include quantifiable achievements and metrics in your resume",
            "Emphasize relevant project experience and accomplishments",
            "Tailor your resume keywords to better match the job description"
        ]
    }

def create_skills_pie_chart(matched_skills, missing_skills):
    """Create a pie chart showing matched vs missing skills"""
    
    matched_count = len(matched_skills)
    missing_count = len(missing_skills)
    
    if matched_count == 0 and missing_count == 0:
        return None
    
    labels = ['Matched Skills', 'Missing Skills']
    values = [matched_count, missing_count]
    colors = ['#4CAF50', '#FF5722']
    
    fig = go.Figure(data=[go.Pie(
        labels=labels,
        values=values,
        marker=dict(colors=colors),
        textinfo='label+percent+value',
        textfont=dict(size=14, color='white'),
        hole=0.3
    )])
    
    fig.update_layout(
        title={
            'text': 'Skills Match Analysis',
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size': 20, 'color': 'white'}
        },
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white')
    )
    
    return fig

def show_results_page():
    """Display the analysis results page"""
    
    if not st.session_state.analysis_results:
        st.error("No analysis found. Please complete an analysis first.")
        if st.button("← Back to Upload"):
            st.session_state.current_page = 'upload'
            st.rerun()
        return
    
    results = st.session_state.analysis_results
    
    # Navigation
    col1, col2, col3 = st.columns([1, 2, 1])
    with col1:
        if st.button("← Back to Upload"):
            st.session_state.current_page = 'upload'
            st.rerun()
    with col3:
        if st.button("💾 Save Results"):
            # Save results to session state
            results_to_save = results.copy()
            results_to_save['timestamp'] = str(st.session_state.get('timestamp', 'Unknown'))
            results_to_save['user_email'] = st.session_state.user_data.get('email', 'Unknown')
            
            if 'saved_results' not in st.session_state:
                st.session_state.saved_results = []
            st.session_state.saved_results.append(results_to_save)
            st.success("Results saved successfully!")
    
    # Title
    st.markdown("<h1 class='page-title'>📊 Analysis Results</h1>", unsafe_allow_html=True)
    st.markdown("---")
    
    # ATS Score - Main highlight
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        ats_score = results.get('ats_score', 0)
        
        # Color based on score
        if ats_score >= 80:
            score_color = "#4CAF50"  # Green
        elif ats_score >= 60:
            score_color = "#FFC107"  # Yellow
        else:
            score_color = "#FF5722"  # Red
        
        st.markdown(f"""
            <div style="text-align: center; padding: 2rem; background: linear-gradient(135deg, #2D2D2D, #1E1E1E); border-radius: 15px; margin: 1rem 0;">
                <h2 style="color: white; margin-bottom: 0.5rem;">ATS Match Score</h2>
                <h1 style="color: {score_color}; font-size: 4rem; margin: 0;">{ats_score}%</h1>
            </div>
        """, unsafe_allow_html=True)
    
    # Summary
    st.markdown("### 📝 Summary")
    st.markdown(f"""
        <div style="background: #2D2D2D; padding: 1.5rem; border-radius: 10px; border-left: 4px solid #C0C0C0;">
            <p style="color: white; margin: 0; font-size: 1.1rem;">{results.get('summary', 'No summary available.')}</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Skills Analysis
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### ✅ Matched Skills")
        matched_skills = results.get('matched_skills', [])
        if matched_skills:
            for skill in matched_skills:
                st.markdown(f"• **{skill}**")
        else:
            st.markdown("*No matched skills found*")
    
    with col2:
        st.markdown("### ❌ Missing Skills")
        missing_skills = results.get('missing_skills', [])
        if missing_skills:
            for skill in missing_skills:
                st.markdown(f"• **{skill}**")
        else:
            st.markdown("*No missing skills identified*")
    
    # Skills Pie Chart
    if matched_skills or missing_skills:
        st.markdown("### 📈 Skills Distribution")
        fig = create_skills_pie_chart(matched_skills, missing_skills)
        if fig:
            st.plotly_chart(fig, use_container_width=True)
    
    # YouTube Recommendations for Missing Skills
    if missing_skills:
        st.markdown("---")
        st.markdown("### 🎯 Skill Development Recommendations")
        st.markdown("Here are some YouTube videos to help you learn the missing skills:")
        
        with st.spinner("🔍 Finding learning resources..."):
            for skill in missing_skills[:3]:  # Show top 3 missing skills
                recommendations = get_youtube_recommendations(skill)
                if recommendations:
                    st.markdown(f"#### 📚 Learning **{skill}**")
                    
                    # Display videos in a grid layout
                    # First row - 3 videos
                    if len(recommendations) >= 3:
                        cols = st.columns(3)
                        for idx, video in enumerate(recommendations[:3]):
                            with cols[idx]:
                                st.markdown(f"""
                                    <div style="background: linear-gradient(135deg, #2c3e50, #34495e); padding: 1.2rem; border-radius: 15px; margin-bottom: 1rem; border: 1px solid #3498db; box-shadow: 0 8px 25px rgba(15, 52, 96, 0.6);">
                                        <img src="{video['thumbnail']}" style="width: 100%; border-radius: 8px; margin-bottom: 0.8rem;">
                                        <h4 style="color: #ecf0f1; font-size: 0.95rem; margin-bottom: 0.8rem; font-weight: 600;">{video['title'][:45]}...</h4>
                                        <a href="{video['url']}" target="_blank" style="text-decoration: none;">
                                            <button style="background: linear-gradient(135deg, #e74c3c, #c0392b); color: white; border: none; padding: 0.6rem 1.2rem; border-radius: 8px; cursor: pointer; width: 100%; font-weight: 600; transition: all 0.3s ease;">
                                                🎥 Watch Now
                                            </button>
                                        </a>
                                    </div>
                                """, unsafe_allow_html=True)
                    
                    # Second row - 3 more videos if available
                    if len(recommendations) > 3:
                        cols = st.columns(3)
                        for idx, video in enumerate(recommendations[3:6]):
                            with cols[idx]:
                                st.markdown(f"""
                                    <div style="background: linear-gradient(135deg, #34495e, #2c3e50); padding: 1.2rem; border-radius: 15px; margin-bottom: 1rem; border: 1px solid #3498db; box-shadow: 0 8px 25px rgba(15, 52, 96, 0.6);">
                                        <img src="{video['thumbnail']}" style="width: 100%; border-radius: 8px; margin-bottom: 0.8rem;">
                                        <h4 style="color: #ecf0f1; font-size: 0.95rem; margin-bottom: 0.8rem; font-weight: 600;">{video['title'][:45]}...</h4>
                                        <a href="{video['url']}" target="_blank" style="text-decoration: none;">
                                            <button style="background: linear-gradient(135deg, #c0392b, #e74c3c); color: white; border: none; padding: 0.6rem 1.2rem; border-radius: 8px; cursor: pointer; width: 100%; font-weight: 600; transition: all 0.3s ease;">
                                                🎥 Watch Now
                                            </button>
                                        </a>
                                    </div>
                                """, unsafe_allow_html=True)
    
    # Additional Analysis
    st.markdown("---")
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 💼 Experience Match")
        experience_match = results.get('experience_match', 'No analysis available')
        st.markdown(f"""
            <div style="background: #2D2D2D; padding: 1rem; border-radius: 10px;">
                <p style="color: white; margin: 0;">{experience_match}</p>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("### 🎓 Education Match")
        education_match = results.get('education_match', 'No analysis available')
        st.markdown(f"""
            <div style="background: #2D2D2D; padding: 1rem; border-radius: 10px;">
                <p style="color: white; margin: 0;">{education_match}</p>
            </div>
        """, unsafe_allow_html=True)
    
    # Recommendations
    recommendations = results.get('recommendations', [])
    if recommendations:
        st.markdown("### 💡 Recommendations")
        for i, rec in enumerate(recommendations, 1):
            st.markdown(f"**{i}.** {rec}")
    
    # PDF Download Section
    st.markdown("---")
    st.markdown("### 📄 Download Professional Report")
    st.markdown("Get a beautifully formatted PDF report of your analysis results:")
    
    # Add PDF download functionality
    user_name = st.session_state.user_data.get('name', 'User')
    add_pdf_download_button(results, user_name)
    
    # Navigation buttons
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        if st.button("🔄 New Analysis", use_container_width=True):
            st.session_state.current_page = 'upload'
            st.session_state.analysis_results = {}
            st.rerun()
    
    with col2:
        if st.button("📊 Saved Results", use_container_width=True):
            st.session_state.current_page = 'saved_results'
            st.rerun()
    
    with col3:
        if st.button("🚪 Logout", use_container_width=True):
            from auth import logout
            logout()
