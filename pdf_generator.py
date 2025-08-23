import streamlit as st
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
import io
from datetime import datetime

def create_professional_pdf_report(analysis_results, user_name="User"):
    """Generate a professional PDF report of the analysis results"""
    
    # Create a BytesIO buffer
    buffer = io.BytesIO()
    
    # Create the PDF document
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        topMargin=0.8*inch,
        bottomMargin=0.8*inch,
        leftMargin=0.8*inch,
        rightMargin=0.8*inch
    )
    
    # Get styles
    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        spaceAfter=30,
        alignment=TA_CENTER,
        textColor=colors.HexColor('#2c3e50')
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=16,
        spaceAfter=12,
        spaceBefore=20,
        textColor=colors.HexColor('#34495e')
    )
    
    body_style = ParagraphStyle(
        'CustomBody',
        parent=styles['Normal'],
        fontSize=11,
        spaceAfter=12,
        alignment=TA_JUSTIFY,
        textColor=colors.HexColor('#2c3e50')
    )
    
    # Build the document content
    story = []
    
    # Title
    story.append(Paragraph("ProFileMatch Analysis Report", title_style))
    story.append(Spacer(1, 20))
    
    # Report info
    report_date = datetime.now().strftime("%B %d, %Y")
    story.append(Paragraph(f"<b>Generated for:</b> {user_name}", body_style))
    story.append(Paragraph(f"<b>Report Date:</b> {report_date}", body_style))
    story.append(Spacer(1, 30))
    
    # ATS Score Section
    ats_score = analysis_results.get('ats_score', 0)
    story.append(Paragraph("ATS Match Score", heading_style))
    
    # Score color based on performance
    if ats_score >= 80:
        score_color = colors.HexColor('#27ae60')
        score_label = "Excellent Match"
    elif ats_score >= 60:
        score_color = colors.HexColor('#f39c12')
        score_label = "Good Match"
    else:
        score_color = colors.HexColor('#e74c3c')
        score_label = "Needs Improvement"
    
    score_style = ParagraphStyle(
        'ScoreStyle',
        parent=styles['Normal'],
        fontSize=36,
        alignment=TA_CENTER,
        textColor=score_color,
        spaceAfter=10
    )
    
    story.append(Paragraph(f"<b>{ats_score}%</b>", score_style))
    story.append(Paragraph(f"<i>{score_label}</i>", ParagraphStyle(
        'ScoreLabelStyle',
        parent=styles['Normal'],
        fontSize=14,
        alignment=TA_CENTER,
        textColor=colors.HexColor('#7f8c8d'),
        spaceAfter=20
    )))
    
    # Summary Section
    summary = analysis_results.get('summary', 'No summary available.')
    story.append(Paragraph("Executive Summary", heading_style))
    story.append(Paragraph(summary, body_style))
    story.append(Spacer(1, 20))
    
    # Skills Analysis Table
    matched_skills = analysis_results.get('matched_skills', [])
    missing_skills = analysis_results.get('missing_skills', [])
    
    if matched_skills or missing_skills:
        story.append(Paragraph("Skills Analysis", heading_style))
        
        # Create skills table
        table_data = [['Matched Skills', 'Missing Skills']]
        
        max_rows = max(len(matched_skills), len(missing_skills))
        for i in range(max_rows):
            matched = matched_skills[i] if i < len(matched_skills) else ""
            missing = missing_skills[i] if i < len(missing_skills) else ""
            table_data.append([matched, missing])
        
        table = Table(table_data, colWidths=[2.5*inch, 2.5*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#34495e')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#ecf0f1')),
            ('TEXTCOLOR', (0, 1), (-1, -1), colors.HexColor('#2c3e50')),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 10),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#bdc3c7')),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('TOPPADDING', (0, 1), (-1, -1), 6),
            ('BOTTOMPADDING', (0, 1), (-1, -1), 6),
        ]))
        
        story.append(table)
        story.append(Spacer(1, 20))
    
    # Experience and Education Match
    experience_match = analysis_results.get('experience_match', 'No analysis available')
    education_match = analysis_results.get('education_match', 'No analysis available')
    
    if experience_match != 'No analysis available':
        story.append(Paragraph("Experience Analysis", heading_style))
        story.append(Paragraph(experience_match, body_style))
        story.append(Spacer(1, 15))
    
    if education_match != 'No analysis available':
        story.append(Paragraph("Education Analysis", heading_style))
        story.append(Paragraph(education_match, body_style))
        story.append(Spacer(1, 15))
    
    # Recommendations
    recommendations = analysis_results.get('recommendations', [])
    if recommendations:
        story.append(Paragraph("Recommendations for Improvement", heading_style))
        for i, rec in enumerate(recommendations, 1):
            story.append(Paragraph(f"<b>{i}.</b> {rec}", body_style))
        story.append(Spacer(1, 20))
    
    # Footer
    story.append(Spacer(1, 30))
    footer_style = ParagraphStyle(
        'Footer',
        parent=styles['Normal'],
        fontSize=10,
        alignment=TA_CENTER,
        textColor=colors.HexColor('#7f8c8d')
    )
    story.append(Paragraph("Generated by ProFileMatch - AI Resume & Job Matcher", footer_style))
    story.append(Paragraph(f"Report Date: {report_date}", footer_style))
    
    # Build the PDF
    doc.build(story)
    buffer.seek(0)
    
    return buffer

def add_pdf_download_button(analysis_results, user_name="User"):
    """Add a download button for the PDF report"""
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("📄 Download PDF Report", use_container_width=True, type="primary"):
            try:
                # Generate PDF
                with st.spinner("🔄 Generating your professional PDF report..."):
                    pdf_buffer = create_professional_pdf_report(analysis_results, user_name)
                
                # Create download
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"ProFileMatch_Report_{timestamp}.pdf"
                
                st.download_button(
                    label="💾 Download Report",
                    data=pdf_buffer,
                    file_name=filename,
                    mime="application/pdf",
                    use_container_width=True
                )
                
                st.success("✅ PDF Report generated successfully!")
                
            except Exception as e:
                st.error("❌ Failed to generate PDF report. Please try again.")
                st.error(f"Error details: {str(e)}")