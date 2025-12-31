"""
Exploratory Data Analysis page.
"""

import streamlit as st
import pandas as pd
from src.ui.services.data_service import DataService
from src.ui.components.charts import (
    render_score_distribution,
    render_sentiment_pie,
    render_wordcloud,
    render_review_length_distribution,
    render_helpfulness_analysis
)
from src.ui.components.metrics import render_data_stats


def render_eda_page():
    st.title("📊 Exploratory Data Analysis")
    
    st.markdown("""
    Explore and visualize the product reviews dataset. 
    Fetch data from MongoDB and analyze patterns in customer feedback.
    """)
    
    data_service = DataService()
    
    with st.expander("⚙️ Connection Settings", expanded=False):
        conn_info = data_service.get_connection_info()
        col1, col2, col3 = st.columns(3)
        col1.text_input("MongoDB URI", value=conn_info["uri"], disabled=True)
        col2.text_input("Database", value=conn_info["database"], disabled=True)
        col3.text_input("Collection", value=conn_info["collection"], disabled=True)
    
    st.subheader("📥 Data Loading")
    
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        limit = st.slider(
            "Number of reviews to fetch",
            min_value=100,
            max_value=10000,
            value=1000,
            step=100,
            help="Adjust the number of reviews to load from the database"
        )
    
    with col2:
        force_refresh = st.checkbox("Force Refresh", value=False)
    
    with col3:
        fetch_clicked = st.button("🔄 Fetch Data", type="primary", use_container_width=True)
    
    if "eda_data" not in st.session_state:
        st.session_state.eda_data = None
    
    if fetch_clicked:
        with st.spinner("Fetching data from MongoDB..."):
            try:
                df = data_service.fetch_reviews(limit=limit, force_refresh=force_refresh)
                if df.empty:
                    st.warning("No data found in the database. Please run the data initialization script.")
                    return
                st.session_state.eda_data = df
                st.success(f"✅ Successfully loaded {len(df):,} reviews!")
            except ConnectionError as e:
                st.error(f"❌ Connection Error: {e}")
                st.info("Make sure MongoDB is running and accessible.")
                return
            except Exception as e:
                st.error(f"❌ Error: {e}")
                return
    
    df = st.session_state.eda_data
    
    if df is None or df.empty:
        st.info("👆 Click 'Fetch Data' to load reviews from the database.")
        return
    
    st.divider()
    
    st.subheader("📈 Quick Statistics")
    render_data_stats(df)
    
    st.divider()
    
    tab1, tab2, tab3, tab4 = st.tabs([
        "📊 Distribution", 
        "☁️ Word Cloud", 
        "📏 Text Analysis",
        "📋 Raw Data"
    ])
    
    with tab1:
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("#### Rating Score Distribution")
            render_score_distribution(df)
        with col2:
            st.markdown("#### Sentiment Breakdown")
            render_sentiment_pie(df)
    
    with tab2:
        st.markdown("#### Word Cloud from Review Text")
        col1, col2 = st.columns(2)
        with col1:
            max_words = st.slider("Maximum words", 50, 200, 100)
        with col2:
            use_cleaned = st.checkbox(
                "Use cleaned text (stopwords & lemmatization)", 
                value=True,
                help="Apply the same preprocessing used in model training"
            )
        render_wordcloud(df, column="Text", max_words=max_words, use_cleaned=use_cleaned)
    
    with tab3:
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("#### Review Length Distribution")
            render_review_length_distribution(df)
        with col2:
            st.markdown("#### Helpfulness Analysis")
            render_helpfulness_analysis(df)
    
    with tab4:
        st.markdown("#### Raw Data Preview")
        
        display_columns = st.multiselect(
            "Select columns to display",
            options=df.columns.tolist(),
            default=["ProductId", "Score", "Summary", "Text"][:4]
        )
        
        if display_columns:
            st.dataframe(
                df[display_columns],
                use_container_width=True,
                height=400
            )
        
        csv = df.to_csv(index=False)
        st.download_button(
            label="📥 Download Data as CSV",
            data=csv,
            file_name="reviews_data.csv",
            mime="text/csv"
        )
