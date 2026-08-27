"""
Unit tests for Kairo — AI Helper engine & student guardrails.
"""

from utils.ai_helper import (
    is_off_topic_or_inappropriate,
    generate_ai_chat_response,
    generate_study_plan_ai,
    generate_mcq_quiz,
    generate_career_roadmap_ai
)

def test_guardrails_check():
    assert is_off_topic_or_inappropriate("hack bank account") == True
    assert is_off_topic_or_inappropriate("explain binary search trees") == False

def test_chat_guardrail_response():
    resp = generate_ai_chat_response("hack bank")
    assert "Academic Guardrail" in resp

def test_chat_fallback_response():
    resp = generate_ai_chat_response("explain Python loops")
    assert "Python" in resp or "Code" in resp

def test_study_plan_generator():
    tasks = generate_study_plan_ai("Python, Math", "2026-09-01", 4.0)
    assert isinstance(tasks, list)
    assert len(tasks) >= 3
    assert "subject" in tasks[0]
    assert "hours" in tasks[0]

def test_mcq_quiz_generator():
    quiz = generate_mcq_quiz("Python", "Lists", "Intermediate", 4)
    assert isinstance(quiz, list)
    assert len(quiz) == 4
    assert "question" in quiz[0]
    assert "options" in quiz[0]
    assert len(quiz[0]["options"]) == 4

def test_career_roadmap_generator():
    roadmap = generate_career_roadmap_ai("3rd Year", "Python, Git", "AI Engineer")
    assert isinstance(roadmap, dict)
    assert "phases" in roadmap
    assert len(roadmap["phases"]) >= 2
