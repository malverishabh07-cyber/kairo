"""
Unit tests for Kairo — ReportLab PDF generators.
"""

from utils.pdf_helper import generate_resume_pdf, generate_study_plan_pdf, generate_roadmap_pdf

def test_generate_resume_pdf():
    sample_resume = {
        "name": "Alex Mercer",
        "email": "alex@stanford.edu",
        "summary": "CS student specializing in AI.",
        "skills": "Python, TypeScript",
        "education": "Stanford University",
        "projects": [{"title": "Kairo", "desc": "Productivity web app"}],
        "experience": [{"role": "Intern", "company": "Tech Lab", "period": "2025", "desc": "Built ML models"}]
    }
    pdf_bytes = generate_resume_pdf(sample_resume)
    assert isinstance(pdf_bytes, bytes)
    assert len(pdf_bytes) > 500
    assert pdf_bytes.startswith(b"%PDF")

def test_generate_study_plan_pdf():
    sample_tasks = [
        {"subject": "Data Structures", "title": "Review Binary Trees", "hours": 2.0, "completed": True},
        {"subject": "Python", "title": "Practice Generators", "hours": 1.5, "completed": False}
    ]
    pdf_bytes = generate_study_plan_pdf(sample_tasks, "Alex Mercer")
    assert isinstance(pdf_bytes, bytes)
    assert len(pdf_bytes) > 500
    assert pdf_bytes.startswith(b"%PDF")

def test_generate_roadmap_pdf():
    sample_roadmap = {
        "career_goal": "AI Engineer",
        "phases": [
            {
                "phase": "Phase 1: Core Fundamentals",
                "timeframe": "Months 1-3",
                "milestones": [{"title": "LeetCode Practice", "desc": "Solve 100 problems"}]
            }
        ]
    }
    pdf_bytes = generate_roadmap_pdf(sample_roadmap, "Alex Mercer")
    assert isinstance(pdf_bytes, bytes)
    assert len(pdf_bytes) > 500
    assert pdf_bytes.startswith(b"%PDF")
