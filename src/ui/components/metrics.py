"""
Reusable metric card components.
"""

import streamlit as st
from typing import Optional, Union


def render_metric_card(
    title: str,
    value: Union[str, int, float],
    delta: Optional[str] = None,
    delta_color: str = "normal"
):
    st.metric(label=title, value=value, delta=delta, delta_color=delta_color)


def render_metric_row(metrics: list[dict]):
    cols = st.columns(len(metrics))
    for col, metric in zip(cols, metrics):
        with col:
            render_metric_card(**metric)


def render_data_stats(df):
    if df.empty:
        st.warning("No data to display statistics.")
        return
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Reviews", f"{len(df):,}")
    
    with col2:
        if "Score" in df.columns:
            avg_score = df["Score"].mean()
            st.metric("Average Score", f"{avg_score:.2f}")
    
    with col3:
        if "Score" in df.columns:
            positive_pct = (df["Score"] >= 4).mean() * 100
            st.metric("Positive Reviews", f"{positive_pct:.1f}%")
    
    with col4:
        if "Text" in df.columns:
            avg_length = df["Text"].astype(str).apply(len).mean()
            st.metric("Avg Review Length", f"{avg_length:.0f} chars")


def render_prediction_result_card(result, show_text: bool = True):
    if result.label == "positive":
        st.success(f"✅ **POSITIVE** (Confidence: {result.confidence_percent})")
    elif result.label == "negative":
        st.error(f"❌ **NEGATIVE** (Confidence: {result.confidence_percent})")
    else:
        st.warning(f"⚠️ **{result.label.upper()}**")
    
    if show_text and result.text:
        with st.expander("View Input Text"):
            st.text(result.text[:500] + "..." if len(result.text) > 500 else result.text)
