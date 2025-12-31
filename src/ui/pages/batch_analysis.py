"""
Batch analysis page for processing multiple reviews.
"""

import streamlit as st
import pandas as pd
from src.ui.services.prediction_service import PredictionService
import io


def render_batch_analysis_page():
    st.title("📋 Batch Analysis")
    
    st.markdown("""
    Upload a CSV file containing product reviews to analyze sentiment in bulk.
    The results can be downloaded with sentiment predictions added.
    """)
    
    pred_service = PredictionService()
    
    if not pred_service.is_model_available():
        st.error("⚠️ Model not available. Please train the model first.")
        return
    
    st.subheader("📤 Upload Reviews")
    
    with st.expander("📖 File Format Requirements", expanded=False):
        st.markdown("""
        Your CSV file should contain a column with review text. 
        The application will detect text columns automatically, or you can specify which column to use.
        
        **Example format:**
        | id | review_text | rating |
        |----|-------------|--------|
        | 1  | Great product! | 5 |
        | 2  | Not satisfied with quality | 2 |
        """)
        
        sample_df = pd.DataFrame({
            "id": [1, 2, 3],
            "review_text": [
                "Excellent product, highly recommend!",
                "Terrible quality, broke after one use",
                "Average product, nothing special"
            ],
            "rating": [5, 1, 3]
        })
        
        csv_sample = sample_df.to_csv(index=False)
        st.download_button(
            "📥 Download Sample CSV",
            data=csv_sample,
            file_name="sample_reviews.csv",
            mime="text/csv"
        )
    
    uploaded_file = st.file_uploader(
        "Choose a CSV file",
        type=["csv"],
        help="Upload a CSV file containing review text"
    )
    
    if uploaded_file is not None:
        try:
            df = pd.read_csv(uploaded_file)
            st.success(f"✅ Loaded {len(df)} rows from '{uploaded_file.name}'")
            
            st.subheader("📋 Data Preview")
            st.dataframe(df.head(), use_container_width=True)
            
            st.subheader("⚙️ Configuration")
            
            text_columns = df.select_dtypes(include=["object"]).columns.tolist()
            
            if not text_columns:
                st.error("No text columns found in the uploaded file.")
                return
            
            col1, col2 = st.columns(2)
            
            with col1:
                text_column = st.selectbox(
                    "Select text column for analysis",
                    options=text_columns,
                    help="Choose the column containing review text"
                )
            
            with col2:
                batch_size = st.number_input(
                    "Batch size",
                    min_value=10,
                    max_value=len(df),
                    value=min(100, len(df)),
                    help="Number of reviews to process at once"
                )
            
            st.divider()
            
            if st.button("🚀 Run Batch Analysis", type="primary", use_container_width=True):
                texts = df[text_column].fillna("").astype(str).tolist()[:batch_size]
                
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                results = []
                for i, text in enumerate(texts):
                    status_text.text(f"Processing review {i+1}/{len(texts)}...")
                    progress_bar.progress((i + 1) / len(texts))
                    
                    try:
                        result = pred_service.predict_single(text)
                        results.append({
                            "text": text[:200],
                            "sentiment": result.label,
                            "confidence": result.confidence
                        })
                    except Exception as e:
                        results.append({
                            "text": text[:200],
                            "sentiment": "error",
                            "confidence": 0.0
                        })
                
                progress_bar.empty()
                status_text.empty()
                
                results_df = pd.DataFrame(results)
                
                st.subheader("📊 Analysis Summary")
                
                summary = pred_service.get_batch_summary(
                    [pred_service.predict_single(t) for t in texts[:min(len(texts), 50)]]
                    if len(texts) <= 50 else 
                    [type('obj', (object,), {'label': r['sentiment'], 'confidence': r['confidence'], 'is_positive': r['sentiment'] == 'positive'})() for r in results]
                )
                
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.metric("Total Analyzed", summary["total"])
                with col2:
                    st.metric("Positive", summary["positive"], delta=None)
                with col3:
                    st.metric("Negative", summary["negative"], delta=None)
                with col4:
                    st.metric("Avg Confidence", f"{summary['avg_confidence']:.1%}")
                
                positive_pct = summary["positive"] / summary["total"] * 100 if summary["total"] > 0 else 0
                
                st.markdown("#### Sentiment Distribution")
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.progress(positive_pct / 100)
                with col2:
                    st.caption(f"{positive_pct:.1f}% Positive")
                
                st.subheader("📋 Detailed Results")
                
                display_df = results_df.copy()
                display_df["confidence"] = display_df["confidence"].apply(lambda x: f"{x:.1%}")
                
                st.dataframe(
                    display_df,
                    use_container_width=True,
                    height=400,
                    column_config={
                        "text": st.column_config.TextColumn("Review Text", width="large"),
                        "sentiment": st.column_config.TextColumn("Sentiment", width="small"),
                        "confidence": st.column_config.TextColumn("Confidence", width="small")
                    }
                )
                
                output_df = df.head(batch_size).copy()
                output_df["predicted_sentiment"] = results_df["sentiment"]
                output_df["confidence"] = results_df["confidence"]
                
                csv_output = output_df.to_csv(index=False)
                st.download_button(
                    "📥 Download Results with Predictions",
                    data=csv_output,
                    file_name="sentiment_analysis_results.csv",
                    mime="text/csv",
                    use_container_width=True
                )
                
        except Exception as e:
            st.error(f"❌ Error reading file: {e}")
    
    st.divider()
    
    st.subheader("📝 Manual Batch Input")
    st.markdown("Alternatively, enter multiple reviews (one per line):")
    
    manual_input = st.text_area(
        "Enter reviews (one per line)",
        height=150,
        placeholder="Great product!\nTerrible quality.\nAverage experience.",
        label_visibility="collapsed"
    )
    
    if st.button("🔍 Analyze Manual Input") and manual_input.strip():
        reviews = [r.strip() for r in manual_input.split("\n") if r.strip()]
        
        if reviews:
            with st.spinner(f"Analyzing {len(reviews)} reviews..."):
                results = pred_service.predict_batch(reviews)
                
                st.subheader("Results")
                for result in results:
                    col1, col2, col3 = st.columns([2, 1, 1])
                    with col1:
                        st.text(result.text[:60] + "..." if len(result.text) > 60 else result.text)
                    with col2:
                        if result.is_positive:
                            st.success(result.label.upper())
                        else:
                            st.error(result.label.upper())
                    with col3:
                        st.caption(result.confidence_percent)
