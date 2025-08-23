import streamlit as st
import PyPDF2
import io
from ai_analyzer import analyze_resume_job_match
from job_templates import show_job_templates, get_template_content, clear_template
try:
    from docx import Document
    DOCX_AVAILABLE = True
except ImportError:
    DOCX_AVAILABLE = False

def extract_text_from_pdf(pdf_file):
    """Extract text from PDF file"""
    try:
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text() + "\n"
        return text.strip()
    except Exception as e:
        st.error("Unable to read PDF file. Please try a different file or convert to text format.")
        return None

def extract_text_from_txt(txt_file):
    """Extract text from TXT file"""
    try:
        return str(txt_file.read(), "utf-8")
    except Exception as e:
        st.error("Unable to read text file. Please check the file format and try again.")
        return None

def extract_text_from_docx(docx_file):
    """Extract text from DOCX file"""
    if not DOCX_AVAILABLE:
        st.error("DOCX support not available. Please convert to PDF or TXT format.")
        return None
    
    try:
        doc = Document(docx_file)
        text = []
        for paragraph in doc.paragraphs:
            text.append(paragraph.text)
        return '\n'.join(text)
    except Exception as e:
        st.error("Unable to read DOCX file. Please check the file format and try again.")
        return None

def process_uploaded_file(uploaded_file):
    """Process uploaded file and extract text"""
    if uploaded_file is None:
        return None
    
    file_extension = uploaded_file.name.split('.')[-1].lower()
    
    if file_extension == 'pdf':
        return extract_text_from_pdf(uploaded_file)
    elif file_extension == 'txt':
        return extract_text_from_txt(uploaded_file)
    elif file_extension in ['docx', 'doc']:
        return extract_text_from_docx(uploaded_file)
    else:
        supported_formats = "PDF, TXT" + (", DOCX, DOC" if DOCX_AVAILABLE else "")
        st.error(f"Unsupported file format. Please upload {supported_formats} files only.")
        return None

def show_upload_page():
    """Display the enhanced file upload page with drag & drop and animations"""
    
    # Enhanced navigation bar
    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:
        user_name = st.session_state.user_data.get('name', 'User')
        st.markdown(f"""
            <div style="display: flex; align-items: center; gap: 1rem;">
                <h2 style="color: #3498db; margin: 0; font-size: 2rem;">👋 Welcome, {user_name}!</h2>
            </div>
        """, unsafe_allow_html=True)
    with col2:
        if st.button("📊 Saved Results", use_container_width=True):
            st.session_state.current_page = 'saved_results'
            st.rerun()
    with col3:
        if st.button("🚪 Logout", use_container_width=True):
            from auth import logout
            logout()
    
    st.markdown("---")
    
    # Enhanced file upload section with animations
    st.markdown("""
        <div style="text-align: center; margin: 2rem 0;">
            <h2 style="color: #ecf0f1; font-size: 2.5rem; margin-bottom: 1rem;">📂 Upload Your Documents</h2>
            <p style="color: #bdc3c7; font-size: 1.1rem;">Drag and drop your files or click to browse</p>
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
            <div class="upload-zone" style="text-align: center; margin-bottom: 1rem;">
                <h4 style="color: #3498db; font-size: 1.4rem;">📝 Resume</h4>
                <p style="color: #bdc3c7; font-size: 0.9rem;">PDF, TXT, DOCX formats</p>
            </div>
        """, unsafe_allow_html=True)
        
        # Determine supported file types
        supported_types = ['pdf', 'txt']
        if DOCX_AVAILABLE:
            supported_types.extend(['docx', 'doc'])
        
        resume_file = st.file_uploader(
            "Choose your resume file",
            type=supported_types,
            key="resume_upload",
            help=f"Supported formats: {', '.join(supported_types).upper()}"
        )
        
        if resume_file:
            st.markdown(f"""
                <div class="success-check" style="background: linear-gradient(135deg, #2ecc71, #27ae60); padding: 1rem; border-radius: 10px; text-align: center; margin-top: 1rem;">
                    <h4 style="color: white; margin: 0;">✅ Resume Ready!</h4>
                    <p style="color: white; margin: 0; opacity: 0.9;">{resume_file.name}</p>
                </div>
            """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
            <div class="upload-zone" style="text-align: center; margin-bottom: 1rem;">
                <h4 style="color: #e74c3c; font-size: 1.4rem;">💼 Job Description</h4>
                <p style="color: #bdc3c7; font-size: 0.9rem;">PDF, TXT, DOCX formats</p>
            </div>
        """, unsafe_allow_html=True)
        
        job_file = st.file_uploader(
            "Choose job description file",
            type=supported_types,
            key="job_upload",
            help=f"Supported formats: {', '.join(supported_types).upper()}"
        )
        
        if job_file:
            st.markdown(f"""
                <div class="success-check" style="background: linear-gradient(135deg, #2ecc71, #27ae60); padding: 1rem; border-radius: 10px; text-align: center; margin-top: 1rem;">
                    <h4 style="color: white; margin: 0;">✅ Job Description Ready!</h4>
                    <p style="color: white; margin: 0; opacity: 0.9;">{job_file.name}</p>
                </div>
            """, unsafe_allow_html=True)
    
    # Enhanced alternative text input with better styling
    st.markdown("---")
    st.markdown("""
        <div style="text-align: center; margin: 2rem 0;">
            <h3 style="color: #ecf0f1; font-size: 2rem;">✍️ Or Enter Text Directly</h3>
            <p style="color: #bdc3c7;">Copy and paste your content below</p>
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 📝 Resume Text")
        resume_text = st.text_area(
            "Paste your resume text here",
            height=200,
            placeholder="Copy and paste your resume content here...",
            help="Enter your resume content as plain text",
            key="resume_text"
        )
    
    with col2:
        st.markdown("#### 💼 Job Description Text")
        
        # Show job templates
        template_content = show_job_templates()
        
        # Get existing template content or use new template
        initial_content = get_template_content() if template_content is None else template_content
        
        job_text = st.text_area(
            "Paste job description here",
            height=200,
            value=initial_content,
            placeholder="Copy and paste the job description here or use a template above...",
            help="Enter the job posting content as plain text or select a template",
            key="job_text"
        )
        
        # Clear template button
        if initial_content:
            if st.button("🗑️ Clear Template", help="Clear the template and start fresh"):
                clear_template()
                st.rerun()
    
    # Enhanced analyze button with animation
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        analyze_button = st.button("🚀 Analyze Match", use_container_width=True, type="primary")
        
        if analyze_button:
            # Get resume content
            resume_content = None
            if resume_file:
                resume_content = process_uploaded_file(resume_file)
            elif resume_text.strip():
                resume_content = resume_text.strip()
            
            # Get job description text
            job_content = None
            if job_file:
                job_content = process_uploaded_file(job_file)
            elif job_text.strip():
                job_content = job_text.strip()
            
            # Validate inputs
            if not resume_content:
                st.error("❌ Please upload a resume file or paste resume text")
                return
            
            if not job_content:
                st.error("❌ Please upload a job description file or paste job description text")
                return
            
            # Animated progress section
            progress_container = st.empty()
            
            with progress_container.container():
                st.markdown("""
                    <div class="progress-container">
                        <h4 style="color: #ecf0f1; text-align: center; margin-bottom: 1rem;">🔍 Processing Your Files...</h4>
                    </div>
                """, unsafe_allow_html=True)
                
                # Progress steps with animations
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                import time
                
                status_text.markdown("**Step 1:** Extracting text from files...")
                time.sleep(0.5)
                progress_bar.progress(25)
                
                status_text.markdown("**Step 2:** Preparing content for AI analysis...")
                time.sleep(0.5)
                progress_bar.progress(50)
                
                status_text.markdown("**Step 3:** Running AI analysis...")
                time.sleep(0.5)
                progress_bar.progress(75)
                
                # Show processing message
                with st.spinner("🔄 Analyzing your resume against the job description..."):
                    try:
                        # Analyze the resume-job match
                        results = analyze_resume_job_match(resume_content, job_content)
                        
                        if results:
                            status_text.markdown("**Step 4:** Analysis complete! ✅")
                            progress_bar.progress(100)
                            
                            # Store results in session state
                            st.session_state.analysis_results = results
                            st.session_state.analysis_results['resume_text'] = resume_content
                            st.session_state.analysis_results['job_text'] = job_content
                            
                            # Success animation
                            st.markdown("""
                                <div class="success-check" style="background: linear-gradient(135deg, #2ecc71, #27ae60); padding: 1.5rem; border-radius: 15px; text-align: center; margin: 1rem 0;">
                                    <h3 style="color: white; margin: 0;">🎉 Analysis Complete!</h3>
                                    <p style="color: white; margin: 0.5rem 0 0 0;">Redirecting to results...</p>
                                </div>
                            """, unsafe_allow_html=True)
                            
                            # Small delay for user to see the success message
                            time.sleep(1.5)
                            
                            # Navigate to results page
                            st.session_state.current_page = 'results'
                            st.rerun()
                        else:
                            progress_bar.progress(100)
                            status_text.markdown("❌ **Error:** Analysis failed")
                            st.error("❌ Analysis failed. Please check your documents and try again.")
                            
                    except Exception as e:
                        progress_bar.progress(100)
                        status_text.markdown("❌ **Error:** Unable to complete analysis")
                        st.error("❌ Unable to complete analysis. Please try again or contact support.")
    
    # Enhanced navigation to saved results
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("📊 View Saved Results", use_container_width=True):
            st.session_state.current_page = 'saved_results'
            st.rerun()
