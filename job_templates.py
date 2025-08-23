import streamlit as st

# Pre-built job description templates for common roles
JOB_TEMPLATES = {
    "Software Engineer": """
**Position:** Software Engineer

**Company:** [Company Name]

**Job Description:**
We are looking for a passionate Software Engineer to design, develop and install software solutions. The successful candidate will be able to build high-quality, innovative and fully performing software in compliance with coding standards and technical design.

**Responsibilities:**
- Design and implement software applications
- Debug and troubleshoot application issues
- Write clean, maintainable code
- Collaborate with cross-functional teams
- Participate in code reviews
- Stay up-to-date with emerging technologies

**Required Skills:**
- Bachelor's degree in Computer Science or related field
- 3+ years of experience in software development
- Proficiency in programming languages: Python, Java, JavaScript
- Experience with web frameworks (React, Django, Flask)
- Knowledge of databases (SQL, NoSQL)
- Understanding of version control systems (Git)
- Strong problem-solving skills
- Excellent communication skills

**Preferred Skills:**
- Experience with cloud platforms (AWS, Azure, GCP)
- Knowledge of containerization (Docker, Kubernetes)
- Familiarity with CI/CD pipelines
- Experience with agile development methodologies
""",

    "Data Scientist": """
**Position:** Data Scientist

**Company:** [Company Name]

**Job Description:**
We are seeking a Data Scientist to join our analytics team. You will be responsible for analyzing large datasets to extract insights that drive business decisions and develop predictive models.

**Responsibilities:**
- Analyze complex datasets to identify trends and patterns
- Develop and implement machine learning models
- Create data visualizations and reports
- Collaborate with stakeholders to understand business requirements
- Clean and preprocess data for analysis
- Present findings to technical and non-technical audiences

**Required Skills:**
- Master's degree in Data Science, Statistics, or related field
- 2+ years of experience in data analysis
- Proficiency in Python or R
- Experience with machine learning libraries (scikit-learn, TensorFlow, PyTorch)
- Strong knowledge of statistics and statistical modeling
- Experience with SQL and database management
- Data visualization tools (Tableau, PowerBI, matplotlib, seaborn)
- Strong analytical and problem-solving skills

**Preferred Skills:**
- Experience with big data technologies (Spark, Hadoop)
- Cloud platform experience (AWS, GCP, Azure)
- Knowledge of deep learning frameworks
- Experience with A/B testing and experimental design
""",

    "Marketing Manager": """
**Position:** Marketing Manager

**Company:** [Company Name]

**Job Description:**
We are looking for a Marketing Manager to develop, implement and execute strategic marketing plans for our organization. You will lead marketing campaigns and drive brand awareness while supporting business growth.

**Responsibilities:**
- Develop comprehensive marketing strategies and campaigns
- Manage marketing budget and allocate resources effectively
- Oversee digital marketing initiatives (SEO, SEM, social media)
- Analyze market trends and customer behavior
- Coordinate with sales teams to align marketing efforts
- Measure and report on campaign performance
- Manage external agencies and vendors

**Required Skills:**
- Bachelor's degree in Marketing, Business, or related field
- 4+ years of marketing experience
- Strong understanding of digital marketing channels
- Experience with marketing automation tools
- Proficiency in analytics tools (Google Analytics, HubSpot)
- Excellent written and verbal communication skills
- Project management experience
- Creative thinking and problem-solving abilities

**Preferred Skills:**
- Experience with content management systems
- Knowledge of graphic design tools (Adobe Creative Suite)
- Social media marketing expertise
- Experience with CRM systems
- Understanding of marketing ROI measurement
""",

    "Product Manager": """
**Position:** Product Manager

**Company:** [Company Name]

**Job Description:**
We're seeking a Product Manager to guide the success of our products and lead cross-functional teams. You will be responsible for the product planning and execution throughout the product lifecycle.

**Responsibilities:**
- Define product vision, strategy, and roadmap
- Work closely with engineering, design, and business teams
- Gather and prioritize product requirements
- Conduct market research and competitive analysis
- Define success metrics and track product performance
- Coordinate product launches and go-to-market strategies
- Communicate with stakeholders and executives

**Required Skills:**
- Bachelor's degree in Business, Engineering, or related field
- 3+ years of product management experience
- Strong analytical and problem-solving skills
- Experience with product management tools (Jira, Confluence, Figma)
- Understanding of software development processes
- Excellent communication and leadership skills
- Data-driven decision making
- Customer-centric mindset

**Preferred Skills:**
- MBA or advanced degree
- Technical background or engineering experience
- Experience with agile/scrum methodologies
- Knowledge of UX/UI principles
- Experience in B2B or B2C product development
""",

    "UX/UI Designer": """
**Position:** UX/UI Designer

**Company:** [Company Name]

**Job Description:**
We are looking for a creative UX/UI Designer to create engaging and intuitive user experiences. You will be responsible for the entire design process from concept to final implementation.

**Responsibilities:**
- Conduct user research and create user personas
- Design wireframes, prototypes, and user interfaces
- Create user journey maps and information architecture
- Collaborate with product managers and developers
- Conduct usability testing and iterate on designs
- Maintain design systems and style guides
- Stay current with design trends and best practices

**Required Skills:**
- Bachelor's degree in Design, HCI, or related field
- 2+ years of UX/UI design experience
- Proficiency in design tools (Figma, Sketch, Adobe Creative Suite)
- Understanding of user-centered design principles
- Experience with prototyping tools
- Knowledge of responsive and mobile design
- Strong portfolio demonstrating design process
- Excellent communication and collaboration skills

**Preferred Skills:**
- Experience with front-end development (HTML, CSS, JavaScript)
- Knowledge of accessibility standards
- Experience with design systems
- Understanding of design research methodologies
- Animation and motion design skills
""",

    "Project Manager": """
**Position:** Project Manager

**Company:** [Company Name]

**Job Description:**
We are seeking an experienced Project Manager to plan, execute, and finalize projects according to strict deadlines and within budget. You will coordinate teams and resources to deliver successful project outcomes.

**Responsibilities:**
- Define project scope, goals, and deliverables
- Develop detailed project plans and timelines
- Coordinate internal resources and third parties
- Monitor project progress and handle changes
- Manage project budgets and resource allocation
- Identify and mitigate project risks
- Communicate project status to stakeholders
- Ensure projects are delivered on time and within scope

**Required Skills:**
- Bachelor's degree in Business, Management, or related field
- 3+ years of project management experience
- PMP or similar project management certification preferred
- Proficiency in project management tools (Asana, Monday, MS Project)
- Strong organizational and time management skills
- Excellent communication and leadership abilities
- Risk management and problem-solving skills
- Experience with budget management

**Preferred Skills:**
- Agile/Scrum Master certification
- Experience in specific industry relevant to company
- Knowledge of change management principles
- Experience with stakeholder management
- Understanding of quality assurance processes
"""
}

def show_job_templates():
    """Display job description templates for quick selection"""
    
    st.markdown("### 🎯 Quick Job Templates")
    st.markdown("Choose from pre-built job descriptions for common roles:")
    
    # Template selection
    col1, col2 = st.columns([2, 1])
    
    with col1:
        selected_template = st.selectbox(
            "Select a job template",
            options=["None"] + list(JOB_TEMPLATES.keys()),
            help="Choose a template to auto-fill the job description"
        )
    
    with col2:
        if st.button("📋 Use Template", use_container_width=True, disabled=(selected_template == "None")):
            if selected_template in JOB_TEMPLATES:
                # Store the template in session state
                st.session_state.selected_job_template = JOB_TEMPLATES[selected_template]
                st.success(f"✅ {selected_template} template loaded!")
                return JOB_TEMPLATES[selected_template]
    
    # Show template preview
    if selected_template != "None" and selected_template in JOB_TEMPLATES:
        with st.expander(f"👀 Preview: {selected_template}"):
            st.markdown(JOB_TEMPLATES[selected_template])
    
    return None

def get_template_content():
    """Get the selected template content from session state"""
    return st.session_state.get('selected_job_template', '')

def clear_template():
    """Clear the selected template from session state"""
    if 'selected_job_template' in st.session_state:
        del st.session_state.selected_job_template