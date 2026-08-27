"""
Kairo — Study Planner Module
Automated AI study schedule generator with task tracking, inline editing, and PDF export.
"""

import streamlit as st
from datetime import date, timedelta
from utils.ai_helper import generate_study_plan_ai
from utils.storage_helper import toggle_task_status, add_study_task, update_study_task, delete_study_task, save_user_data
from utils.pdf_helper import generate_study_plan_pdf

def render_study_planner():
    st.markdown(
        """
        <div class="kairo-header page-enter">
            <div>
                <h1 class="kairo-title">📚 AI Study Planner</h1>
                <p class="kairo-tagline">Transform your exam goals and course syllabus into actionable daily focus tasks.</p>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    col_form, col_tasks = st.columns([1, 1.2])

    with col_form:
        st.markdown(
            """
            <div class="glass-card page-enter">
                <h3 style="color: var(--primary-accent); margin-top: 0;">⚡ Create AI Study Plan</h3>
            """,
            unsafe_allow_html=True
        )

        with st.form("study_plan_form"):
            subjects_input = st.text_input("Course Subjects (comma separated)", "Data Structures, Operating Systems, Machine Learning")
            exam_date_input = st.date_input("Target Exam / Deadline Date", date.today() + timedelta(days=14))
            hours_input = st.slider("Daily Study Hours Available", 1.0, 10.0, 4.0, 0.5)
            focus_notes = st.text_area("Specific Focus Areas or Weak Points (Optional)", "Focus more on tree traversal and synchronization problems.")
            
            submit_plan = st.form_submit_button("🚀 Generate AI Plan", use_container_width=True)

        st.markdown("</div>", unsafe_allow_html=True)

        if submit_plan:
            with st.spinner("🤖 Generating optimal Kairo AI study schedule..."):
                new_tasks = generate_study_plan_ai(subjects_input, str(exam_date_input), hours_input)
                st.session_state["study_tasks"].extend(new_tasks)
                save_user_data()
                st.success("✨ New study plan generated successfully!")
                st.rerun()

        # Add Manual Custom Task Expander
        with st.expander("➕ Add Custom Task Manually"):
            with st.form("manual_task_form"):
                m_subj = st.text_input("Subject", "General Study")
                m_title = st.text_input("Task Description", "Review course notes")
                m_hrs = st.number_input("Hours", 0.5, 8.0, 1.5, 0.5)
                if st.form_submit_button("Add Task", use_container_width=True):
                    add_study_task(m_subj, m_title, m_hrs)
                    st.success("Task added!")
                    st.rerun()

    with col_tasks:
        st.markdown("<h3 style='color: var(--primary-accent);'>📋 Scheduled Study Tasks</h3>", unsafe_allow_html=True)

        tasks = st.session_state.get("study_tasks", [])
        
        if not tasks:
            st.info("No study tasks found. Fill out the form on the left to generate your custom plan!")
        else:
            # Completion Progress Metrics
            completed_count = sum(1 for t in tasks if t["completed"])
            total_count = len(tasks)
            pct = int((completed_count / total_count) * 100) if total_count > 0 else 0

            st.markdown(f"**Plan Completion:** {completed_count}/{total_count} tasks completed ({pct}%)")
            st.progress(pct / 100.0)

            # Export Study Plan to PDF
            user_name = st.session_state.get("user_name", "Student")
            pdf_bytes = generate_study_plan_pdf(tasks, user_name)
            st.download_button(
                label="📥 Download Study Schedule (PDF)",
                data=pdf_bytes,
                file_name="kairo_study_schedule.pdf",
                mime="application/pdf",
                use_container_width=True
            )

            st.markdown("<br>", unsafe_allow_html=True)

            for task in tasks:
                t_id = task["id"]
                completed = task["completed"]
                subj = task["subject"]
                title = task["title"]
                hrs = task["hours"]
                t_date = task.get("date", "Upcoming")

                c_item, c_toggle, c_delete = st.columns([0.72, 0.16, 0.12])
                with c_item:
                    st.markdown(
                        f"""
                        <div class="task-item stagger-item">
                            <div>
                                <span style="font-weight: 700; color: var(--primary-accent);">[{subj}]</span>
                                <span style="color: {'#94a3b8' if completed else '#f8fafc'}; text-decoration: {'line-through' if completed else 'none'};">{title}</span>
                            </div>
                            <div>
                                <span style="font-size: 0.8rem; color: #94a3b8; margin-right: 8px;">🗓️ {t_date}</span>
                                <span style="font-size: 0.8rem; color: var(--primary-accent); background: rgba(var(--accent-rgb),0.15); padding: 2px 8px; border-radius: 6px;">{hrs} hrs</span>
                            </div>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
                with c_toggle:
                    btn_txt = "Undo" if completed else "Done"
                    if st.button(btn_txt, key=f"plan_task_{t_id}"):
                        toggle_task_status(t_id)
                        st.rerun()
                with c_delete:
                    if st.button("🗑️", key=f"del_task_{t_id}"):
                        delete_study_task(t_id)
                        st.rerun()

            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("🗑️ Clear All Tasks", key="clear_all_tasks_btn"):
                st.session_state["study_tasks"] = []
                save_user_data()
                st.rerun()
