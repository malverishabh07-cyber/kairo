"""
=============================================================================
Kairo — Flow State Study & AI Productivity
Futuristic AI-powered productivity platform for students.
=============================================================================
"""

import os
import streamlit as st

# 1. Page Configuration
st.set_page_config(
    page_title="Kairo — Flow State Study & AI Productivity",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Initialize Session State & Auth Early
from utils.responsive_helper import inject_responsive_classes
from utils.storage_helper import init_session_state
from utils.auth_helper import render_sidebar_account, render_login_modal

inject_responsive_classes()
init_session_state()

# 3. Inject CSS Design Systems, Custom Cursor & Theme Preset
def load_assets():
    base_dir = os.path.dirname(__file__)
    active_theme = st.session_state.get("theme_preset", "cyan_violet")
    
    # Load Core & Animation CSS
    for css_file in ["style.css", "animations.css"]:
        css_path = os.path.join(base_dir, "assets", css_file)
        if os.path.exists(css_path):
            with open(css_path, "r", encoding="utf-8") as f:
                st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

    # Inject Active Theme Body Class
    st.markdown(
        f"""
        <script>
            document.body.className = 'theme-{active_theme}';
        </script>
        """,
        unsafe_allow_html=True
    )
                
    # Inject JavaScript Interactions & Physics Overlay
    js_path = os.path.join(base_dir, "assets", "interactions.js")
    if os.path.exists(js_path):
        with open(js_path, "r", encoding="utf-8") as f:
            st.components.v1.html(f"<script>{f.read()}</script>", height=0, width=0)

load_assets()

# 4. Auth Modal Gate
if st.session_state.get("auth_show_modal", False):
    render_login_modal()

# 5. Import Page Modules
from modules.dashboard import render_dashboard
from modules.timer import render_timer
from modules.ai_assistant import render_ai_assistant
from modules.study_planner import render_study_planner
from modules.quiz_generator import render_quiz_generator
from modules.resume_builder import render_resume_builder
from modules.career_roadmap import render_career_roadmap
from modules.analytics import render_analytics
from modules.settings import render_settings

# 6. Navigation Options
NAV_OPTIONS = [
    "🏠 Dashboard",
    "⏱️ Focus Timer",
    "🤖 AI Assistant",
    "📚 Study Planner",
    "📝 Quiz Generator",
    "📄 Resume Builder",
    "🚀 AI Career Roadmap",
    "📊 Analytics",
    "⚙️ Settings"
]

if "nav_selection" not in st.session_state:
    st.session_state["nav_selection"] = "🏠 Dashboard"

# 7. Sidebar Rendering
with st.sidebar:
    st.markdown(
        """
        <div style="text-align: center; padding: 1.2rem 0 0.8rem;">
            <div style="font-size: 2.2rem; margin-bottom: 0px;" class="flame-icon">⚡</div>
            <h2 style="font-family: 'Outfit', sans-serif; font-weight: 900; background: var(--grad-primary); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin: 0; letter-spacing: -0.02em;">Kairo</h2>
            <p style="font-size: 0.78rem; color: #94a3b8; margin-top: 2px;">Flow State Study & AI Productivity</p>
        </div>
        <hr style="border-color: rgba(56, 189, 248, 0.15); margin-top: 0;">
        """,
        unsafe_allow_html=True
    )

    selected_page = st.radio(
        label="Navigation Menu",
        options=NAV_OPTIONS,
        index=NAV_OPTIONS.index(st.session_state["nav_selection"]) if st.session_state["nav_selection"] in NAV_OPTIONS else 0,
        label_visibility="collapsed"
    )
    st.session_state["nav_selection"] = selected_page

    # User Account Widget
    render_sidebar_account()

    st.markdown(
        """
        <div style="background: rgba(22, 31, 51, 0.7); border: 1px solid var(--border-glass); border-radius: 12px; padding: 10px; text-align: center; margin-top: 10px;">
            <div style="font-size: 0.78rem; color: var(--primary-accent); font-weight: 600;">🧠 AI Engine Status</div>
            <div style="font-size: 0.72rem; color: #94a3b8; margin-top: 2px;">Gemini 1.5 Flash Active</div>
            <div style="font-size: 0.7rem; color: #10b981; margin-top: 2px;">🟢 Flow Guardrails Operational</div>
        </div>
        <div style="text-align: center; font-size: 0.72rem; color: #64748b; margin-top: 0.8rem;">
            Kairo v3.0 • Focus, Themes & Motion
        </div>
        """,
        unsafe_allow_html=True
    )

# 8. Page Router
st.markdown("<div class='page-enter'>", unsafe_allow_html=True)
if selected_page == "🏠 Dashboard":
    render_dashboard()
elif selected_page == "⏱️ Focus Timer":
    render_timer()
elif selected_page == "🤖 AI Assistant":
    render_ai_assistant()
elif selected_page == "📚 Study Planner":
    render_study_planner()
elif selected_page == "📝 Quiz Generator":
    render_quiz_generator()
elif selected_page == "📄 Resume Builder":
    render_resume_builder()
elif selected_page == "🚀 AI Career Roadmap":
    render_career_roadmap()
elif selected_page == "📊 Analytics":
    render_analytics()
elif selected_page == "⚙️ Settings":
    render_settings()
st.markdown("</div>", unsafe_allow_html=True)

# 9. Persistent Floating AI Assistant Quick Launcher across all pages
st.markdown(
    """
    <div class="floating-ai-launcher" onclick="window.location.hash='#ai-assistant';" title="Open Kairo AI Mentor">
        🤖
        <div class="floating-ai-dot"></div>
    </div>
    """,
    unsafe_allow_html=True
)
