"""
Kairo — Storage & Session State Helper
Handles default initialization, user-keyed JSON file persistence, XP & focus tracking, and data mutation helpers.
"""

import os
import json
import streamlit as st
from datetime import date
from utils.auth_helper import get_current_user_id, login_guest

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")

def ensure_data_dir():
    """Ensure data directory exists."""
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR, exist_ok=True)

def get_user_file_path(user_id: str = None) -> str:
    """Get absolute path to user data file."""
    ensure_data_dir()
    uid = user_id or get_current_user_id()
    return os.path.join(DATA_DIR, f"{uid}.json")

def save_user_data():
    """Persist current session state data to user JSON file."""
    try:
        user_id = get_current_user_id()
        file_path = get_user_file_path(user_id)

        payload = {
            "user_name": st.session_state.get("user_name", "Alex Mercer"),
            "user_school": st.session_state.get("user_school", "Stanford University"),
            "user_major": st.session_state.get("user_major", "Computer Science"),
            "target_gpa": st.session_state.get("target_gpa", "3.9"),
            "daily_target_hours": st.session_state.get("daily_target_hours", 4.5),
            "study_streak": st.session_state.get("study_streak", 12),
            "user_xp": st.session_state.get("user_xp", 1450),
            "tasks_completed_count": st.session_state.get("tasks_completed_count", 28),
            "total_study_hours": st.session_state.get("total_study_hours", 42.5),
            "focus_sessions_completed": st.session_state.get("focus_sessions_completed", 16),
            "theme_preset": st.session_state.get("theme_preset", "cyan_violet"),
            "ambient_sound": st.session_state.get("ambient_sound", "lofi"),
            "ambient_sound_enabled": st.session_state.get("ambient_sound_enabled", True),
            "study_tasks": st.session_state.get("study_tasks", []),
            "quiz_history": st.session_state.get("quiz_history", []),
            "resume_data": st.session_state.get("resume_data", {}),
            "career_roadmap": st.session_state.get("career_roadmap", None),
            "chat_messages": st.session_state.get("chat_messages", [])
        }

        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(payload, f, indent=2, default=str)
    except Exception as e:
        print(f"Warning: Failed to save user data: {e}")

def load_user_data(user_id: str = None):
    """Load user data from JSON file into session state if available."""
    try:
        file_path = get_user_file_path(user_id)
        if os.path.exists(file_path):
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)

            for key in [
                "user_name", "user_school", "user_major", "target_gpa", "daily_target_hours",
                "study_streak", "user_xp", "tasks_completed_count", "total_study_hours",
                "focus_sessions_completed", "theme_preset", "ambient_sound", "ambient_sound_enabled",
                "study_tasks", "quiz_history", "resume_data", "career_roadmap", "chat_messages"
            ]:
                if key in data:
                    st.session_state[key] = data[key]
    except Exception as e:
        print(f"Warning: Failed to load user data: {e}")

def init_session_state():
    """Ensure session state is fully populated with realistic defaults and persistent data."""
    if "user_account" not in st.session_state:
        login_guest()

    if "auth_show_modal" not in st.session_state:
        st.session_state["auth_show_modal"] = False

    # Default Theme Preset
    if "theme_preset" not in st.session_state:
        st.session_state["theme_preset"] = "cyan_violet"

    # Default Profile State
    if "user_name" not in st.session_state:
        st.session_state["user_name"] = "Alex Mercer"
    if "user_school" not in st.session_state:
        st.session_state["user_school"] = "Stanford University"
    if "user_major" not in st.session_state:
        st.session_state["user_major"] = "Computer Science"
    if "target_gpa" not in st.session_state:
        st.session_state["target_gpa"] = "3.9"
    if "daily_target_hours" not in st.session_state:
        st.session_state["daily_target_hours"] = 4.5

    # Default Metrics & Gamification State
    if "study_streak" not in st.session_state:
        st.session_state["study_streak"] = 12
    if "user_xp" not in st.session_state:
        st.session_state["user_xp"] = 1450
    if "tasks_completed_count" not in st.session_state:
        st.session_state["tasks_completed_count"] = 28
    if "total_study_hours" not in st.session_state:
        st.session_state["total_study_hours"] = 42.5
    if "focus_sessions_completed" not in st.session_state:
        st.session_state["focus_sessions_completed"] = 16
    if "checked_in_today" not in st.session_state:
        st.session_state["checked_in_today"] = False

    # Focus Timer Ambient Sound Defaults
    if "ambient_sound" not in st.session_state:
        st.session_state["ambient_sound"] = "lofi"
    if "ambient_sound_enabled" not in st.session_state:
        st.session_state["ambient_sound_enabled"] = True

    # Default Chat Messages
    if "chat_messages" not in st.session_state:
        st.session_state["chat_messages"] = [
            {"role": "assistant", "content": "Hello! I am **Kairo AI**, your personal academic mentor & productivity assistant. How can I help you master your focus and subjects today?"}
        ]

    # Default Study Tasks
    if "study_tasks" not in st.session_state:
        st.session_state["study_tasks"] = [
            {"id": 1, "subject": "Data Structures", "title": "Review Binary Search Trees & AVL rotations", "hours": 1.5, "completed": True, "date": str(date.today())},
            {"id": 2, "subject": "Operating Systems", "title": "Implement Process Synchronization with Semaphores", "hours": 2.0, "completed": False, "date": str(date.today())},
            {"id": 3, "subject": "Linear Algebra", "title": "Practice Eigenvalues & Eigenvectors calculations", "hours": 1.0, "completed": False, "date": str(date.today())},
            {"id": 4, "subject": "Machine Learning", "title": "Read Neural Networks Backpropagation derivation", "hours": 2.0, "completed": True, "date": str(date.today())},
        ]

    # Default Quiz History & Current Quiz
    if "quiz_history" not in st.session_state:
        st.session_state["quiz_history"] = [
            {"subject": "Python Basics", "score": 90, "total": 100, "date": "2026-08-04"},
            {"subject": "Data Structures", "score": 85, "total": 100, "date": "2026-08-05"},
            {"subject": "Machine Learning", "score": 95, "total": 100, "date": "2026-08-06"},
        ]
    if "current_quiz" not in st.session_state:
        st.session_state["current_quiz"] = None

    # Default Resume State
    if "resume_data" not in st.session_state:
        st.session_state["resume_data"] = {
            "name": "Alex Mercer",
            "email": "alex.mercer@stanford.edu",
            "phone": "+1 (555) 234-5678",
            "location": "Palo Alto, CA",
            "linkedin": "linkedin.com/in/alex-mercer",
            "github": "github.com/alex-mercer",
            "summary": "Ambitious Computer Science undergraduate specializing in Artificial Intelligence and Full-Stack Engineering. Proven track record in building scalable ML pipelines, web applications, and algorithmic problem-solving.",
            "education": "B.S. in Computer Science, Stanford University (2023 - 2027) | GPA: 3.9/4.0",
            "skills": "Python, TypeScript, React, Next.js, PyTorch, Streamlit, PostgreSQL, Docker, Git, REST APIs",
            "projects": [
                {
                    "title": "Kairo — Focus & Smart Productivity Platform",
                    "desc": "Built a full-stack student productivity suite featuring AI mentor, interactive focus timer with soundscapes, study planner, and PDF exports."
                },
                {
                    "title": "Neural Vision - Image Classifier",
                    "desc": "Developed a ResNet-based image classification pipeline achieving 94% accuracy on domain dataset with PyTorch and CUDA optimization."
                }
            ],
            "experience": [
                {
                    "role": "AI Research Assistant",
                    "company": "Stanford AI Lab",
                    "period": "Jun 2025 - Present",
                    "desc": "Assisted in fine-tuning open-source LLMs on specialized domain datasets. Reduced inference latency by 18%."
                }
            ],
            "certifications": "DeepLearning.AI TensorFlow Specialization, AWS Certified Developer Associate"
        }

    # Default Career Roadmap
    if "career_roadmap" not in st.session_state:
        st.session_state["career_roadmap"] = None

    # Settings & API Key
    if "gemini_api_key" not in st.session_state:
        st.session_state["gemini_api_key"] = ""

    # Attempt to load saved data for active user
    load_user_data()

def add_xp(points: int):
    """Increment user XP and persist."""
    st.session_state["user_xp"] = st.session_state.get("user_xp", 1450) + points
    save_user_data()

def complete_focus_session(duration_minutes: float = 25.0):
    """Record completed focus session, award XP, update streak and hours."""
    st.session_state["focus_sessions_completed"] = st.session_state.get("focus_sessions_completed", 0) + 1
    hours_add = round(duration_minutes / 60.0, 2)
    st.session_state["total_study_hours"] = round(st.session_state.get("total_study_hours", 0.0) + hours_add, 1)
    
    # Award 50 XP per focus block
    st.session_state["user_xp"] = st.session_state.get("user_xp", 1450) + 50
    
    if not st.session_state.get("checked_in_today", False):
        st.session_state["study_streak"] = st.session_state.get("study_streak", 12) + 1
        st.session_state["checked_in_today"] = True
        
    save_user_data()

def toggle_task_status(task_id: int):
    """Toggle completed status of a study task and save."""
    for task in st.session_state["study_tasks"]:
        if task["id"] == task_id:
            task["completed"] = not task["completed"]
            if task["completed"]:
                st.session_state["tasks_completed_count"] += 1
                add_xp(25) # 25 XP per completed task
            else:
                st.session_state["tasks_completed_count"] = max(0, st.session_state["tasks_completed_count"] - 1)
            break
    save_user_data()

def add_study_task(subject: str, title: str, hours: float):
    """Add a new task to study planner and save."""
    new_id = max([t.get("id", 0) for t in st.session_state["study_tasks"]], default=0) + 1
    new_task = {
        "id": new_id,
        "subject": subject,
        "title": title,
        "hours": hours,
        "completed": False,
        "date": str(date.today())
    }
    st.session_state["study_tasks"].append(new_task)
    save_user_data()

def update_study_task(task_id: int, title: str, subject: str, hours: float):
    """Edit an existing study task."""
    for task in st.session_state["study_tasks"]:
        if task["id"] == task_id:
            task["title"] = title
            task["subject"] = subject
            task["hours"] = hours
            break
    save_user_data()

def delete_study_task(task_id: int):
    """Delete a task from study planner."""
    st.session_state["study_tasks"] = [t for t in st.session_state["study_tasks"] if t["id"] != task_id]
    save_user_data()
