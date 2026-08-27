"""
Kairo — AI Career Roadmap Module
Generates personalized step-by-step career milestones, project guides, editable milestones, and PDF export for students.
"""

import streamlit as st
from utils.ai_helper import generate_career_roadmap_ai
from utils.pdf_helper import generate_roadmap_pdf
from utils.storage_helper import save_user_data

DREAM_ROLES = [
    "AI / ML Engineer",
    "Full-Stack Web Developer",
    "Data Scientist",
    "Cloud & DevOps Engineer",
    "Cybersecurity Analyst",
    "Mobile App Developer (iOS/Android)",
    "Backend Systems Engineer"
]

def render_career_roadmap():
    st.markdown(
        """
        <div class="kairo-header page-enter">
            <div>
                <h1 class="kairo-title">🚀 AI Career Roadmap</h1>
                <p class="kairo-tagline">Map out your journey from university coursework to your dream tech role.</p>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    col_in, col_out = st.columns([1, 1.3])

    with col_in:
        st.markdown(
            """
            <div class="glass-card page-enter">
                <h3 style="color: var(--primary-accent); margin-top: 0;">🎯 Define Your Career Goal</h3>
            """,
            unsafe_allow_html=True
        )

        with st.form("career_roadmap_form"):
            current_year = st.selectbox("Current Academic Year", ["1st Year (Freshman)", "2nd Year (Sophomore)", "3rd Year (Junior)", "4th Year (Senior)"])
            known_skills = st.text_area("Skills You Already Know", "Python, HTML/CSS, Basic Data Structures, Git")
            dream_role = st.selectbox("Target Dream Role", DREAM_ROLES)
            target_timeline = st.select_slider("Target Timeline to Job Readiness", ["6 Months", "1 Year", "2 Years"])

            generate_roadmap_btn = st.form_submit_button("⚡ Generate AI Roadmap", use_container_width=True)

        st.markdown("</div>", unsafe_allow_html=True)

        if generate_roadmap_btn:
            with st.spinner(f"🤖 Synthesizing personalized Kairo roadmap for {dream_role}..."):
                roadmap = generate_career_roadmap_ai(current_year, known_skills, dream_role)
                st.session_state["career_roadmap"] = roadmap
                save_user_data()
                st.success("Roadmap generated!")
                st.rerun()

    with col_out:
        roadmap = st.session_state.get("career_roadmap")

        if not roadmap:
            st.markdown(
                """
                <div class="glass-card page-enter" style="text-align: center; padding: 3rem 1.5rem;">
                    <div style="font-size: 3rem; margin-bottom: 1rem;">🗺️</div>
                    <h3 style="color: #f8fafc;">Your Career Roadmap Awaits</h3>
                    <p style="color: #94a3b8;">Enter your current academic year, existing skills, and target role on the left to build your tailored milestone map.</p>
                </div>
                """,
                unsafe_allow_html=True
            )
        else:
            goal_title = roadmap.get("title", f"Roadmap for {roadmap.get('career_goal', 'Target Role')}")
            st.markdown(f"<h3 style='color: var(--primary-accent);'>📌 {goal_title}</h3>", unsafe_allow_html=True)

            # Export Roadmap to PDF
            user_name = st.session_state.get("user_name", "Student")
            try:
                pdf_bytes = generate_roadmap_pdf(roadmap, user_name)
                st.download_button(
                    label="📥 Download Career Roadmap PDF",
                    data=pdf_bytes,
                    file_name="kairo_career_roadmap.pdf",
                    mime="application/pdf",
                    use_container_width=True
                )
            except Exception as e:
                st.error(f"Error generating PDF: {e}")

            st.markdown("<br>", unsafe_allow_html=True)

            phases = roadmap.get("phases", [])
            for idx, phase in enumerate(phases):
                p_name = phase.get("phase_title") or phase.get("phase", f"Phase {idx+1}")
                duration = phase.get("duration") or phase.get("timeframe", "3 Months")
                skills = phase.get("key_skills", "Core Concepts & Practical Labs")
                
                st.markdown(
                    f"""
                    <div class="roadmap-phase stagger-item">
                        <div style="display: flex; justify-content: space-between; align-items: center;">
                            <h4 style="color: #f8fafc; margin: 0;">{p_name}</h4>
                            <span style="background: rgba(var(--accent-rgb), 0.15); color: var(--primary-accent); padding: 2px 10px; border-radius: 12px; font-size: 0.8rem; font-weight: 600;">
                                ⏱️ {duration}
                            </span>
                        </div>
                        <p style="color: var(--primary-accent); font-size: 0.88rem; margin: 6px 0;"><b>Target Skills:</b> {skills}</p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
