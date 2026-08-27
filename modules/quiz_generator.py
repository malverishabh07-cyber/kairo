"""
Kairo — Quiz Generator Module
Generates interactive MCQ quizzes with automated scoring, XP rewards, correct answer explanations, and inline editing.
"""

import streamlit as st
from datetime import date
from utils.ai_helper import generate_mcq_quiz
from utils.storage_helper import save_user_data, add_xp

def render_quiz_generator():
    st.markdown(
        """
        <div class="kairo-header page-enter">
            <div>
                <h1 class="kairo-title">📝 AI Quiz Generator</h1>
                <p class="kairo-tagline">Test your mastery with AI-generated active recall quizzes and earn Flow XP.</p>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    q_col1, q_col2 = st.columns([1, 1.3])

    with q_col1:
        st.markdown(
            """
            <div class="glass-card page-enter">
                <h3 style="color: var(--primary-accent); margin-top: 0;">⚙️ Configure Quiz</h3>
            """,
            unsafe_allow_html=True
        )

        with st.form("quiz_config_form"):
            subject = st.selectbox("Subject Area", ["Data Structures & Algorithms", "Python Programming", "Machine Learning", "Operating Systems", "Computer Networks", "Database Systems"])
            topic = st.text_input("Specific Topic", "Trees, Graphs & Time Complexity")
            difficulty = st.select_slider("Difficulty Level", ["Beginner", "Intermediate", "Advanced"], value="Intermediate")
            num_questions = st.slider("Number of Questions", 2, 6, 4)

            generate_btn = st.form_submit_button("⚡ Generate Quiz", use_container_width=True)

        st.markdown("</div>", unsafe_allow_html=True)

        if generate_btn:
            with st.spinner("🤖 Generating Kairo AI questions..."):
                questions = generate_mcq_quiz(subject, topic, difficulty, num_questions)
                st.session_state["current_quiz"] = {
                    "subject": subject,
                    "topic": topic,
                    "difficulty": difficulty,
                    "questions": questions,
                    "user_answers": {},
                    "submitted": False,
                    "score": 0
                }
                st.rerun()

        # Quiz History Log Card
        st.markdown("<br>", unsafe_allow_html=True)
        st.subheader("📊 Quiz Score History")
        history = st.session_state.get("quiz_history", [])
        if not history:
            st.info("No past quiz records yet.")
        else:
            for item in reversed(history[-4:]):
                score_pct = int((item["score"] / item["total"]) * 100)
                color = "#10b981" if score_pct >= 80 else "#f59e0b"
                st.markdown(
                    f"""
                    <div style="background: rgba(22, 31, 51, 0.6); border: 1px solid var(--border-glass); border-radius: 12px; padding: 10px 14px; margin-bottom: 8px; display: flex; justify-content: space-between; align-items: center;" class="stagger-item">
                        <div>
                            <div style="font-weight: 600; color: #f8fafc;">{item['subject']}</div>
                            <div style="font-size: 0.78rem; color: #94a3b8;">{item['date']}</div>
                        </div>
                        <div style="font-size: 1.1rem; font-weight: 700; color: {color};">
                            {score_pct}% ({item['score']}/{item['total']})
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

    with q_col2:
        current_quiz = st.session_state.get("current_quiz")

        if not current_quiz:
            st.markdown(
                """
                <div class="glass-card page-enter" style="text-align: center; padding: 3rem 1.5rem;">
                    <div style="font-size: 3rem; margin-bottom: 1rem;">🎯</div>
                    <h3 style="color: #f8fafc;">Ready for a Quiz Challenge?</h3>
                    <p style="color: #94a3b8;">Select your subject and topic on the left to generate an AI-powered quiz.</p>
                </div>
                """,
                unsafe_allow_html=True
            )
        else:
            st.markdown(f"<h3 style='color: var(--primary-accent);'>📝 Quiz: {current_quiz['subject']} ({current_quiz['topic']})</h3>", unsafe_allow_html=True)
            st.markdown(f"**Difficulty:** `{current_quiz['difficulty']}` | **Questions:** `{len(current_quiz['questions'])}`")
            
            # Allow tweaking generated questions before submitting
            with st.expander("✏️ Edit Questions & Correct Options"):
                for q_idx, q_item in enumerate(current_quiz["questions"]):
                    q_item["question"] = st.text_input(f"Q{q_idx+1} Question Text", q_item["question"], key=f"edit_q_{q_idx}")
                    q_item["explanation"] = st.text_input(f"Q{q_idx+1} Explanation", q_item["explanation"], key=f"edit_exp_{q_idx}")

            st.markdown("<hr style='border-color: rgba(56,189,248,0.15);'>", unsafe_allow_html=True)

            questions = current_quiz["questions"]
            submitted = current_quiz["submitted"]

            with st.form("quiz_answer_form"):
                user_answers = {}
                for idx, q in enumerate(questions):
                    st.markdown(f"**Q{idx+1}: {q['question']}**")
                    choice = st.radio(
                        label=f"q_{idx}_options",
                        options=q["options"],
                        key=f"q_radio_{idx}",
                        disabled=submitted,
                        label_visibility="collapsed"
                    )
                    user_answers[idx] = q["options"].index(choice) if choice in q["options"] else 0
                    
                    if submitted:
                        correct_idx = q["correct_index"]
                        user_selected_idx = current_quiz["user_answers"].get(idx, 0)
                        if user_selected_idx == correct_idx:
                            st.markdown(
                                f"""
                                <div class="answer-correct" style="padding: 10px 14px; border-radius: 8px; margin-top: 6px;">
                                    <b>✅ Correct!</b> {q['explanation']}
                                </div>
                                """,
                                unsafe_allow_html=True
                            )
                        else:
                            st.markdown(
                                f"""
                                <div class="answer-incorrect" style="padding: 10px 14px; border-radius: 8px; margin-top: 6px;">
                                    <b>❌ Incorrect.</b> Correct answer: <b>{q['options'][correct_idx]}</b><br>{q['explanation']}
                                </div>
                                """,
                                unsafe_allow_html=True
                            )
                    st.markdown("<br>", unsafe_allow_html=True)

                if not submitted:
                    submit_quiz_btn = st.form_submit_button("🏆 Submit Answers", use_container_width=True)
                    if submit_quiz_btn:
                        score = 0
                        for idx, q in enumerate(questions):
                            if user_answers[idx] == q["correct_index"]:
                                score += 1
                        
                        current_quiz["user_answers"] = user_answers
                        current_quiz["submitted"] = True
                        current_quiz["score"] = score
                        
                        # Award XP based on score
                        earned_xp = score * 30
                        add_xp(earned_xp)

                        # Record history & save
                        st.session_state["quiz_history"].append({
                            "subject": f"{current_quiz['subject']} ({current_quiz['topic']})",
                            "score": score,
                            "total": len(questions),
                            "date": str(date.today())
                        })
                        save_user_data()
                        st.rerun()
                else:
                    score = current_quiz["score"]
                    total = len(questions)
                    score_pct = int((score / total) * 100)
                    st.markdown(
                        f"""
                        <div class="glass-card page-enter" style="text-align: center; border-color: var(--primary-accent); margin-top: 1rem;">
                            <h2 style="color: var(--primary-accent); margin: 0;">Quiz Complete! Score: {score}/{total} ({score_pct}%) • +{score * 30} XP</h2>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
                    
                    if st.form_submit_button("🔄 Take Another Quiz", use_container_width=True):
                        st.session_state["current_quiz"] = None
                        st.rerun()
