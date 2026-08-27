"""
Kairo — PDF Helper
Generates downloadable modern PDFs using ReportLab for Resumes, Study Plans, and Career Roadmaps.
"""

import io
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable, Table, TableStyle

def generate_resume_pdf(resume_data: dict) -> bytes:
    """Compile resume dict into a PDF byte stream."""
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40
    )
    
    styles = getSampleStyleSheet()
    
    name_style = ParagraphStyle(
        'NameStyle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=24,
        leading=28,
        textColor=colors.HexColor('#0f172a'),
        alignment=0,
        spaceAfter=4
    )
    
    contact_style = ParagraphStyle(
        'ContactStyle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=12,
        textColor=colors.HexColor('#475569'),
        alignment=0,
        spaceAfter=12
    )
    
    section_heading = ParagraphStyle(
        'SectionHeading',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=13,
        leading=16,
        textColor=colors.HexColor('#0284c7'),
        spaceBefore=10,
        spaceAfter=4
    )
    
    body_bold = ParagraphStyle(
        'BodyBold',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10,
        leading=14,
        textColor=colors.HexColor('#1e293b'),
        spaceAfter=2
    )
    
    body_style = ParagraphStyle(
        'BodyStyle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=13.5,
        textColor=colors.HexColor('#334155'),
        spaceAfter=6
    )

    story = []

    name = resume_data.get("name", "Alex Mercer")
    story.append(Paragraph(name, name_style))
    
    contact_info = [
        resume_data.get("email", ""),
        resume_data.get("phone", ""),
        resume_data.get("location", ""),
        resume_data.get("linkedin", ""),
        resume_data.get("github", "")
    ]
    contact_line = "  •  ".join([c for c in contact_info if c])
    story.append(Paragraph(contact_line, contact_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor('#0284c7'), spaceAfter=10))

    summary = resume_data.get("summary", "")
    if summary:
        story.append(Paragraph("PROFESSIONAL SUMMARY", section_heading))
        story.append(Paragraph(summary, body_style))

    edu = resume_data.get("education", "")
    if edu:
        story.append(Paragraph("EDUCATION", section_heading))
        story.append(Paragraph(edu, body_style))

    skills = resume_data.get("skills", "")
    if skills:
        story.append(Paragraph("TECHNICAL SKILLS", section_heading))
        story.append(Paragraph(f"<b>Key Competencies:</b> {skills}", body_style))

    projects = resume_data.get("projects", [])
    if projects:
        story.append(Paragraph("PROJECTS", section_heading))
        for proj in projects:
            p_title = proj.get("title", "")
            p_desc = proj.get("desc", "")
            if p_title:
                story.append(Paragraph(f"<b>{p_title}</b>", body_bold))
            if p_desc:
                story.append(Paragraph(p_desc, body_style))

    exp = resume_data.get("experience", [])
    if exp:
        story.append(Paragraph("EXPERIENCE", section_heading))
        for item in exp:
            role = item.get("role", "")
            company = item.get("company", "")
            period = item.get("period", "")
            desc = item.get("desc", "")
            header = f"<b>{role}</b> - {company} <i>({period})</i>"
            story.append(Paragraph(header, body_bold))
            if desc:
                story.append(Paragraph(desc, body_style))

    certs = resume_data.get("certifications", "")
    if certs:
        story.append(Paragraph("CERTIFICATIONS & ACHIEVEMENTS", section_heading))
        story.append(Paragraph(certs, body_style))

    doc.build(story)
    pdf_bytes = buffer.getvalue()
    buffer.close()
    return pdf_bytes

def generate_study_plan_pdf(tasks: list, user_name: str = "Alex Mercer") -> bytes:
    """Compile study tasks into a clean PDF Schedule Document."""
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40
    )
    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        'TitleStyle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=20,
        leading=24,
        textColor=colors.HexColor('#0f172a'),
        spaceAfter=4
    )
    
    sub_style = ParagraphStyle(
        'SubStyle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        leading=14,
        textColor=colors.HexColor('#64748b'),
        spaceAfter=12
    )

    story = []
    story.append(Paragraph(f"Kairo — Study Schedule", title_style))
    story.append(Paragraph(f"Student: {user_name} | Generated by Kairo Platform", sub_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor('#00f2fe'), spaceAfter=14))

    table_data = [["Status", "Subject", "Task Description", "Allocated Hours"]]
    for task in tasks:
        status = "✅ Completed" if task.get("completed") else "⏳ Pending"
        table_data.append([
            status,
            task.get("subject", "General"),
            task.get("title", ""),
            f"{task.get('hours', 1.0)} hrs"
        ])

    t = Table(table_data, colWidths=[90, 110, 240, 90])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#0f172a')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.HexColor('#ffffff')),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
        ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#f8fafc')),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#cbd5e1')),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    story.append(t)

    doc.build(story)
    pdf_bytes = buffer.getvalue()
    buffer.close()
    return pdf_bytes

def generate_roadmap_pdf(roadmap: dict, user_name: str = "Alex Mercer") -> bytes:
    """Compile AI Career Roadmap into a formatted PDF."""
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40
    )
    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        'TitleStyle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=20,
        leading=24,
        textColor=colors.HexColor('#0f172a'),
        spaceAfter=4
    )
    
    sub_style = ParagraphStyle(
        'SubStyle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        leading=14,
        textColor=colors.HexColor('#64748b'),
        spaceAfter=12
    )

    section_heading = ParagraphStyle(
        'SectionHeading',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=16,
        textColor=colors.HexColor('#7f00ff'),
        spaceBefore=10,
        spaceAfter=4
    )

    body_style = ParagraphStyle(
        'BodyStyle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=13.5,
        textColor=colors.HexColor('#334155'),
        spaceAfter=6
    )

    story = []
    goal = roadmap.get("career_goal", "Career Goal")
    story.append(Paragraph(f"Kairo — Career Roadmap: {goal}", title_style))
    story.append(Paragraph(f"Student: {user_name} | Generated by Kairo AI", sub_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor('#7f00ff'), spaceAfter=14))

    phases = roadmap.get("phases", [])
    for phase in phases:
        p_title = phase.get("phase", "Phase")
        timeframe = phase.get("timeframe", "")
        story.append(Paragraph(f"{p_title} ({timeframe})", section_heading))
        
        milestones = phase.get("milestones", [])
        for m in milestones:
            m_title = m.get("title", "")
            m_desc = m.get("desc", "")
            story.append(Paragraph(f"• <b>{m_title}</b>: {m_desc}", body_style))
        story.append(Spacer(1, 6))

    doc.build(story)
    pdf_bytes = buffer.getvalue()
    buffer.close()
    return pdf_bytes
