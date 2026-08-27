"""
Kairo — Dashboard Hub
Main hub with welcome card, user profile, XP/Streak metrics, schedule, chart preview & quick actions.
"""

import streamlit as st
import plotly.express as px
import pandas as pd
from utils.storage_helper import toggle_task_status, add_xp

QUOTES = [
    "\"The secret of getting ahead is getting started.\" — Mark Twain",
    "\"Success is the sum of small efforts, repeated day in and day out.\" — Robert Collier",
    "\"The future belongs to those who prepare for it today.\" — Malcolm X",
    "\"Don't count the days, make the days count.\" — Muhammad Ali",
    "\"Your focus determines your reality.\" — Star Wars",
    "\"Flow is the state in which people are so involved in an activity that nothing else seems to matter.\" — Mihaly Csikszentmihalyi"
]

def render_dashboard():
    user_name = st.session_state.get("user_name", "Student")
    school = st.session_state.get("user_school", "Stanford University")
    major = st.session_state.get("user_major", "Computer Science")

    st.markdown(
        f"""
        <div class="kairo-header page-enter">
            <div>
                <h1 class="kairo-title">Welcome back, {user_name}! ⚡</h1>
                <p class="kairo-tagline">Enter flow state, track your daily focus, and master your subjects with Kairo.</p>
            </div>
            <div style="text-align: right; display: flex; align-items: flex-end;">
                <span style="background: rgba(var(--accent-rgb), 0.15); color: var(--primary-accent); padding: 4px 12px; border-radius: 20px; font-size: 0.85rem; font-weight: 600; border: 1px solid rgba(var(--accent-rgb), 0.3);">
                    🎓 {major} @ {school}
                </span>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Top Metrics Grid with Stagger Animation
    m1, m2, m3, m4 = st.columns(4)

    streak = st.session_state.get("study_streak", 12)
    xp = st.session_state.get("user_xp", 1450)
    hours = st.session_state.get("total_study_hours", 42.5)
    tasks_done = st.session_state.get("tasks_completed_count", 28)

    with m1:
        st.markdown(
            f"""
            <div class="metric-card stagger-item">
                <div class="metric-val" style="color: var(--color-streak); background: none; -webkit-text-fill-color: var(--color-streak);"><span class="flame-icon">🔥</span> {streak} Days</div>
                <div class="metric-lbl">Daily Flow Streak</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with m2:
        st.markdown(
            f"""
            <div class="metric-card stagger-item">
                <div class="metric-val" style="color: var(--color-xp); background: none; -webkit-text-fill-color: var(--color-xp);">⚡ {xp:,} XP</div>
                <div class="metric-lbl">Total Mastery XP</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with m3:
        st.markdown(
            f"""
            <div class="metric-card stagger-item">
                <div class="metric-val">⏱️ {hours} hrs</div>
                <div class="metric-lbl">Total Focused Hours</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with m4:
        st.markdown(
            f"""
            <div class="metric-card stagger-item">
                <div class="metric-val">✅ {tasks_done}</div>
                <div class="metric-lbl">Tasks Completed</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown("<br>", unsafe_allow_html=True)

    # Daily Check-in Banner
    c_check1, c_check2 = st.columns([3, 1])
    with c_check1:
        checked = st.session_state.get("checked_in_today", False)
        if checked:
            st.success("✨ Great job! You've checked in today and kept your streak alive!")
        else:
            st.info("⚡ Ready to start studying? Click check-in to boost your streak & earn +25 XP today!")
    with c_check2:
        if not checked:
            if st.button("🔥 Daily Check-in", use_container_width=True):
                st.session_state["study_streak"] += 1
                st.session_state["checked_in_today"] = True
                add_xp(25)
                st.rerun()

    # Main Grid (Left: Today's Schedule & Quick Actions | Right: Productivity Chart & Quote)
    col_left, col_right = st.columns([1.1, 0.9])

    with col_left:
        st.subheader("📅 Today's Schedule & Focus Tasks")
        tasks = st.session_state.get("study_tasks", [])
        
        if not tasks:
            st.info("No study tasks scheduled for today. Head to Study Planner to generate your plan!")
        else:
            for task in tasks:
                t_id = task["id"]
                completed = task["completed"]
                subj = task["subject"]
                title = task["title"]
                hrs = task["hours"]

                t_col1, t_col2 = st.columns([0.85, 0.15])
                with t_col1:
                    st.markdown(
                        f"""
                        <div class="task-item stagger-item">
                            <div>
                                <span style="font-weight: 700; color: var(--primary-accent);">[{subj}]</span> 
                                <span style="color: {'#94a3b8' if completed else '#f8fafc'}; text-decoration: {'line-through' if completed else 'none'};">{title}</span>
                            </div>
                            <span style="font-size: 0.82rem; color: var(--primary-accent); background: rgba(var(--accent-rgb),0.1); padding: 2px 8px; border-radius: 6px;">{hrs} hrs</span>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
                with t_col2:
                    btn_label = "Undo" if completed else "Done"
                    if st.button(btn_label, key=f"dash_task_{t_id}"):
                        toggle_task_status(t_id)
                        st.rerun()

        st.markdown("<br>", unsafe_allow_html=True)
        st.subheader("⚡ Quick Actions")
        q1, q2, q3, q4 = st.columns(4)
        with q1:
            if st.button("⏱️ Focus Timer", use_container_width=True):
                st.session_state["nav_selection"] = "⏱️ Focus Timer"
                st.rerun()
        with q2:
            if st.button("🤖 AI Assistant", use_container_width=True):
                st.session_state["nav_selection"] = "🤖 AI Assistant"
                st.rerun()
        with q3:
            if st.button("📚 Study Planner", use_container_width=True):
                st.session_state["nav_selection"] = "📚 Study Planner"
                st.rerun()
        with q4:
            if st.button("📝 Quiz Gen", use_container_width=True):
                st.session_state["nav_selection"] = "📝 Quiz Generator"
                st.rerun()

    with col_right:
        st.subheader("📈 Weekly Focus Hours")
        df_chart = pd.DataFrame({
            "Day": ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
            "Hours": [3.5, 4.0, 5.2, 3.8, 6.0, 4.5, 5.0]
        })
        fig = px.bar(
            df_chart, 
            x="Day", 
            y="Hours", 
            text="Hours",
            color="Hours",
            color_continuous_scale=["#00f2fe", "#7f00ff"]
        )
        fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font_color='#94a3b8',
            margin=dict(l=10, r=10, t=10, b=10),
            height=210,
            showlegend=False
        )
        fig.update_traces(marker_line_color='rgba(0,242,254,0.3)', marker_line_width=1.5, textposition='outside')
        st.plotly_chart(fig, use_container_width=True)

        st.subheader("💬 Daily Inspiration")
        if "quote_index" not in st.session_state:
            st.session_state["quote_index"] = 0
        current_quote = QUOTES[st.session_state["quote_index"]]
        
        st.markdown(
            f"""
            <div class="quote-card page-enter">
                {current_quote}
            </div>
            """,
            unsafe_allow_html=True
        )
        
        if st.button("🔄 Refresh Quote", key="refresh_quote_btn"):
            st.session_state["quote_index"] = (st.session_state["quote_index"] + 1) % len(QUOTES)
            st.rerun()
