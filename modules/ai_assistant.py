"""
Kairo — AI Assistant Module
Futuristic chat interface powered by Gemini API with session memory, quick prompt chips, and academic guardrails.
"""

import streamlit as st
from utils.ai_helper import generate_ai_chat_response
from utils.storage_helper import save_user_data

PRESET_PROMPTS = [
    "💡 Explain Quantum Entanglement like I'm 10",
    "🐍 How do I optimize a Python loop using vectorization?",
    "📚 Create a 3-step study guide for Organic Chemistry",
    "🎯 Draft an elevator pitch for my AI engineering resume"
]

def render_ai_assistant():
    st.markdown(
        """
        <div class="kairo-header page-enter">
            <div>
                <h1 class="kairo-title">🤖 Kairo AI Mentor & Assistant</h1>
                <p class="kairo-tagline">Ask questions, debug code, synthesize notes, or master complex academic concepts in seconds.</p>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Top Control Bar
    ctrl_col1, ctrl_col2, ctrl_col3 = st.columns([2, 1, 1])
    with ctrl_col1:
        st.markdown("**Session Memory:** Active 🧠 | **Model:** Gemini 1.5 Flash (Academic Guardrails Active)")
    with ctrl_col2:
        chat_text = "\n\n".join([f"{msg['role'].upper()}: {msg['content']}" for msg in st.session_state["chat_messages"]])
        st.download_button(
            label="📥 Download Chat Log",
            data=chat_text,
            file_name="kairo_ai_chat_history.txt",
            mime="text/plain",
            use_container_width=True
        )
    with ctrl_col3:
        if st.button("🗑️ Clear Chat", use_container_width=True):
            st.session_state["chat_messages"] = [
                {"role": "assistant", "content": "Chat history cleared! What topic would you like to explore next?"}
            ]
            save_user_data()
            st.rerun()

    # Preset Quick Prompt Chips
    st.markdown("<p style='font-size: 0.9rem; color: #94a3b8; margin-top: 0.5rem;'>⚡ <b>Quick Prompts:</b></p>", unsafe_allow_html=True)
    chip_cols = st.columns(len(PRESET_PROMPTS))
    selected_preset = None
    for idx, prompt_text in enumerate(PRESET_PROMPTS):
        with chip_cols[idx]:
            if st.button(prompt_text, key=f"preset_btn_{idx}", use_container_width=True):
                selected_preset = prompt_text[2:].strip()

    st.markdown("<hr style='border-color: rgba(56, 189, 248, 0.15); margin: 1rem 0;'>", unsafe_allow_html=True)

    # Render Chat Conversation with Slide/Fade-in Animations
    chat_container = st.container()
    with chat_container:
        for msg in st.session_state["chat_messages"]:
            if msg["role"] == "user":
                st.markdown(
                    f"""
                    <div class="chat-bubble-user page-enter">
                        <b>👤 You:</b><br>{msg['content']}
                    </div>
                    """,
                    unsafe_allow_html=True
                )
            else:
                st.markdown(
                    f"""
                    <div class="chat-bubble-ai page-enter">
                        <span style="background: var(--grad-primary); border-radius: 50%; padding: 4px 8px; font-weight: bold; color: #000; margin-right: 6px;">⚡</span> <b>Kairo AI:</b><br>{msg['content']}
                    </div>
                    """,
                    unsafe_allow_html=True
                )

    # Handle preset trigger or user chat input
    user_input = st.chat_input("Ask Kairo AI anything (e.g. explain Recursion vs Iteration)...")
    prompt_to_send = selected_preset or user_input

    if prompt_to_send:
        # Append User message
        st.session_state["chat_messages"].append({"role": "user", "content": prompt_to_send})
        
        # Display thinking state with animated pulse
        with chat_container:
            st.markdown(
                f"""
                <div class="chat-bubble-user page-enter">
                    <b>👤 You:</b><br>{prompt_to_send}
                </div>
                """,
                unsafe_allow_html=True
            )
            
            st.markdown(
                """
                <div class="chat-bubble-ai page-enter">
                    <span style="background: var(--grad-primary); border-radius: 50%; padding: 4px 8px; font-weight: bold; color: #000; margin-right: 6px;">⚡</span> <b>Kairo AI:</b> 
                    <span class="thinking-dot"></span><span class="thinking-dot"></span><span class="thinking-dot"></span>
                </div>
                """,
                unsafe_allow_html=True
            )
            
            response_text = generate_ai_chat_response(prompt_to_send, st.session_state["chat_messages"])

        # Append AI response & save to disk
        st.session_state["chat_messages"].append({"role": "assistant", "content": response_text})
        save_user_data()
        st.rerun()
