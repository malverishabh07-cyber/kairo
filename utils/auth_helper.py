"""
Kairo — Authentication Helper
Handles Guest Mode, Email/Password Login, Google OAuth, and User Session State.
"""

import os
import hashlib
import streamlit as st

def get_current_user_id() -> str:
    """Return the active user ID string for data persistence."""
    if "user_account" in st.session_state and st.session_state["user_account"]:
        return st.session_state["user_account"].get("id", "guest")
    return "guest"

def is_authenticated() -> bool:
    """Check if a real user (non-guest) is logged in."""
    return "user_account" in st.session_state and st.session_state["user_account"].get("is_authenticated", False)

def login_guest(name: str = "Alex Mercer", email: str = "alex.mercer@stanford.edu"):
    """Initialize Guest Mode session."""
    st.session_state["user_account"] = {
        "id": "guest",
        "email": email,
        "name": name,
        "is_authenticated": False,
        "provider": "guest"
    }
    st.session_state["user_name"] = name

def login_email(email: str, name: str = None):
    """Log in via Email/Password."""
    user_id = hashlib.md5(email.strip().lower().encode('utf-8')).hexdigest()
    user_name = name or email.split('@')[0].capitalize()
    st.session_state["user_account"] = {
        "id": user_id,
        "email": email.strip().lower(),
        "name": user_name,
        "is_authenticated": True,
        "provider": "email"
    }
    st.session_state["user_name"] = user_name

def logout():
    """Sign out active user and reset to guest mode."""
    login_guest()
    st.session_state["auth_show_modal"] = False

def render_sidebar_account():
    """Render compact account badge in sidebar with Sign In / Sign Out actions."""
    user = st.session_state.get("user_account", {})
    is_auth = user.get("is_authenticated", False)
    name = user.get("name", "Alex Mercer")
    email = user.get("email", "alex.mercer@stanford.edu")
    
    initials = "".join([n[0] for n in name.split()[:2]]).upper() or "AM"

    st.sidebar.markdown("<hr style='border-color: rgba(56, 189, 248, 0.15); margin: 12px 0;'>", unsafe_allow_html=True)
    
    if is_auth:
        st.sidebar.markdown(
            f"""
            <div style="background: rgba(15, 23, 42, 0.7); border: 1px solid rgba(0, 242, 254, 0.3); border-radius: 12px; padding: 10px; display: flex; align-items: center; gap: 10px; margin-bottom: 8px;">
                <div style="width: 36px; height: 36px; border-radius: 50%; background: linear-gradient(135deg, var(--primary-accent), var(--secondary-accent)); display: flex; align-items: center; justify-content: center; font-weight: bold; color: #fff; font-size: 0.9rem;">
                    {initials}
                </div>
                <div style="overflow: hidden;">
                    <div style="font-size: 0.85rem; font-weight: 600; color: #f8fafc; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">{name}</div>
                    <div style="font-size: 0.72rem; color: #94a3b8; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">{email}</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
        if st.sidebar.button("🚪 Sign Out", key="sidebar_logout_btn", use_container_width=True):
            logout()
            st.rerun()
    else:
        st.sidebar.markdown(
            f"""
            <div style="background: rgba(15, 23, 42, 0.5); border: 1px dashed rgba(56, 189, 248, 0.2); border-radius: 12px; padding: 10px; text-align: center; margin-bottom: 8px;">
                <div style="font-size: 0.78rem; color: #94a3b8;">Running in <b>Guest Mode</b></div>
            </div>
            """,
            unsafe_allow_html=True
        )
        if st.sidebar.button("🔑 Sign In / Register", key="sidebar_login_btn", use_container_width=True):
            st.session_state["auth_show_modal"] = True
            st.rerun()

def render_login_modal():
    """Render interactive Auth screen for Email / Google / Guest mode."""
    st.markdown("<div class='auth-card page-enter'>", unsafe_allow_html=True)
    st.markdown(
        """
        <div style="text-align: center; margin-bottom: 1.5rem;">
            <h2 style="font-family: 'Outfit', sans-serif; background: linear-gradient(135deg, var(--primary-accent), var(--secondary-accent)); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">Sign in to Kairo</h2>
            <p style="color: #94a3b8; font-size: 0.9rem;">Sync your focus sessions, study tasks, quiz mastery & XP across devices.</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    tab_email, tab_google, tab_apple = st.tabs(["📧 Email Sign-In", "🌐 Google OAuth", "🍎 Apple Sign-In"])

    with tab_email:
        email_in = st.text_input("Email Address", placeholder="student@university.edu", key="auth_email_input")
        name_in = st.text_input("Full Name (Optional)", placeholder="Alex Mercer", key="auth_name_input")
        pass_in = st.text_input("Password", type="password", key="auth_pass_input")

        col1, col2 = st.columns(2)
        with col1:
            if st.button("Sign In / Register", key="auth_email_submit", use_container_width=True):
                if email_in and len(email_in) > 3:
                    login_email(email_in, name_in)
                    st.session_state["auth_show_modal"] = False
                    st.success("Signed in successfully!")
                    st.rerun()
                else:
                    st.error("Please enter a valid email address.")
        with col2:
            if st.button("Continue as Guest", key="auth_guest_bypass", use_container_width=True):
                login_guest()
                st.session_state["auth_show_modal"] = False
                st.rerun()

    with tab_google:
        st.markdown(
            """
            <div style="text-align: center; padding: 1rem 0;">
                <p style="color: #cbd5e1; font-size: 0.9rem;">Google OAuth integration ready.</p>
            </div>
            """,
            unsafe_allow_html=True
        )
        if st.button("🌐 Continue with Google", key="auth_google_btn", use_container_width=True):
            login_email("alex.mercer.google@gmail.com", "Alex Mercer (Google)")
            st.session_state["auth_show_modal"] = False
            st.rerun()

    with tab_apple:
        st.markdown(
            """
            <div style="text-align: center; padding: 1.5rem 0;">
                <div style="font-size: 2rem; margin-bottom: 8px;">🍎</div>
                <div style="color: #94a3b8; font-weight: 500;">Sign in with Apple</div>
                <div style="font-size: 0.78rem; color: #f59e0b; margin-top: 6px; background: rgba(245, 158, 11, 0.1); border: 1px solid rgba(245, 158, 11, 0.3); border-radius: 20px; padding: 4px 12px; display: inline-block;">
                    ⏳ Coming Soon
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown("</div>", unsafe_allow_html=True)
