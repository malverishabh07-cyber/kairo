"""
Synapse AI - Responsive Helper Utility
Injects viewport detection and responsive CSS helper attributes into Streamlit DOM.
"""

import streamlit as st

def inject_responsive_classes():
    """Inject JS & CSS snippets for viewport detection and responsive layouts."""
    responsive_html = """
    <script>
    (function() {
        function updateViewportAttr() {
            var width = window.innerWidth;
            var deviceClass = 'desktop';
            if (width <= 480) {
                deviceClass = 'mobile';
            } else if (width <= 768) {
                deviceClass = 'tablet';
            }
            document.body.setAttribute('data-device', deviceClass);
        }
        window.addEventListener('resize', updateViewportAttr);
        updateViewportAttr();
    })();
    </script>
    """
    st.components.v1.html(responsive_html, height=0, width=0)
