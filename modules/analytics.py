"""
Kairo — Analytics & Learning Insights
Interactive Plotly charts for study hours, focus sessions, quiz mastery, task completion & XP velocity.
"""

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

def render_analytics():
    st.markdown(
        """
        <div class="kairo-header page-enter">
            <div>
                <h1 class="kairo-title">📊 Kairo Learning & Focus Analytics</h1>
                <p class="kairo-tagline">Visualize your deep flow trends, focus blocks, mastery radar, and XP velocity.</p>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    tasks = st.session_state.get("study_tasks", [])
    completed_count = sum(1 for t in tasks if t["completed"])
    total_count = len(tasks)
    completion_rate = round((completed_count / total_count * 100), 1) if total_count > 0 else 87.5

    quiz_history = st.session_state.get("quiz_history", [])
    if quiz_history:
        quiz_mastery = round(sum((q["score"] / q["total"]) * 100 for q in quiz_history) / len(quiz_history), 1)
    else:
        quiz_mastery = 90.0

    hours = st.session_state.get("total_study_hours", 42.5)
    sessions = st.session_state.get("focus_sessions_completed", 16)
    xp = st.session_state.get("user_xp", 1450)

    # Top Metric Banner with Stagger Animation
    a1, a2, a3, a4 = st.columns(4)
    with a1:
        st.markdown(
            f"""
            <div class="metric-card stagger-item">
                <div class="metric-val">⏱️ {hours} hrs</div>
                <div class="metric-lbl">Total Focus Hours</div>
            </div>
            """,
            unsafe_allow_html=True
        )
    with a2:
        st.markdown(
            f"""
            <div class="metric-card stagger-item">
                <div class="metric-val">🧘 {sessions} Blocks</div>
                <div class="metric-lbl">Focus Sessions Done</div>
            </div>
            """,
            unsafe_allow_html=True
        )
    with a3:
        st.markdown(
            f"""
            <div class="metric-card stagger-item">
                <div class="metric-val">⚡ {xp:,} XP</div>
                <div class="metric-lbl">Total Mastery XP</div>
            </div>
            """,
            unsafe_allow_html=True
        )
    with a4:
        st.markdown(
            f"""
            <div class="metric-card stagger-item">
                <div class="metric-val">🎯 {quiz_mastery}%</div>
                <div class="metric-lbl">Avg Quiz Mastery</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown("<br>", unsafe_allow_html=True)

    # Main Chart Grid (Row 1)
    col_chart1, col_chart2 = st.columns(2)

    with col_chart1:
        st.subheader("⏱️ Weekly Focus Hours Distribution")
        df_weekly = pd.DataFrame({
            "Day": ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
            "Hours": [3.5, 4.0, 5.2, 3.8, 6.0, 4.5, 5.0],
            "Target": [4.0, 4.0, 4.0, 4.0, 4.0, 4.0, 4.0]
        })
        fig_weekly = px.bar(
            df_weekly,
            x="Day",
            y="Hours",
            title="Actual vs Target Hours",
            color="Hours",
            color_continuous_scale=["#00f2fe", "#7f00ff"]
        )
        fig_weekly.add_trace(
            go.Scatter(x=df_weekly["Day"], y=df_weekly["Target"], name="Daily Goal", line=dict(color="#00f2fe", width=3, dash="dash"))
        )
        fig_weekly.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font_color='#94a3b8',
            height=320,
            margin=dict(l=20, r=20, t=40, b=20)
        )
        st.plotly_chart(fig_weekly, use_container_width=True)

    with col_chart2:
        st.subheader("🎯 Subject Mastery Radar")
        categories = ["Algorithms", "OS Systems", "Machine Learning", "Linear Algebra", "Python Dev", "Database Design"]
        scores = [92, 85, 95, 78, 96, 88]

        fig_radar = go.Figure()
        fig_radar.add_trace(go.Scatterpolar(
            r=scores + [scores[0]],
            theta=categories + [categories[0]],
            fill='toself',
            fillcolor='rgba(0, 242, 254, 0.25)',
            line=dict(color='#00f2fe', width=2),
            name='Mastery %'
        ))
        fig_radar.update_layout(
            polar=dict(
                radialaxis=dict(visible=True, range=[0, 100], color='#94a3b8'),
                bgcolor='rgba(0,0,0,0)'
            ),
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='#94a3b8',
            height=320,
            margin=dict(l=40, r=40, t=40, b=20),
            showlegend=False
        )
        st.plotly_chart(fig_radar, use_container_width=True)

    # Row 2 Charts
    col_chart3, col_chart4 = st.columns(2)

    with col_chart3:
        st.subheader("📈 Task Completion Velocity")
        df_tasks_trend = pd.DataFrame({
            "Week": ["Week 1", "Week 2", "Week 3", "Week 4"],
            "Completed": [12, 18, 24, max(28, completed_count)]
        })
        fig_trend = px.area(
            df_tasks_trend,
            x="Week",
            y="Completed",
            markers=True,
            color_discrete_sequence=["#8b5cf6"]
        )
        fig_trend.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font_color='#94a3b8',
            height=300,
            margin=dict(l=20, r=20, t=20, b=20)
        )
        st.plotly_chart(fig_trend, use_container_width=True)

    with col_chart4:
        st.subheader("⚡ Overall Productivity Index")
        fig_gauge = go.Figure(go.Indicator(
            mode = "gauge+number",
            value = 95,
            domain = {'x': [0, 1], 'y': [0, 1]},
            title = {'text': "Kairo Flow Index", 'font': {'color': '#f8fafc', 'size': 18}},
            gauge = {
                'axis': {'range': [None, 100], 'tickwidth': 1, 'tickcolor': "#94a3b8"},
                'bar': {'color': "#00f2fe"},
                'bgcolor': "rgba(15, 23, 42, 0.8)",
                'bordercolor': "rgba(56, 189, 248, 0.3)",
                'steps': [
                    {'range': [0, 50], 'color': 'rgba(239, 68, 68, 0.3)'},
                    {'range': [50, 80], 'color': 'rgba(245, 158, 11, 0.3)'},
                    {'range': [80, 100], 'color': 'rgba(16, 185, 129, 0.3)'}
                ]
            }
        ))
        fig_gauge.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='#94a3b8',
            height=300,
            margin=dict(l=30, r=30, t=30, b=20)
        )
        st.plotly_chart(fig_gauge, use_container_width=True)
