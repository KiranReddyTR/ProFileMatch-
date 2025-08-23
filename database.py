import streamlit as st
import json
import os
from datetime import datetime
import pandas as pd

def save_analysis_result(results, user_email):
    """Save analysis result to persistent storage"""
    
    # Create results directory if it doesn't exist
    if not os.path.exists("saved_analyses"):
        os.makedirs("saved_analyses")
    
    # Add metadata
    results_with_metadata = results.copy()
    results_with_metadata.update({
        'timestamp': datetime.now().isoformat(),
        'user_email': user_email
    })
    
    # Save to file
    filename = f"saved_analyses/analysis_{user_email}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    
    try:
        with open(filename, 'w') as f:
            json.dump(results_with_metadata, f, indent=2)
        return True, filename
    except Exception as e:
        st.error("Unable to save results. Please try again.")
        return False, None

def load_user_analyses(user_email):
    """Load all analyses for a specific user"""
    
    if not os.path.exists("saved_analyses"):
        return []
    
    user_analyses = []
    
    try:
        for filename in os.listdir("saved_analyses"):
            if filename.endswith('.json') and user_email in filename:
                filepath = os.path.join("saved_analyses", filename)
                with open(filepath, 'r') as f:
                    analysis = json.load(f)
                    analysis['filename'] = filename
                    user_analyses.append(analysis)
        
        # Sort by timestamp (newest first)
        user_analyses.sort(key=lambda x: x.get('timestamp', ''), reverse=True)
        
    except Exception as e:
        st.error("Unable to load saved results. Please refresh the page.")
    
    return user_analyses

def delete_analysis(filename):
    """Delete a saved analysis"""
    try:
        filepath = os.path.join("saved_analyses", filename)
        if os.path.exists(filepath):
            os.remove(filepath)
            return True
    except Exception as e:
        st.error("Unable to delete analysis. Please try again.")
    return False

def export_analysis_to_csv(analyses):
    """Export analyses to CSV format"""
    
    if not analyses:
        return None
    
    # Flatten the data for CSV export
    flattened_data = []
    
    for analysis in analyses:
        row = {
            'Timestamp': analysis.get('timestamp', ''),
            'ATS Score': analysis.get('ats_score', 0),
            'Matched Skills Count': len(analysis.get('matched_skills', [])),
            'Missing Skills Count': len(analysis.get('missing_skills', [])),
            'Matched Skills': ', '.join(analysis.get('matched_skills', [])),
            'Missing Skills': ', '.join(analysis.get('missing_skills', [])),
            'Summary': analysis.get('summary', ''),
            'Experience Match': analysis.get('experience_match', ''),
            'Education Match': analysis.get('education_match', '')
        }
        flattened_data.append(row)
    
    return pd.DataFrame(flattened_data)

def show_saved_results_page():
    """Display the saved results page"""
    
    # Navigation
    col1, col2, col3 = st.columns([1, 2, 1])
    with col1:
        if st.button("← Back to Upload"):
            st.session_state.current_page = 'upload'
            st.rerun()
    with col3:
        if st.button("🚪 Logout"):
            from auth import logout
            logout()
    
    # Title
    st.markdown("<h1 class='page-title'>📊 Saved Analysis Results</h1>", unsafe_allow_html=True)
    st.markdown("---")
    
    # Get user email
    user_email = st.session_state.user_data.get('email', '')
    
    if not user_email:
        st.error("Session expired. Please log in again.")
        return
    
    # Load saved analyses
    saved_analyses = load_user_analyses(user_email)
    
    # Also include session-based results
    if 'saved_results' in st.session_state and st.session_state.saved_results:
        saved_analyses.extend(st.session_state.saved_results)
    
    if not saved_analyses:
        st.markdown("""
            <div style="text-align: center; padding: 3rem; background: #2D2D2D; border-radius: 10px; margin: 2rem 0;">
                <h3 style="color: #ffffff; font-weight: 600;">📭 No Saved Results</h3>
                <p style="color: #e8e8e8; font-weight: 500;">You haven't saved any analysis results yet.</p>
                <p style="color: #e8e8e8; font-weight: 500;">Complete an analysis and save it to see your results here.</p>
            </div>
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("🚀 Start New Analysis", use_container_width=True, type="primary"):
                st.session_state.current_page = 'upload'
                st.rerun()
        return
    
    # Export functionality
    st.markdown("### 📥 Export Options")
    col1, col2 = st.columns([1, 3])
    with col1:
        if st.button("📊 Export to CSV"):
            df = export_analysis_to_csv(saved_analyses)
            if df is not None:
                csv = df.to_csv(index=False)
                st.download_button(
                    label="⬇️ Download CSV",
                    data=csv,
                    file_name=f"resume_analyses_{datetime.now().strftime('%Y%m%d')}.csv",
                    mime="text/csv"
                )
    
    st.markdown("---")
    
    # Display saved analyses
    st.markdown(f"### 📋 Your Analysis History ({len(saved_analyses)} results)")
    
    for i, analysis in enumerate(saved_analyses):
        with st.expander(f"📄 Analysis #{i+1} - Score: {analysis.get('ats_score', 'N/A')}% - {analysis.get('timestamp', 'Unknown date')[:10]}"):
            
            # Analysis overview
            col1, col2, col3 = st.columns(3)
            
            with col1:
                ats_score = analysis.get('ats_score', 0)
                score_color = "#4CAF50" if ats_score >= 80 else "#FFC107" if ats_score >= 60 else "#FF5722"
                st.markdown(f"""
                    <div style="text-align: center; background: #2D2D2D; padding: 1rem; border-radius: 8px;">
                        <h3 style="color: {score_color}; margin: 0;">{ats_score}%</h3>
                        <p style="color: #ffffff; margin: 0; font-weight: 500;">ATS Score</p>
                    </div>
                """, unsafe_allow_html=True)
            
            with col2:
                matched_count = len(analysis.get('matched_skills', []))
                st.markdown(f"""
                    <div style="text-align: center; background: #2D2D2D; padding: 1rem; border-radius: 8px;">
                        <h3 style="color: #4CAF50; margin: 0;">{matched_count}</h3>
                        <p style="color: #ffffff; margin: 0; font-weight: 500;">Matched Skills</p>
                    </div>
                """, unsafe_allow_html=True)
            
            with col3:
                missing_count = len(analysis.get('missing_skills', []))
                st.markdown(f"""
                    <div style="text-align: center; background: #2D2D2D; padding: 1rem; border-radius: 8px;">
                        <h3 style="color: #FF5722; margin: 0;">{missing_count}</h3>
                        <p style="color: #ffffff; margin: 0; font-weight: 500;">Missing Skills</p>
                    </div>
                """, unsafe_allow_html=True)
            
            st.markdown("---")
            
            # Summary
            summary = analysis.get('summary', 'No summary available')
            st.markdown(f"**Summary:** {summary}")
            
            # Skills breakdown
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**✅ Matched Skills:**")
                matched_skills = analysis.get('matched_skills', [])
                if matched_skills:
                    for skill in matched_skills:
                        st.markdown(f"• {skill}")
                else:
                    st.markdown("*None*")
            
            with col2:
                st.markdown("**❌ Missing Skills:**")
                missing_skills = analysis.get('missing_skills', [])
                if missing_skills:
                    for skill in missing_skills:
                        st.markdown(f"• {skill}")
                else:
                    st.markdown("*None*")
            
            # Additional information
            if analysis.get('experience_match'):
                st.markdown(f"**Experience Match:** {analysis.get('experience_match')}")
            
            if analysis.get('education_match'):
                st.markdown(f"**Education Match:** {analysis.get('education_match')}")
            
            # Action buttons
            col1, col2, col3 = st.columns(3)
            
            with col1:
                if st.button(f"📊 View Details #{i+1}", key=f"view_{i}"):
                    # Set this analysis as current and navigate to results
                    st.session_state.analysis_results = analysis
                    st.session_state.current_page = 'results'
                    st.rerun()
            
            with col2:
                # Individual export
                analysis_df = export_analysis_to_csv([analysis])
                if analysis_df is not None:
                    csv = analysis_df.to_csv(index=False)
                    st.download_button(
                        label=f"⬇️ Export #{i+1}",
                        data=csv,
                        file_name=f"analysis_{i+1}_{datetime.now().strftime('%Y%m%d')}.csv",
                        mime="text/csv",
                        key=f"export_{i}"
                    )
            
            with col3:
                if st.button(f"🗑️ Delete #{i+1}", key=f"delete_{i}", type="secondary"):
                    # Delete from file system if it has a filename
                    if 'filename' in analysis:
                        if delete_analysis(analysis['filename']):
                            st.success("Analysis deleted successfully!")
                            st.rerun()
                    else:
                        # Delete from session state
                        if analysis in st.session_state.saved_results:
                            st.session_state.saved_results.remove(analysis)
                            st.success("Analysis deleted successfully!")
                            st.rerun()
    
    # Action buttons at the bottom
    st.markdown("---")
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🆕 New Analysis", use_container_width=True, type="primary"):
            st.session_state.current_page = 'upload'
            st.rerun()
    
    with col2:
        if st.button("🔄 Refresh Results", use_container_width=True):
            st.rerun()
