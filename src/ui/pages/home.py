"""
Home page of the Sentiment Analysis Dashboard.
"""

import streamlit as st


def render_home_page():
    st.title("🎯 Product Review Sentiment Analysis")
    
    st.markdown("""
    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                padding: 2rem; border-radius: 10px; color: white; margin-bottom: 2rem;">
        <h2 style="margin: 0; color: white;">Welcome to the Sentiment Analysis Dashboard</h2>
        <p style="margin-top: 1rem; font-size: 1.1rem;">
            Analyze product reviews and understand customer sentiment using machine learning.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.header("📋 Project Overview")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🔄 Data Pipeline")
        st.markdown("""
        This project implements a complete ETL data pipeline:
        
        1. **Extract**: Fetch Amazon product reviews from Kaggle dataset
        2. **Transform**: Clean, preprocess, and vectorize text data
        3. **Load**: Store processed data in MongoDB for analysis
        """)
        
        st.subheader("🧠 Machine Learning")
        st.markdown("""
        - **Text Preprocessing**: Cleaning, lemmatization, stopword removal
        - **Feature Extraction**: TF-IDF vectorization with n-grams
        - **Classification**: Logistic Regression for sentiment prediction
        - **Class Balancing**: Handled imbalanced dataset through undersampling
        """)
    
    with col2:
        st.subheader("🛠️ Technology Stack")
        
        tech_data = {
            "Category": ["Backend", "Database", "ML/NLP", "Frontend", "DevOps"],
            "Technologies": [
                "Python, Pydantic",
                "MongoDB",
                "Scikit-learn, NLTK, Pandas",
                "Streamlit",
                "Docker, Docker Compose"
            ]
        }
        st.table(tech_data)
        
        st.subheader("📊 Features")
        st.markdown("""
        - ✅ Interactive data exploration
        - ✅ Real-time sentiment prediction
        - ✅ Batch analysis capabilities
        - ✅ Visualization dashboards
        - ✅ Pipeline monitoring
        """)
    
    st.divider()
    
    st.header("🚀 Quick Start")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.info("### 1️⃣ Explore Data\nNavigate to **Data Explorer** to visualize and understand the dataset.")
    
    with col2:
        st.info("### 2️⃣ Make Predictions\nUse **Single Prediction** to analyze individual reviews in real-time.")
    
    with col3:
        st.info("### 3️⃣ Batch Analysis\nUpload CSV files in **Batch Analysis** for bulk sentiment analysis.")
    
    st.divider()
    
    st.header("📈 System Status")
    
    from src.ui.services.data_service import DataService
    from src.ui.services.prediction_service import PredictionService
    
    data_service = DataService()
    pred_service = PredictionService()
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        db_connected = data_service.check_connection()
        if db_connected:
            st.success("✅ Database Connected")
            stats = data_service.get_collection_stats()
            st.metric("Total Documents", f"{stats['total_documents']:,}")
        else:
            st.error("❌ Database Disconnected")
            st.caption("Make sure MongoDB is running")
    
    with col2:
        model_info = pred_service.get_model_info()
        if model_info["model_exists"] and model_info["vectorizer_exists"]:
            st.success("✅ Model Ready")
            st.metric("Model Size", model_info.get("model_size", "N/A"))
        else:
            st.warning("⚠️ Model Not Trained")
            st.caption("Run the training script first")
    
    with col3:
        st.info("ℹ️ System Info")
        import platform
        st.caption(f"Python {platform.python_version()}")
        st.caption(f"Platform: {platform.system()}")
