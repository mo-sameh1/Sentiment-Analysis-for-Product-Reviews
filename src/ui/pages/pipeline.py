"""
Pipeline status and management page.
"""

import streamlit as st
import os
import subprocess
import sys
from pathlib import Path
from src.ui.services.data_service import DataService
from src.ui.services.prediction_service import PredictionService


def render_pipeline_page():
    st.title("⚙️ Pipeline Status & Management")
    
    st.markdown("""
    Monitor and manage the data pipeline components. 
    View connection status, run training, and check system health.
    """)
    
    data_service = DataService()
    pred_service = PredictionService()
    
    st.subheader("🔌 Connection Status")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### MongoDB Database")
        
        if data_service.check_connection():
            st.success("✅ Connected")
            stats = data_service.get_collection_stats()
            
            conn_info = data_service.get_connection_info()
            st.markdown(f"""
            - **URI**: `{conn_info['uri']}`
            - **Database**: `{conn_info['database']}`
            - **Collection**: `{conn_info['collection']}`
            - **Documents**: {stats['total_documents']:,}
            """)
        else:
            st.error("❌ Disconnected")
            st.markdown("""
            **Troubleshooting:**
            1. Ensure MongoDB is running
            2. Check the connection URI in `.env` file
            3. Verify network connectivity
            
            ```bash
            # Start MongoDB with Docker
            docker-compose up -d mongodb
            ```
            """)
    
    with col2:
        st.markdown("#### ML Model")
        
        model_info = pred_service.get_model_info()
        
        if pred_service.is_model_available():
            st.success("✅ Model Ready")
            st.markdown(f"""
            - **Model Path**: `{model_info['model_path']}`
            - **Model Size**: {model_info.get('model_size', 'N/A')}
            - **Vectorizer Path**: `{model_info['vectorizer_path']}`
            - **Vectorizer Size**: {model_info.get('vectorizer_size', 'N/A')}
            """)
        else:
            st.warning("⚠️ Model Not Trained")
            st.markdown("""
            The sentiment model needs to be trained before making predictions.
            
            Missing files:
            """)
            if not model_info["model_exists"]:
                st.markdown(f"- ❌ `{model_info['model_path']}`")
            if not model_info["vectorizer_exists"]:
                st.markdown(f"- ❌ `{model_info['vectorizer_path']}`")
    
    st.divider()
    
    st.subheader("🔄 Pipeline Operations")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("#### Data Download")
        st.caption("Download dataset from Kaggle")
        
        if st.button("📥 Download Data", use_container_width=True):
            with st.spinner("Downloading data..."):
                try:
                    result = subprocess.run(
                        [sys.executable, "scripts/download_data.py"],
                        capture_output=True,
                        text=True,
                        cwd=str(Path(__file__).parents[3])
                    )
                    if result.returncode == 0:
                        st.success("✅ Data downloaded successfully!")
                        st.code(result.stdout)
                    else:
                        st.error("❌ Download failed")
                        st.code(result.stderr)
                except Exception as e:
                    st.error(f"Error: {e}")
    
    with col2:
        st.markdown("#### Database Init")
        st.caption("Load data into MongoDB")
        
        if st.button("🗄️ Initialize DB", use_container_width=True):
            with st.spinner("Initializing database..."):
                try:
                    result = subprocess.run(
                        [sys.executable, "scripts/initialize_db.py"],
                        capture_output=True,
                        text=True,
                        cwd=str(Path(__file__).parents[3])
                    )
                    if result.returncode == 0:
                        st.success("✅ Database initialized!")
                        st.code(result.stdout)
                    else:
                        st.error("❌ Initialization failed")
                        st.code(result.stderr)
                except Exception as e:
                    st.error(f"Error: {e}")
    
    with col3:
        st.markdown("#### Model Training")
        st.caption("Train sentiment classifier")
        
        if st.button("🧠 Train Model", use_container_width=True, type="primary"):
            with st.spinner("Training model... This may take a few minutes."):
                try:
                    result = subprocess.run(
                        [sys.executable, "scripts/train_model.py"],
                        capture_output=True,
                        text=True,
                        cwd=str(Path(__file__).parents[3])
                    )
                    if result.returncode == 0:
                        st.success("✅ Model trained successfully!")
                        st.code(result.stdout)
                        st.balloons()
                    else:
                        st.error("❌ Training failed")
                        st.code(result.stderr)
                except Exception as e:
                    st.error(f"Error: {e}")
    
    st.divider()
    
    st.subheader("📁 Project Structure")
    
    with st.expander("View Project Files", expanded=False):
        project_root = Path(__file__).parents[3]
        
        structure = """
        ```
        Sentiment-Analysis-for-Product-Reviews/
        ├── streamlit_app.py          # Main Streamlit entry point
        ├── requirements.txt          # Python dependencies
        ├── docker-compose.yml        # Docker services config
        ├── .env                      # Environment variables
        │
        ├── data/                     # Data directory
        │   ├── Reviews.csv           # Raw dataset
        │   ├── model.pkl             # Trained model
        │   └── vectorizer.pkl        # Fitted vectorizer
        │
        ├── scripts/                  # Utility scripts
        │   ├── download_data.py      # Kaggle data download
        │   ├── initialize_db.py      # MongoDB data loader
        │   └── train_model.py        # Model training script
        │
        └── src/                      # Source code
            ├── models.py             # Pydantic models
            ├── pipeline.py           # Pipeline orchestration
            ├── inference.py          # Inference utilities
            │
            ├── fetchers/             # Data fetchers
            │   ├── base.py
            │   ├── csv_fetcher.py
            │   └── mongo_fetcher.py
            │
            ├── transformers/         # Data transformers
            │   ├── base.py
            │   └── text_sentiment_transformer.py
            │
            ├── loaders/              # Model loaders
            │   ├── base.py
            │   └── sentiment_loader.py
            │
            └── ui/                   # Streamlit UI
                ├── pages/            # Page components
                ├── components/       # Reusable components
                └── services/         # Business logic services
        ```
        """
        st.markdown(structure)
    
    st.divider()
    
    st.subheader("📊 System Information")
    
    col1, col2 = st.columns(2)
    
    with col1:
        import platform
        st.markdown("#### Environment")
        st.markdown(f"""
        - **Python Version**: {platform.python_version()}
        - **Platform**: {platform.system()} {platform.release()}
        - **Architecture**: {platform.machine()}
        """)
    
    with col2:
        st.markdown("#### Dependencies")
        try:
            import sklearn
            import pandas
            import nltk
            import pymongo
            
            st.markdown(f"""
            - **scikit-learn**: {sklearn.__version__}
            - **pandas**: {pandas.__version__}
            - **nltk**: {nltk.__version__}
            - **pymongo**: {pymongo.__version__}
            """)
        except ImportError as e:
            st.error(f"Missing dependency: {e}")
