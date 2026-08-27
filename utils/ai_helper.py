"""
Kairo — AI Helper Engine
Handles Google Gemini API integration, prompt caching, rate limiting, student guardrails, and fallback generators.
"""

import os
import json
import time
import random
import streamlit as st

try:
    import google.generativeai as genai
    HAS_GENAI = True
except ImportError:
    HAS_GENAI = False

# Prompt Cache to prevent unnecessary quota usage
_AI_CACHE = {}
_LAST_CALL_TIMESTAMP = 0.0
COOLDOWN_SECONDS = 2.0

def check_rate_limit() -> bool:
    """Ensure a minimum cooldown interval between API calls."""
    global _LAST_CALL_TIMESTAMP
    now = time.time()
    if now - _LAST_CALL_TIMESTAMP < COOLDOWN_SECONDS:
        return False
    _LAST_CALL_TIMESTAMP = now
    return True

def get_configured_api_key():
    """Retrieve Gemini API key from session state or environment variables."""
    key = st.session_state.get("gemini_api_key", "").strip()
    if not key:
        key = os.environ.get("GEMINI_API_KEY", "").strip()
    return key

def is_off_topic_or_inappropriate(prompt: str) -> bool:
    """Check if a user prompt violates student academic guardrails."""
    lower_p = prompt.lower()
    inappropriate_keywords = [
        "hack bank", "illegal", "bomb", "weapon", "steal credit card", "bypass malware", "nsfw", "gambling"
    ]
    for kw in inappropriate_keywords:
        if kw in lower_p:
            return True
    return False

def generate_ai_chat_response(prompt: str, chat_history: list = None) -> str:
    """Generate response for AI Assistant with student academic guardrails."""
    prompt_clean = prompt.strip()
    
    # 1. Guardrail Check
    if is_off_topic_or_inappropriate(prompt_clean):
        return (
            "### 🛡️ Kairo Academic Guardrail\n"
            "I am **Kairo AI**, your dedicated academic & career mentor. "
            "I am designed to assist with study planning, subject revision, programming concepts, resume building, and career guidance. "
            "Please ask a question related to your studies or career goals!"
        )

    # 2. Cache Check
    cache_key = f"chat_{prompt_clean}"
    if cache_key in _AI_CACHE:
        return _AI_CACHE[cache_key]

    api_key = get_configured_api_key()
    if api_key and HAS_GENAI and check_rate_limit():
        try:
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel("gemini-1.5-flash")
            
            system_instruction = (
                "You are Kairo AI, an encouraging, high-performance academic and career mentor for students. "
                "Maintain focus strictly on education, technical skills, study methods, and career advice. "
                "Provide clear, structured markdown responses with code blocks and bullet points."
            )
            full_prompt = f"{system_instruction}\n\nUser Question: {prompt_clean}"
            
            response = model.generate_content(full_prompt)
            if response and response.text:
                res_text = response.text.strip()
                _AI_CACHE[cache_key] = res_text
                return res_text
        except Exception:
            pass

    # 3. Intelligent Fallback Response
    lower_p = prompt_clean.lower()
    if "python" in lower_p or "code" in lower_p:
        res = (
            "### 🐍 Python & Coding Assistance\n"
            "Here is an optimized implementation pattern for your study problem:\n\n"
            "```python\n"
            "# Kairo Algorithm Pattern\n"
            "def optimize_study_schedule(topics, available_hours):\n"
            "    # Sort topics by difficulty weight\n"
            "    priority_queue = sorted(topics, key=lambda x: x.get('difficulty', 1), reverse=True)\n"
            "    schedule = []\n"
            "    for t in priority_queue:\n"
            "        hrs = min(2.0, available_hours * 0.35)\n"
            "        schedule.append({'topic': t['name'], 'allocated_hours': round(hrs, 1)})\n"
            "    return schedule\n"
            "```\n\n"
            "**Key Tips:**\n"
            "- Break complex problems into modular helper functions.\n"
            "- Use explicit type hints and docstrings for clean maintainable code."
        )
    elif "study" in lower_p or "exam" in lower_p or "schedule" in lower_p or "pomodoro" in lower_p or "timer" in lower_p:
        res = (
            "### 📚 Active Recall & Spaced Repetition Strategy\n"
            "To maximize retention and enter deep flow state:\n\n"
            "1. **Pomodoro Blocks**: Study intensely for 25–50 minutes using the Kairo Focus Timer, then rest completely.\n"
            "2. **Feynman Technique**: Explain concepts out loud in simple terms as if teaching a peer.\n"
            "3. **Self-Testing**: Attempt active practice quizzes before reviewing raw notes."
        )
    else:
        res = (
            f"### 💡 Kairo Study Insight\n"
            f"Great inquiry regarding **\"{prompt_clean[:40]}...\"**!\n\n"
            f"**Recommended Action Steps:**\n"
            f"- **Deconstruct core principles**: Identify foundational equations or definitions.\n"
            f"- **Hands-on practice**: Solve 2-3 step-by-step example exercises.\n"
            f"- **Summary synthesis**: Write down 3 key takeaways for quick exam revision.\n\n"
            f"*Tip: Configure your Gemini API Key in Settings to enable unlimited live AI responses!*"
        )

    _AI_CACHE[cache_key] = res
    return res

def generate_study_plan_ai(subjects: str, exam_date: str, hours_per_day: float) -> list:
    """Generate structured study plan tasks for editable Study Planner."""
    cache_key = f"plan_{subjects}_{exam_date}_{hours_per_day}"
    if cache_key in _AI_CACHE:
        return _AI_CACHE[cache_key]

    api_key = get_configured_api_key()
    if api_key and HAS_GENAI and check_rate_limit():
        try:
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel("gemini-1.5-flash")
            prompt = (
                f"Create a JSON list of 4 study tasks for subjects: {subjects}. Target date is {exam_date}. "
                f"Daily hours: {hours_per_day}. Return valid JSON array of objects with keys: subject, title, hours."
            )
            res = model.generate_content(prompt)
            clean_json = res.text.replace("```json", "").replace("```", "").strip()
            tasks_data = json.loads(clean_json)
            formatted_tasks = []
            for idx, item in enumerate(tasks_data, 1):
                formatted_tasks.append({
                    "id": random.randint(100, 999),
                    "subject": item.get("subject", subjects.split(",")[0].strip()),
                    "title": item.get("title", f"Review core concepts in {item.get('subject', 'module')}"),
                    "hours": float(item.get("hours", 1.5)),
                    "completed": False,
                    "date": str(exam_date)
                })
            _AI_CACHE[cache_key] = formatted_tasks
            return formatted_tasks
        except Exception:
            pass

    # Built-in structured fallback tasks
    subj_list = [s.strip() for s in subjects.split(",") if s.strip()]
    if not subj_list:
        subj_list = ["Computer Science", "Mathematics", "Physics"]

    tasks = [
        {"id": random.randint(1000, 9999), "subject": subj_list[0 % len(subj_list)], "title": f"[{subj_list[0 % len(subj_list)]}] Deep dive theoretical concepts & formulas", "hours": round(hours_per_day * 0.4, 1), "completed": False, "date": str(exam_date)},
        {"id": random.randint(1000, 9999), "subject": subj_list[1 % len(subj_list)], "title": f"[{subj_list[1 % len(subj_list)]}] Solve 5 practice problem sets", "hours": round(hours_per_day * 0.3, 1), "completed": False, "date": str(exam_date)},
        {"id": random.randint(1000, 9999), "subject": subj_list[2 % len(subj_list)], "title": f"[{subj_list[2 % len(subj_list)]}] Summarize core notes into a 1-page cheatsheet", "hours": round(hours_per_day * 0.2, 1), "completed": False, "date": str(exam_date)},
        {"id": random.randint(1000, 9999), "subject": subj_list[0 % len(subj_list)], "title": f"[{subj_list[0 % len(subj_list)]}] Complete practice quiz & revise mistakes", "hours": round(hours_per_day * 0.1, 1), "completed": False, "date": str(exam_date)},
    ]
    _AI_CACHE[cache_key] = tasks
    return tasks

def generate_mcq_quiz(subject: str, topic: str, difficulty: str, num_questions: int = 4) -> list:
    """Generate multiple choice questions for editable Quiz Generator."""
    cache_key = f"quiz_{subject}_{topic}_{difficulty}_{num_questions}"
    if cache_key in _AI_CACHE:
        return _AI_CACHE[cache_key]

    api_key = get_configured_api_key()
    if api_key and HAS_GENAI and check_rate_limit():
        try:
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel("gemini-1.5-flash")
            prompt = (
                f"Generate a {difficulty} MCQ quiz on subject '{subject}' and topic '{topic}'. "
                f"Generate {num_questions} questions. Return strictly a JSON array of objects with keys: "
                f"question, options (array of 4 strings), correct_index (0-3 integer), explanation."
            )
            res = model.generate_content(prompt)
            clean_json = res.text.replace("```json", "").replace("```", "").strip()
            quiz_res = json.loads(clean_json)
            _AI_CACHE[cache_key] = quiz_res
            return quiz_res
        except Exception:
            pass

    # Built-in realistic fallback questions
    quiz_res = [
        {
            "question": f"In {subject} ({topic}), what does time complexity (Big-O) measure?",
            "options": [
                "Exact wall-clock execution time in milliseconds",
                "How algorithm resource requirements scale relative to input size N",
                "The number of lines of source code in the file",
                "Compiler optimization speed"
            ],
            "correct_index": 1,
            "explanation": "Big-O notation describes the limiting behavior and asymptotic growth rate of an algorithm as input size N grows."
        },
        {
            "question": f"Which data structure operates under the First-In, First-Out (FIFO) rule in {subject}?",
            "options": [
                "Stack",
                "Queue",
                "Binary Search Tree",
                "Priority Heap"
            ],
            "correct_index": 1,
            "explanation": "A Queue processes elements in FIFO order: elements enter at the back and exit from the front."
        },
        {
            "question": f"In a balanced Binary Search Tree, what is the search time complexity?",
            "options": [
                "O(1)",
                "O(N)",
                "O(log N)",
                "O(N log N)"
            ],
            "correct_index": 2,
            "explanation": "Balanced BSTs halve the search space at each step, yielding logarithmic search time O(log N)."
        },
        {
            "question": "Which software engineering practice prevents accidental mutation of private object state?",
            "options": [
                "Encapsulation and immutability",
                "Global variable access everywhere",
                "Infinite recursive loop execution",
                "Disabling runtime exception checks"
            ],
            "correct_index": 0,
            "explanation": "Encapsulation restricts direct state access, enforcing clean interface contracts."
        }
    ]
    _AI_CACHE[cache_key] = quiz_res
    return quiz_res

def generate_career_roadmap_ai(year: str, skills: str, dream_role: str) -> dict:
    """Generate step-by-step career roadmap for editable Career Roadmap module."""
    cache_key = f"roadmap_{year}_{skills}_{dream_role}"
    if cache_key in _AI_CACHE:
        return _AI_CACHE[cache_key]

    api_key = get_configured_api_key()
    if api_key and HAS_GENAI and check_rate_limit():
        try:
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel("gemini-1.5-flash")
            prompt = (
                f"Create a career roadmap for a {year} student who knows '{skills}' and aims to become a '{dream_role}'. "
                f"Return JSON object with keys: career_goal, phases (list of objects with phase, timeframe, milestones (list of objects with title, desc))."
            )
            res = model.generate_content(prompt)
            clean_json = res.text.replace("```json", "").replace("```", "").strip()
            roadmap_res = json.loads(clean_json)
            _AI_CACHE[cache_key] = roadmap_res
            return roadmap_res
        except Exception:
            pass

    # Built-in structured fallback roadmap
    roadmap_res = {
        "career_goal": dream_role if dream_role else "Software Engineer",
        "phases": [
            {
                "phase": "Phase 1: Core Technical Foundations",
                "timeframe": "Months 1-3",
                "milestones": [
                    {"title": f"Master {skills if skills else 'Core Programming'} & Data Structures", "desc": "Solve 100+ algorithmic problems on LeetCode/HackerRank."},
                    {"title": "Version Control & Git Workflow", "desc": "Master Git branching, pull requests, and GitHub project management."}
                ]
            },
            {
                "phase": f"Phase 2: Specialization for {dream_role}",
                "timeframe": "Months 4-6",
                "milestones": [
                    {"title": f"Build Flagship {dream_role} Application", "desc": "Develop a full-stack project featuring authentication and API integration."},
                    {"title": "Containerization & CI/CD", "desc": "Dockerize application and build GitHub Actions deployment workflow."}
                ]
            },
            {
                "phase": "Phase 3: Portfolio & Technical Interviews",
                "timeframe": "Months 7-12",
                "milestones": [
                    {"title": "System Design & Mock Interviews", "desc": "Practice scalable system architecture and complete peer mock interviews."},
                    {"title": "Resume & LinkedIn Optimization", "desc": "Polish resume with measurable project impacts and apply to target roles."}
                ]
            }
        ]
    }
    _AI_CACHE[cache_key] = roadmap_res
    return roadmap_res
