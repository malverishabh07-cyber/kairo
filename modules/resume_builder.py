"""
Kairo — Resume Builder Module
Multi-section resume builder with live interactive glassmorphic preview and ReportLab PDF download.
"""

import streamlit as st
from utils.pdf_helper import generate_resume_pdf
from utils.storage_helper import save_user_data

def render_resume_builder():
    st.markdown(
        """
        <div class="kairo-header page-enter">
            <div>
                <h1 class="kairo-title">📄 AI Resume Builder</h1>
                <p class="kairo-tagline">Craft a sleek, high-impact technical resume tailored for top tech roles.</p>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    resume_data = st.session_state.get("resume_data", {})

    col_editor, col_preview = st.columns([1, 1.1])

    with col_editor:
        st.markdown("<h3 style='color: var(--primary-accent);'>✏️ Edit Resume Details</h3>", unsafe_allow_html=True)
        
        tabs = st.tabs(["👤 Personal", "🎓 Education", "⚡ Skills", "🚀 Projects", "💼 Experience"])

        with tabs[0]:
            name = st.text_input("Full Name", resume_data.get("name", ""))
            email = st.text_input("Email Address", resume_data.get("email", ""))
            phone = st.text_input("Phone Number", resume_data.get("phone", ""))
            location = st.text_input("Location (City, State)", resume_data.get("location", ""))
            linkedin = st.text_input("LinkedIn Profile", resume_data.get("linkedin", ""))
            github = st.text_input("GitHub Profile", resume_data.get("github", ""))
            summary = st.text_area("Professional Summary", resume_data.get("summary", ""), height=100)

        with tabs[1]:
            education = st.text_area("Education Details", resume_data.get("education", ""), height=100)

        with tabs[2]:
            skills = st.text_area("Technical Skills & Frameworks", resume_data.get("skills", ""), height=100)

        with tabs[3]:
            st.markdown("**Project 1:**")
            p1_title = st.text_input("Project 1 Title", resume_data.get("projects", [{}])[0].get("title", "") if resume_data.get("projects") else "")
            p1_desc = st.text_area("Project 1 Description", resume_data.get("projects", [{}])[0].get("desc", "") if resume_data.get("projects") else "", height=70)
            
            st.markdown("**Project 2:**")
            p2_title = st.text_input("Project 2 Title", resume_data.get("projects", [{}, {}])[1].get("title", "") if len(resume_data.get("projects", [])) > 1 else "")
            p2_desc = st.text_area("Project 2 Description", resume_data.get("projects", [{}, {}])[1].get("desc", "") if len(resume_data.get("projects", [])) > 1 else "", height=70)

        with tabs[4]:
            role = st.text_input("Recent Role Title", resume_data.get("experience", [{}])[0].get("role", "") if resume_data.get("experience") else "")
            company = st.text_input("Company / Lab Name", resume_data.get("experience", [{}])[0].get("company", "") if resume_data.get("experience") else "")
            period = st.text_input("Period / Duration", resume_data.get("experience", [{}])[0].get("period", "") if resume_data.get("experience") else "")
            exp_desc = st.text_area("Key Achievements", resume_data.get("experience", [{}])[0].get("desc", "") if resume_data.get("experience") else "", height=80)
            certs = st.text_input("Certifications & Achievements", resume_data.get("certifications", ""))

        if st.button("💾 Save & Update Preview", use_container_width=True):
            updated_data = {
                "name": name,
                "email": email,
                "phone": phone,
                "location": location,
                "linkedin": linkedin,
                "github": github,
                "summary": summary,
                "education": education,
                "skills": skills,
                "projects": [
                    {"title": p1_title, "desc": p1_desc},
                    {"title": p2_title, "desc": p2_desc}
                ],
                "experience": [
                    {"role": role, "company": company, "period": period, "desc": exp_desc}
                ],
                "certifications": certs
            }
            st.session_state["resume_data"] = updated_data
            save_user_data()
            st.success("✨ Resume data saved and preview updated!")
            st.rerun()

    with col_preview:
        st.markdown("<h3 style='color: var(--primary-accent);'>👀 Live Resume Preview</h3>", unsafe_allow_html=True)

        data = st.session_state.get("resume_data", {})
        
        # Render Glassmorphic Resume Preview Card
        st.markdown(
            f"""
            <div class="glass-card page-enter" style="background: rgba(15, 23, 42, 0.9); border-color: rgba(var(--accent-rgb), 0.4); padding: 2rem;">
                <h1 style="color: var(--primary-accent); margin-bottom: 4px; font-size: 1.8rem;">{data.get('name', 'Alex Mercer')}</h1>
                <div style="font-size: 0.85rem; color: #94a3b8; margin-bottom: 1rem;">
                    {data.get('email', '')} | {data.get('phone', '')} | {data.get('location', '')}<br>
                    <span style="color: var(--primary-accent);">{data.get('linkedin', '')} • {data.get('github', '')}</span>
                </div>
                
                <h4 style="color: var(--primary-accent); border-bottom: 1px solid rgba(var(--accent-rgb),0.2); padding-bottom: 4px; margin-top: 1rem;">PROFESSIONAL SUMMARY</h4>
                <p style="font-size: 0.9rem; color: #cbd5e1;">{data.get('summary', '')}</p>
                
                <h4 style="color: var(--primary-accent); border-bottom: 1px solid rgba(var(--accent-rgb),0.2); padding-bottom: 4px; margin-top: 1rem;">EDUCATION</h4>
                <p style="font-size: 0.9rem; color: #cbd5e1;">{data.get('education', '')}</p>
                
                <h4 style="color: var(--primary-accent); border-bottom: 1px solid rgba(var(--accent-rgb),0.2); padding-bottom: 4px; margin-top: 1rem;">TECHNICAL SKILLS</h4>
                <p style="font-size: 0.9rem; color: #cbd5e1;">{data.get('skills', '')}</p>
                
                <h4 style="color: var(--primary-accent); border-bottom: 1px solid rgba(var(--accent-rgb),0.2); padding-bottom: 4px; margin-top: 1rem;">FEATURED PROJECTS</h4>
                {"".join([f"<p style='font-size: 0.9rem; margin-bottom: 2px;'><b style='color: #f8fafc;'>{p.get('title', '')}:</b> <span style='color: #cbd5e1;'>{p.get('desc', '')}</span></p>" for p in data.get('projects', []) if p.get('title')])}
                
                <h4 style="color: var(--primary-accent); border-bottom: 1px solid rgba(var(--accent-rgb),0.2); padding-bottom: 4px; margin-top: 1rem;">EXPERIENCE</h4>
                {"".join([f"<p style='font-size: 0.9rem;'><b style='color: #f8fafc;'>{e.get('role', '')}</b> - {e.get('company', '')} <i style='color: #94a3b8;'>({e.get('period', '')})</i><br><span style='color: #cbd5e1;'>{e.get('desc', '')}</span></p>" for e in data.get('experience', []) if e.get('role')])}
            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown("<br>", unsafe_allow_html=True)
        # Generate ReportLab PDF
        try:
            pdf_bytes = generate_resume_pdf(data)
            st.download_button(
                label="📥 Download Resume PDF",
                data=pdf_bytes,
                file_name=f"{data.get('name', 'resume').lower().replace(' ', '_')}_resume.pdf",
                mime="application/pdf",
                use_container_width=True
            )
        except Exception as e:
            st.error(f"Error compiling PDF: {e}")
