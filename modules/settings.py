"""
Kairo — Settings & Customization Module
API key configuration, curated theme presets, profile customization, and auth management.
"""

import streamlit as st
from utils.storage_helper import save_user_data

THEME_OPTIONS = {
    "cyan_violet": {
        "name": "⚡ Cyan & Violet (Default)",
        "desc": "Futuristic neon cyan with deep violet undertones",
        "primary": "#00F2FE",
        "secondary": "#7F00FF"
    },
    "emerald_amber": {
        "name": "🌿 Emerald & Amber",
        "desc": "Calming forest emerald paired with warm energy amber",
        "primary": "#10B981",
        "secondary": "#F59E0B"
    },
    "rose_indigo": {
        "name": "🌹 Rose & Indigo",
        "desc": "Vibrant rose glow with royal indigo depths",
        "primary": "#F43F5E",
        "secondary": "#6366F1"
    },
    "amber_slate": {
        "name": "🌅 Amber & Slate",
        "desc": "Warm sunset amber paired with minimal slate tones",
        "primary": "#F59E0B",
        "secondary": "#64748B"
    }
}

def render_settings():
    st.markdown(
        """
        <div class="kairo-header page-enter">
            <div>
                <h1 class="kairo-title">⚙️ Kairo Settings & Themes</h1>
                <p class="kairo-tagline">Manage your theme presets, Gemini API Key, student profile, and app preferences.</p>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # 1. Curated Theme Presets Card
    st.markdown(
        """
        <div class="glass-card page-enter">
            <h3 style="color: var(--primary-accent); margin-top: 0;">🎨 Curated Theme Customization</h3>
            <p style="font-size: 0.88rem; color: #94a3b8;">
                Choose an accent theme. The selected palette is applied instantly app-wide, including the custom cursor and focus timer glow.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    current_theme = st.session_state.get("theme_preset", "cyan_violet")
    t_cols = st.columns(4)
    for idx, (t_key, t_info) in enumerate(THEME_OPTIONS.items()):
        with t_cols[idx]:
            is_active = (current_theme == t_key)
            border_style = f"border: 2px solid {t_info['primary']};" if is_active else "border: 1px solid rgba(255,255,255,0.1);"
            bg_active = "background: rgba(22, 31, 51, 0.95);" if is_active else "background: rgba(22, 31, 51, 0.5);"
            
            st.markdown(
                f"""
                <div style="{bg_active} {border_style} border-radius: 14px; padding: 14px; text-align: center; margin-bottom: 8px;">
                    <div style="display: flex; justify-content: center; gap: 8px; margin-bottom: 8px;">
                        <span style="width: 20px; height: 20px; border-radius: 50%; background: {t_info['primary']}; display: inline-block; box-shadow: 0 0 8px {t_info['primary']};"></span>
                        <span style="width: 20px; height: 20px; border-radius: 50%; background: {t_info['secondary']}; display: inline-block;"></span>
                    </div>
                    <div style="font-weight: 700; font-size: 0.9rem; color: #ffffff;">{t_info['name'].split(' ')[1]}</div>
                    <div style="font-size: 0.72rem; color: #94a3b8; margin-top: 4px;">{t_info['desc']}</div>
                </div>
                """,
                unsafe_allow_html=True
            )
            btn_label = "✅ Active" if is_active else "Apply"
            if st.button(btn_label, key=f"apply_theme_{t_key}", use_container_width=True, type="primary" if is_active else "secondary"):
                st.session_state["theme_preset"] = t_key
                save_user_data()
                st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    col_set1, col_set2 = st.columns([1.1, 1])

    with col_set1:
        # API Key Configuration Card
        st.markdown(
            """
            <div class="glass-card page-enter">
                <h3 style="color: var(--primary-accent); margin-top: 0;">🔑 Gemini API Key Configuration</h3>
                <p style="font-size: 0.88rem; color: #94a3b8;">
                    Enter your Google Gemini API Key to enable live AI responses, custom quiz generation, and personalized roadmaps.
                </p>
            """,
            unsafe_allow_html=True
        )

        current_key = st.session_state.get("gemini_api_key", "")
        api_input = st.text_input("Gemini API Key", value=current_key, type="password", placeholder="AIzaSy...")

        if st.button("💾 Save API Key", key="save_api_key_btn"):
            st.session_state["gemini_api_key"] = api_input.strip()
            save_user_data()
            st.success("✨ API Key saved successfully!")
            st.rerun()

        if current_key:
            st.markdown("🟢 **Status:** API Key Configured (Live Kairo AI)")
        else:
            st.markdown("🟡 **Status:** Running in Built-in Intelligent Fallback Mode (No key required)")

        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # Profile Settings Card
        st.markdown(
            """
            <div class="glass-card page-enter">
                <h3 style="color: var(--primary-accent); margin-top: 0;">👤 Student Profile</h3>
            """,
            unsafe_allow_html=True
        )

        with st.form("profile_settings_form"):
            p_name = st.text_input("Student Name", st.session_state.get("user_name", "Alex Mercer"))
            p_school = st.text_input("University / Institution", st.session_state.get("user_school", "Stanford University"))
            p_major = st.text_input("Major / Specialization", st.session_state.get("user_major", "Computer Science"))
            p_gpa = st.text_input("Target GPA", st.session_state.get("target_gpa", "3.9"))
            p_hours = st.number_input("Daily Target Study Hours", 1.0, 12.0, float(st.session_state.get("daily_target_hours", 4.5)), 0.5)

            save_profile_btn = st.form_submit_button("💾 Save Profile", use_container_width=True)

        if save_profile_btn:
            st.session_state["user_name"] = p_name
            st.session_state["user_school"] = p_school
            st.session_state["user_major"] = p_major
            st.session_state["target_gpa"] = p_gpa
            st.session_state["daily_target_hours"] = p_hours
            save_user_data()
            st.success("✨ Profile details updated!")
            st.rerun()

        st.markdown("</div>", unsafe_allow_html=True)

    with col_set2:
        # Account & Authentication Manager Card
        st.markdown(
            """
            <div class="glass-card page-enter">
                <h3 style="color: var(--primary-accent); margin-top: 0;">🔒 User Account & Auth</h3>
            """,
            unsafe_allow_html=True
        )

        user_acc = st.session_state.get("user_account", {})
        provider = user_acc.get("provider", "guest")
        
        st.write(f"**Current User:** `{user_acc.get('name', 'Alex Mercer')}`")
        st.write(f"**Email:** `{user_acc.get('email', 'alex.mercer@stanford.edu')}`")
        st.write(f"**Auth Mode:** `{provider.upper()}`")

        if st.button("🔑 Switch Account / Sign In", key="settings_auth_btn", use_container_width=True):
            st.session_state["auth_show_modal"] = True
            st.rerun()

        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # Focus & Sound Preferences
        st.markdown(
            """
            <div class="glass-card page-enter">
                <h3 style="color: var(--primary-accent); margin-top: 0;">🎵 Focus Timer & Audio Preferences</h3>
            """,
            unsafe_allow_html=True
        )

        sound_on = st.checkbox("Enable Ambient Soundscapes during Focus", value=st.session_state.get("ambient_sound_enabled", True))
        st.session_state["ambient_sound_enabled"] = sound_on
        st.checkbox("Enable Celebratory Chimes on Session Finish", value=True)
        st.checkbox("Enable Daily Streak Reminders", value=True)

        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("⚠️ Reset All Session Data", key="reset_session_btn", use_container_width=True):
            st.session_state.clear()
            st.success("Session state reset to initial state!")
            st.rerun()
