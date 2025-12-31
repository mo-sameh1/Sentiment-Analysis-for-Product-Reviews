"""
Sidebar component for navigation.
"""

import streamlit as st
from src.config import APP_TITLE, APP_VERSION, PAGES, PAGE_HOME


def render_sidebar():
    with st.sidebar:
        st.image("https://img.icons8.com/fluency/96/sentiment-analysis.png", width=80)
        st.title("Navigation")
        
        if "current_page" not in st.session_state:
            st.session_state.current_page = PAGE_HOME
        
        for icon, page_name in PAGES:
            if st.button(f"{icon} {page_name}", key=f"nav_{page_name}", use_container_width=True):
                st.session_state.current_page = page_name
                st.rerun()
        
        st.divider()
        
        st.caption("📌 Quick Info")
        
        from src.ui.services.data_service import DataService
        from src.ui.services.prediction_service import PredictionService
        
        data_service = DataService()
        pred_service = PredictionService()
        
        db_status = "🟢 Connected" if data_service.check_connection() else "🔴 Disconnected"
        model_status = "🟢 Ready" if pred_service.is_model_available() else "🟡 Not Trained"
        
        st.markdown(f"**Database:** {db_status}")
        st.markdown(f"**Model:** {model_status}")
        
        st.divider()
        st.caption(f"{APP_TITLE} v{APP_VERSION}")
