"""
Single prediction page for real-time sentiment analysis.
"""

import streamlit as st
from src.ui.services.prediction_service import PredictionService
from src.ui.components.metrics import render_prediction_result_card
from src.config import SAMPLE_REVIEWS, CONFIDENCE_HIGH_THRESHOLD, CONFIDENCE_MEDIUM_THRESHOLD


def render_prediction_page():
    st.title("🔮 Sentiment Prediction")
    
    st.markdown("""
    Enter a product review to analyze its sentiment using our trained machine learning model.
    The model will classify the review as **Positive** or **Negative** with a confidence score.
    """)
    
    pred_service = PredictionService()
    model_info = pred_service.get_model_info()
    
    if not pred_service.is_model_available():
        st.error("⚠️ Model Not Available")
        st.markdown("""
        The sentiment analysis model has not been trained yet. 
        Please run the training script first:
        
        ```bash
        python scripts/train_model.py
        ```
        
        Or use the training function in the **Pipeline Status** page.
        """)
        
        with st.expander("Model Status Details"):
            st.json(model_info)
        return
    
    with st.expander("ℹ️ Model Information", expanded=False):
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Model File", "✅ Available" if model_info["model_exists"] else "❌ Missing")
            if model_info.get("model_size"):
                st.caption(f"Size: {model_info['model_size']}")
        with col2:
            st.metric("Vectorizer", "✅ Available" if model_info["vectorizer_exists"] else "❌ Missing")
            if model_info.get("vectorizer_size"):
                st.caption(f"Size: {model_info['vectorizer_size']}")
    
    st.divider()
    
    st.subheader("📝 Enter Review Text")
    
    col1, col2 = st.columns([3, 1])
    
    with col2:
        st.markdown("**Quick Examples:**")
        selected_sample = st.selectbox(
            "Load sample",
            options=["Custom"] + list(SAMPLE_REVIEWS.keys()),
            label_visibility="collapsed"
        )
    
    with col1:
        if selected_sample != "Custom":
            default_text = SAMPLE_REVIEWS[selected_sample]
        else:
            default_text = ""
        
        text_input = st.text_area(
            "Review Text",
            value=default_text,
            height=150,
            placeholder="Enter a product review here...",
            label_visibility="collapsed"
        )
    
    col1, col2, col3 = st.columns([1, 1, 2])
    
    with col1:
        analyze_clicked = st.button(
            "🔍 Analyze Sentiment",
            type="primary",
            use_container_width=True,
            disabled=not text_input.strip()
        )
    
    with col2:
        clear_clicked = st.button("🗑️ Clear", use_container_width=True)
    
    if clear_clicked:
        st.rerun()
    
    if "prediction_history" not in st.session_state:
        st.session_state.prediction_history = []
    
    if analyze_clicked and text_input.strip():
        with st.spinner("Analyzing sentiment..."):
            try:
                result = pred_service.predict_single(text_input)
                
                st.session_state.prediction_history.insert(0, result)
                if len(st.session_state.prediction_history) > 10:
                    st.session_state.prediction_history = st.session_state.prediction_history[:10]
                
                st.divider()
                st.subheader("📊 Analysis Result")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    if result.is_positive:
                        st.success("### ✅ POSITIVE")
                    else:
                        st.error("### ❌ NEGATIVE")
                
                with col2:
                    if result.confidence > CONFIDENCE_HIGH_THRESHOLD:
                        confidence_color = "green"
                    elif result.confidence > CONFIDENCE_MEDIUM_THRESHOLD:
                        confidence_color = "orange"
                    else:
                        confidence_color = "red"
                    st.markdown(f"""
                    ### Confidence: <span style="color: {confidence_color}">{result.confidence_percent}</span>
                    """, unsafe_allow_html=True)
                
                st.progress(result.confidence)
                
                with st.expander("📋 Interpretation Guide"):
                    st.markdown("""
                    **Confidence Score Interpretation:**
                    - **> 80%**: High confidence - the model is very sure about its prediction
                    - **60-80%**: Moderate confidence - prediction is likely correct but has some uncertainty
                    - **< 60%**: Low confidence - the review might have mixed sentiments or ambiguous language
                    
                    **Note**: The model classifies reviews as binary (Positive/Negative). 
                    Neutral reviews (score=3) are excluded from training.
                    """)
                
            except Exception as e:
                st.error(f"❌ Prediction Error: {e}")
    
    if st.session_state.prediction_history:
        st.divider()
        st.subheader("📜 Recent Predictions")
        
        for i, result in enumerate(st.session_state.prediction_history[:5]):
            with st.container():
                col1, col2, col3 = st.columns([1, 1, 4])
                with col1:
                    emoji = "✅" if result.is_positive else "❌"
                    st.markdown(f"**{emoji} {result.label.upper()}**")
                with col2:
                    st.markdown(f"*{result.confidence_percent}*")
                with col3:
                    truncated = result.text[:80] + "..." if len(result.text) > 80 else result.text
                    st.caption(truncated)
