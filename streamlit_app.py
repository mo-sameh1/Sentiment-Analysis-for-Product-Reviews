"""
Streamlit Application Entry Point for Sentiment Analysis Dashboard.

This module serves as the main entry point for the Streamlit web application,
ensuring proper Python path configuration before importing any project modules.
"""

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import streamlit as st
from dotenv import load_dotenv

load_dotenv()

from src.config import (
    APP_TITLE,
    APP_ICON,
    PAGE_HOME,
    PAGE_DATA_EXPLORER,
    PAGE_SINGLE_PREDICTION,
    PAGE_BATCH_ANALYSIS,
    PAGE_PIPELINE_STATUS,
)

st.set_page_config(
    page_title=APP_TITLE,
    page_icon=APP_ICON,
    layout="wide",
    initial_sidebar_state="expanded"
)

from src.ui.pages.home import render_home_page
from src.ui.pages.eda import render_eda_page
from src.ui.pages.prediction import render_prediction_page
from src.ui.pages.pipeline import render_pipeline_page
from src.ui.pages.batch_analysis import render_batch_analysis_page
from src.ui.components.sidebar import render_sidebar


def main():
    render_sidebar()
    
    page = st.session_state.get("current_page", PAGE_HOME)
    
    if page == PAGE_HOME:
        render_home_page()
    elif page == PAGE_DATA_EXPLORER:
        render_eda_page()
    elif page == PAGE_SINGLE_PREDICTION:
        render_prediction_page()
    elif page == PAGE_BATCH_ANALYSIS:
        render_batch_analysis_page()
    elif page == PAGE_PIPELINE_STATUS:
        render_pipeline_page()


if __name__ == "__main__":
    main()
